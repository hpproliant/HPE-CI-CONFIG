#!/usr/bin/python3
import os
import time


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
        err_code = os.system('tar -xvf {}/{}'.format(path, i))
        if err_code != 0:
            log_list.append(i)
            break
        print('Paste logs in the repo')
        paste_path = ''
        with open('{}/tmp/controller/paste_location'.format(path)) as f:
            paste_path = f.readline().strip()
        os.remove('{}/tmp/controller/paste_location'.format(path))
        print('Paste path found: {}'.format(paste_path))
        os.system('mkdir -p {}/logs/{}'.format(log_repo, paste_path))
        os.system('cp -r {}/tmp/controller {}/logs/{}'.format(
            path, log_repo, paste_path))
        os.system('cp {}/tmp/job_logs/job-output.json {}/logs/{}'.format(
            path, log_repo, paste_path))
        # tar_name = paste_path.split('/')[-1] + '.tar'
        print('Compressing logs')
        os.system((
            "cd {}/logs/{}/controller/logs;"
            "tar -cvf devstack_logs.tar devstack_logs;"
            "xz -z devstack_logs.tar;"
            "tar -cvf services.tar *.service;"
            "xz -z services.tar;"
            "rm -rf devstack_logs *.service").format(log_repo, paste_path))
        #dir_content = os.listdir('{}/logs/{}'.format(log_repo, paste_path))
        #print(dir_content)
        #for del_file in dir_content:
        #    if '.xz' not in del_file and 'job-output.json' not in del_file:
        #        os.system('rm -rf {}/logs/{}/{}'.format(
        #            log_repo, paste_path, del_file))
        print('Keeping only last 3 patchsets')
        current_change = i.split('_')[0]
        patchset_list = os.listdir('{}/logs/{}/{}'.format(
            log_repo, current_change[-2:], current_change))
        patchset_list = [int(x) for x in patchset_list if '.html' not in x]
        patchset_list.sort()
        for j in patchset_list[:-3]:
            os.system('rm -rf {}/logs/{}/{}/{}'.format(
                log_repo, current_change[:-2], current_change, j))
        print("Creating all directory htmls")
        os.system('python {}/logs2html.py {}'.format(log_repo, log_repo))
        print("Performing Git operations")
        os.chdir(log_repo)
        os.system('chmod -R 0777 *')
        os.system('git config --global user.name "hpproliant"')
        os.system('git config --global user.email "proliantutils@gmail.com"')
        os.system('git config --global credential.helper "/usr/local/share/gcm-core/git-credential-manager-core"')
        os.system('git config --global credential.credentialstore "cache"')
        os.system('git config --global credential.https://dev.azure.com.usehttppath "true"')
        os.system('git add .')
        os.system('git commit -m "Commited {}"'.format(paste_path))
        os.system('git push --set-upstream origin master')
        print("Cleaning up")
        os.system("rm -rf {}/{} {}/tmp".format(path, i, path))

    time.sleep(10)

