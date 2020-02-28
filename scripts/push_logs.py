import os
import time


import pdb; pdb.set_trace()
log_list = []
path = '/home/ironman-build/hpeironicci_incoming_logs'
log_repo = '/home/ironman-build/hpeproliant.github.io'
while True:
    if len(log_list) == 0:
        log_list = [x for x in os.listdir(path) if '.tar' in x]
    while len(log_list) > 0:
        i = log_list.pop()
        print("Found {}. Extracting....".format(i))
        os.chdir(path)
        os.system('tar -xvf {}/{}'.format(path, i))
        print('Paste logs in the repo')
        paste_path = ''
        with open('{}/tmp/controller/paste_location'.format(path)) as f:
            paste_path = f.readline().strip()
        print('Paste path found: {}'.format(paste_path))
        os.system('mkdir -p {}/logs/{}'.format(log_repo, paste_path))
        os.system('cp -r {}/tmp/controller {}/logs/{}'.format(
            path, log_repo, paste_path))
        os.system('cp -r {}/tmp/job_logs/* {}/logs/{}'.format(
            path, log_repo, paste_path))
#        print('Keeping only last 3 patchsets')
#        current_change, current_patchset = i.split('.tar')[0].split('_')
#        patchset_list = os.listdir('{}/logs/{}/{}'.format(
#            log_repo, current_change[-2:], current_change))
#        patchset_list = [int(x) for x in patchset_list if '.html' not in x]
#        patchset_list.sort()
#        for j in patchset_list[:-3]:
#            os.system('rm -rf {}/logs/{}/{}/{}'.format(
#                log_repo, current_change[:-2], current_change, j))
        print("Creating all directory htmls")
        os.remove('{}/logs/{}/controller/paste_location'.format(log_repo, paste_path))
        os.system('python {}/logs2html.py {}'.format(log_repo, log_repo))
        print("Performing Git operations")
        os.chdir(log_repo)
        os.system('git add .')
        os.system('git commit -m "Commited {}"'.format(paste_path))
        os.system('git push')
        print("Cleaning up")
        os.system("rm -rf {}/{} {}/tmp".format(path, i, path))

    time.sleep(10)

