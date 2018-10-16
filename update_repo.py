import sys
import os
import json
import subprocess
import webbrowser
import time


from html_report import HtmlReport
from pprint import pprint



# TODO
# update status adequat feststellen und 
# SystemTray Ui fuer Windows https://stackoverflow.com/questions/9494739/how-to-build-a-systemtray-app-for-windows


def update_repos(label, path, vcs, exec_path):
    """ execute the vcs update command """

    repo = {
        'label': label,
        'path': path,
        'status': '',
        'message': []
    }
    
    print('\nupdating {} [{}]'.format(path, vcs['program']))

    try:
        os.chdir(path)
    except Exception:
        repo['status'] = "warning"
        repo['message'].append(['folder not found'])
        os.chdir(exec_path)
        return repo
    #end

    cmd = ""
    if(vcs['program'] == 'git'):
        cmd = vcs['program'] + " " + vcs['command']
    elif(vcs['program'] == 'svn'):
        cmd = vcs['program'] + " " + vcs['command']
    # end

    # message = []
    try:
        proc = subprocess.Popen(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in proc.stdout:
            if 'up to date' in line or 'At revision' in line:
                repo['status'] = "upToDate"
            elif 'conflict' in line:
                repo['status'] = 'conflict'
            elif 'Updating' in line or 'Updated to revision':
                repo['status'] = "updating"
            # end
            sys.stdout.write(line)

            line.replace('\n', '')
            line.replace('\t', '')

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


def default_settings():
    """ create default settings file """

    default = {
        "execpath": ".",
        "toUpdate": [
            {
                "label": "Git Repo",
                "folder": "",
                "vcs": {
                    "program": "git",
                    "command": "pull"
                },
                "enabled": True
            },
            {
                "label": "Svn Repo",
                "folder": "",
                "vcs": {
                    "program": "svn",
                    "command": "update"
                },
                "enabled": True
            },
        ]
    }

    with open('.\\settings.json', 'w') as default_settings:
        json.dump(default, default_settings)
    # end

    default_settings.closed
# end



def load_settings():
    loaded_settings = {}
    try:
        with open('.\\settings.json', 'r') as settings_file:
            loaded_settings = json.load(settings_file)
        # end

        settings_file.closed
    except IOError:
        default_settings()
        return load_settings()
    # end
    return loaded_settings
# end


def main():
    """ Main Function """

    settings = load_settings()

    updateList = settings['toUpdate']
    report = {
        'repos': []
    }
    try:
        for repo in updateList:
            if(repo['enabled']):
                vcs = repo['vcs']
                result = update_repos(repo['label'],
                    repo['folder'], vcs, settings['execpath'])
                report['repos'].append(result)
            else:
                repo = {
                    'label': repo['label'],
                    'path': repo['folder'],
                    'status': 'disabled',
                    'message': ["repo not enabled to update"]
                }
                report['repos'].append(repo)
            # end
        # end
    except KeyboardInterrupt:
        pass
    html_report = HtmlReport(report)

    report_filename = 'report.html'

    with open('.\\' + report_filename, 'w') as report_file:
        report_file.write(html_report.get_html_report())
    # end
    report_file = 'file:///' + os.getcwd() + '\\' + report_filename
    webbrowser.open_new_tab(report_file)
    # input() # for debug use
    sys.exit(0)

# end


if __name__ == '__main__':
  main()
# end