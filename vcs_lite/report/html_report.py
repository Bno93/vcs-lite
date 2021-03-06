import time
from yattag import Doc


class HtmlReport(object):

    def __init__(self, report):

        self.__doc, self.__tag, self.__text = Doc().tagtext()
        self.__create_html_page(report)

    # end

    def __create_html_page(self, report):
        self.__doc.asis('<!DOCTYPE html>')
        with self.__tag('html'):
            self.__create_html_header(report)
            self.__create_html_body(report)
    # end

    def __create_html_header(self, report):
        with self.__tag('head'):
            with self.__tag('meta', charset='utf-8'):
                pass
            # end
            with self.__tag('meta', ("http-equiv", "X-UA-Compatible"), content="IE=edge"):
                pass
            # end
            with self.__tag('meta', name="viewport", content="width=device-width, initial-scale=1"):
                pass
            # end
            with self.__tag('title'):
                self.__text('Repo Report')
            # end
            with self.__tag('link', rel='stylesheet',
                            href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
                            integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u",
                            crossorigin="anonymous"):
                pass
            # end
            with self.__tag('script', src='https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js'):
                pass
            # end
            with self.__tag('script', src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js",
                            integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa",
                            crossorigin="anonymous"):
                pass
            # end
            with self.__tag('script'):
                self.__text('$(document).ready(function () {\n')
                for repo in report['repos']:
                    self.__text(
                        "$('#" + self.__create_id(repo['label']) + "').on('shown.bs.collapse', function() {$('#" + self.__create_chevron_id(repo['label']) + "').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');});\n")
                    self.__text(
                        "$('#" + self.__create_id(repo['label']) + "').on('hidden.bs.collapse', function() {$('#" + self.__create_chevron_id(repo['label']) + "').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');});\n")
                # end
                self.__text('});')
            with self.__tag('style'):
                self.__text(
                    "#content{margin-left:10%;margin-right:10%;margin-top:1%;padding-left:10%;padding-right:10%;padding-top:1%;}\n")
                self.__text('span { float: right; }\n')
                self.__text('#heading{ margin:2%; }\n')
                self.__text('.text-overflow { text-overflow: ellipsis; overflow: hidden; }\n')
            # end
    # end

    def __choose_panel_status(self, status):
        if status == 'upToDate':
            return 'panel-success'
        if status == 'updating':
            return 'panel-info'
        if status == 'error' or status == 'conflict':
            return 'panel-danger'
        if status == 'warning':
            return 'panel-warning'
        else:
            return 'panel-default'

    # end

    # private\mobilecomputing\mobilecomputing_programmentwurf

    def __create_id(self, name):
        html_id = str(name)
        html_id = html_id.replace(".", "")
        html_id = html_id.replace("\\", "-")
        html_id = html_id.replace(" ", "_")
        html_id = html_id.replace("(", "")
        html_id = html_id.replace(")", "")
        return html_id
    # end

    def __create_chevron_id(self, name):
        html_id = str(name)
        html_id = html_id.replace(".", "")
        html_id = html_id.replace("\\", "-")
        html_id = html_id.replace(" ", "_")
        html_id = html_id.replace("(", "")
        html_id = html_id.replace(")", "")
        return html_id + "-cheveron"

    # end

    def __create_repo_panel_head(self, label, path):
        with self.__tag('div', klass='panel-heading text-overflow'):
            self.__text("{} ({})".format(label, path))
            repo_id = self.__create_id(label)
            cheveron_id = self.__create_chevron_id(label)
            with self.__tag('span', ("data-toggle", "collapse"), ("data-target", "#{}".format(repo_id)), id=cheveron_id, klass="glyphicon glyphicon-chevron-down"):
                self.__text('')
            # end
        # end
    # end

    def __create_repo_panel_body(self, label, message):
        with self.__tag('div', klass='panel-body repo collapse', id='{}'.format(self.__create_id(label))):


            if type(message) is list:
                print("message is a list: {}".format(message))
                with self.__tag('ul', klass='list-group'):
                    for line in message:
                        with self.__tag('li', klass='list-group-item'):
                            self.__text(str(line))
                        # end
                    # end
                # end
            # end
        # end
    # end

    def __create_repo_panel(self, repo):
        panel_status = self.__choose_panel_status(repo['status'])

        with self.__tag('div', klass='panel ' + panel_status):
            self.__create_repo_panel_head(repo['label'], repo['path'])
            self.__create_repo_panel_body(repo['label'], repo['message'])
        # end
    # end

    def __create_html_body(self, report):
        with self.__tag('body'):
            with self.__tag('div', klass='panel panel-default', id='heading'):
                with self.__tag('div', klass='panel-heading'):
                    self.__text('Repo Update Report from ' +
                                time.strftime('%H:%M %d.%m.%Y'))
                    with self.__tag('span', ("data-toggle", "collapse"), ("data-target", "{}".format(".repo")), klass="glyphicon glyphicon-chevron-down"):
                        self.__text('')
                    # end
                # end
                with self.__tag('div', klass='panel-body', id='content'):
                    for repo in report['repos']:
                        self.__create_repo_panel(repo)
                    # end
                # end
            # end
        # end
    # end

    def get_html_report(self):
        return self.__doc.getvalue()
    # end

# end
