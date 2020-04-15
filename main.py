#!/usr/bin/env python3

import requests

from datetime import datetime, timedelta
import threading
import time
import re
import subprocess

PROGRAMS = "https://wappuradio.fi/api/programs"
STREAM_URL = "https://stream.wappuradio.fi/wappuradio.opus"

def save(prog):
    print (prog)
    name = re.sub('[^A-Za-z0-9]', '', prog['name'])
    #start = prog['start'].strftime('%Y-%m-%d_%H:%M:%S')
    start = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    fname = "%s_%s.opus" % (name, start)
    cmd = "curl -s --output %s %s" % (fname, STREAM_URL)
    print (cmd)
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    length = (prog['end'] - datetime.now()).total_seconds()
    print ("%s seconds left of the program" % (length,))
    time.sleep(length)
    proc.terminate()
    print ("%s ended" % (prog["title"],))

def main():
    r = requests.get(PROGRAMS)
    unsorted_data = r.json()
    data = sorted(unsorted_data, key=lambda k: k['start']) 
    #print (data)
    for prog in data:
        #print (prog)
        #return None
        start = datetime.strptime(prog['start'], '%Y-%m-%dT%H:%M:%S+03:00') - timedelta(minutes=5)
        prog['start'] = start
        end = datetime.strptime(prog['end'], '%Y-%m-%dT%H:%M:%S+03:00') + timedelta(minutes=5)
        prog['end'] = end
        if datetime.now() > end:
            print ('Skipping %s' % (title,))
            continue
        #print (start, end, delay)

        delay = (start - datetime.now()).total_seconds()
        if delay > 900:
            time.sleep(delay-300)
        delay = (start - datetime.now()).total_seconds()
        print ('Queuing %s %s' % (prog['title'], start))
        threading.Timer(delay, save, [prog]).start()

if __name__ == '__main__':
    main()
