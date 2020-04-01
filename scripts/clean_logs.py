import os
import shutil
import time


os.system('find /home/ironman-build/hpeproliant.github.io -name job-output.json > /home/ironman-build/hpeproliant.github.io_job-output')
with open('/home/ironman-build/hpeproliant.github.io_job-output', 'r') as f:
    line = f.readline().strip()
    while(line):
        if time.time() - os.path.getmtime(line) > 20*24*60*60:
            print(time.ctime(os.path.getmtime(line)))
            dir = line.split('job-output.json')[0]
            print("Deleting {}".format(dir))
            shutil.rmtree(dir)
        line = f.readline().strip()

