#!/usr/bin/env python3
import sys
import time

NULL_CHAR = 0
HYPHEN = 45
SPACE = 44
OTHER_SPACE = 49
SHIFT = 32
SINGLEQ = 52
ENTER = 40
APPLE = 8
PERIOD = 55
COMMA = 54
RT_ARROW = 79
L_BRACKET = 47 
R_BRACKET = 48 
AMP = 36


def write_report(send_key, control_keys, release=True, debug=False):
    with open('/dev/hidg0', 'wb+') as fd:
        buf = [NULL_CHAR] * 8
        ctl_keys = 0
        for c in control_keys:
            ctl_keys |= c
        buf[0] = ctl_keys
        buf[2] = send_key
        if debug:
            print(buf)
        fd.write(bytearray(buf))
        if release:
           if debug:
                print([NULL_CHAR]*8)
           fd.write(bytearray([NULL_CHAR]*8))


def send_string(command, test=True):
    for c in command:
        shift = False
        if ord(c) > 96 and ord(c) < 123:
            char = ord(c) - 93
        elif ord(c) > 64 and ord(c) < 91:
            char = ord(c) - 61
            shift = True
        elif ord(c) > 48 and ord(c) < 58:
            char = ord(c) - 19
        elif ord(c) == 48:
            char = 39
        elif c == '-':
            char = HYPHEN
        elif c == ' ':
            char = SPACE
        elif c == "'":
            char = SINGLEQ
        elif c == '"':
            char = SINGLEQ # + shift
            shift = True
        elif c == '.':
            char = PERIOD
        elif c == ',':
            char = COMMA
        elif c == '{':
            char = L_BRACKET
            shift = True
        elif c == '}': 
            char = R_BRACKET
            shift = True
        elif c == '&':
            char = AMP
            shift = True
        else:
            print('MISSED SOMETHING - {}'.format(c))
        if not test:
            if shift:
                write_report(char, [SHIFT])
            else:
                write_report(char, [NULL_CHAR])


def quit_zoom():
    activate_zoom_command = """osascript -e 'tell application "zoom.us" to activate' && sleep 5 && logout"""
    send_string(activate_zoom_command, test=False)
    write_report(ENTER, [NULL_CHAR])
    time.sleep(1)
    write_report(ord('q') - 93, [APPLE], debug=True)
    write_report(ENTER, [NULL_CHAR])


def mute_zoom():
    activate_zoom_command = """osascript -e 'tell application "zoom.us" to activate' && sleep 5 && logout"""
    send_string(activate_zoom_command, test=False)
    write_report(ENTER, [NULL_CHAR])
    time.sleep(1)
    write_report(ord('a') - 93, [APPLE, SHIFT], debug=True)


def open_terminal():
    write_report(SPACE, [APPLE], debug=True)
    time.sleep(1)
    send_string("terminal", test=False)
    write_report(RT_ARROW, [NULL_CHAR])
    write_report(ENTER, [NULL_CHAR])
    time.sleep(1)
    write_report(ord('n') - 93, [APPLE], debug=True)
    time.sleep(1)


def main():
    if sys.argv[1].lower() == 'mute':
        open_terminal()
        mute_zoom()
    elif sys.argv[1].lower() == 'quit':
        open_terminal()
        quit_zoom()


if __name__ == '__main__':
    main()
