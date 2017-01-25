#!/usr/bin/python3

import os
import sys
import json
import time
import fcntl
import signal

# use:
# python3 watcher.py 'temp' 'php -f script.php'
# python3 watcher.py config.json
# watcher --help

SHOW_LOG = True
CHANGE_PATH = False
SYSTEM_COMMAND = False

arguments = sys.argv[1:]


def to_path(path):
    _path = path
    if path[-1] is not '/':
        _path = path + '/'
    return _path


def parse_json_file(file):
    directory = False
    command = False
    try:
        with open(arguments[0], 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        print('[watcher] Error. File Not Found "%s"' % (file))
    else:
        try:
            directory = to_path(config['watcher_directory'])
            command = config['watcher_command']
        except KeyError:
            print('[watcher] Config not find keys "watcher_directory" or "watcher_command"')
    return {'directory': directory, 'command': command}


if len(arguments) is 2:
    CHANGE_PATH = to_path(arguments[0])
    SYSTEM_COMMAND = arguments[1]
elif len(arguments) is 1:
    if arguments[0] == '--help':
        print('[watcher] Utility monitoring a change of the directory or file.')
        print('[watcher] Uses:')
        print('[watcher] watcher FILE_PATH "BASH_COMMANSD"')
        print('[watcher] watcher FILE_CONFIG')
        exit()
    elif os.path.isfile(arguments[0]):
        config = parse_json_file(arguments[0])
        CHANGE_PATH = config['directory']
        SYSTEM_COMMAND = config['command']
elif os.path.isfile('config.json'):
    config = parse_json_file('config.json')
    CHANGE_PATH = config['directory']
    SYSTEM_COMMAND = config['command']


if os.path.exists(CHANGE_PATH) is False:
    print('[watcher] Path not exist "%s". Exit' % (CHANGE_PATH))
    exit()
elif SYSTEM_COMMAND is False:
    print('[watcher] Command not find. Exit')
    exit()
else:
    print('[watcher] start')


def handler(signum, frame):
    try:
        if SHOW_LOG:
            print('[watcher] Catch changes "%s". run "%s"' % (CHANGE_PATH, SYSTEM_COMMAND))

        os.system(SYSTEM_COMMAND)

    except RuntimeError:
        pass


fd = os.open(CHANGE_PATH, os.O_RDONLY)
fcntl.fcntl(fd, fcntl.F_NOTIFY, fcntl.DN_MODIFY | fcntl.DN_MULTISHOT)

signal.signal(signal.SIGIO, handler)

while True:
    time.sleep(1000)
