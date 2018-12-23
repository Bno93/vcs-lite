import sys
import os
import subprocess
import logging

class Updater(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
        pass
    # end

    def update(self, label, path, vcs, exec_path):
        """ execute the vcs update command """

        repo = {
            'label': label,
            'path': path,
            'status': '',
            'message': []
        }

        logging.info('updating {} [{}]'.format(path, vcs['program']))

        try:
            os.chdir(path)
        except Exception:
            repo['status'] = "warning"
            repo['message'].append(['folder not found'])
            os.chdir(exec_path)
            return repo
        # end

        cmd = ""
        if(vcs['program'] == 'git'):
            cmd = vcs['program'] + " " + vcs['command']
        elif(vcs['program'] == 'svn'):
            cmd = vcs['program'] + " " + vcs['command']
        # end

        # message = []
        try:
            proc = subprocess.Popen(
                cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in proc.stdout:
                if 'up to date' in line or 'At revision' in line:
                    repo['status'] = "upToDate"
                elif 'conflict' in line:
                    repo['status'] = 'conflict'
                elif 'Updating' in line or 'Updated to revision':
                    repo['status'] = "updating"
                # end

                line.replace('\n', '')
                line.replace('\t', '')
                logging.info(line)

                repo['message'].append(str(line))
            # end
        except subprocess.CalledProcessError as err:
            print("ERROR: " + err)
            sys.exit(-1)
        except KeyboardInterrupt:
            print("stop updating")
            sys.exit(-2)
        # end
        os.chdir(exec_path)
        return repo

    # end