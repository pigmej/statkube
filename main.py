from getpass import getpass
from itertools import groupby
import csv
import operator
import os

from github3 import login
from prettytable import PrettyTable
import yaml


def get_settings(yaml_path=os.getenv('STATKUBE_SETTINGS_FILE',
                                     'settings.yaml')):
    with open(yaml_path) as fp:
        settings = yaml.load(fp)

    for key in settings:
        env = os.getenv(key)
        if env:
            settings[key] = env

    return settings


class GithubSession(object):

    def __init__(self):
        self.settings = get_settings()

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__,
                               self.settings['STATKUBE_USERNAME'])

    __repr__ = __str__

    @property
    def session(self):
        try:
            return self._session
        except AttributeError:
            self._session = self.login()
            return self._session

    @property
    def pull_requests(self):
        try:
            return self._pull_requests
        except AttributeError:
            self._pull_requests = self._fetch_pull_requests()
            return self._pull_requests

    def _fetch_pull_requests(self):
        query = self._build_issue_query()
        search_iter = self.session.search_issues(query)
        return [i.issue for i in search_iter]

    def login(self, method='basic'):
        if method == 'basic':
            return login(
                self.settings['STATKUBE_USERNAME'],
                # TODO: uncomment.
                # password=self.settings['STATKUBE_PASSWORD'])
                password=getpass())

    def _build_issue_query(self, type_='pr'):
        query = 'type:{} repo:{} '.format(type_,
                                          self.settings['STATKUBE_REPO'])
        query += ' '.join(
            'author:{}'.format(user)
            for user in self.settings['STATKUBE_USERS'])

        return query

    def get_general_info(self):

        def key_username(x):
            return x.user.login

        ret = []
        for username, prs in groupby(
                sorted(self.pull_requests, key=key_username),
                key=key_username):

            prs = list(prs)
            ret.append({
                'username': username,
                'open': len(filter(lambda x: x.state == 'open', prs)),
                'closed': len(filter(lambda x: x.state == 'closed', prs)),
            })

        return ret

    def get_pull_requests_data(self):
        return [{
            'id': pr.number,
            'username': pr.user.login,
            'title': pr.title,
            'state': pr.state,
            'comments': pr.comments,
            'labels': ', '.join(l.name for l in pr.labels),
            'url': pr.html_url,
        } for pr in self.pull_requests]

    def _pretty(self, data, **kwargs):
        if not data:
            raise ValueError("data argument is empty!")

        header = data[0].keys()
        ptable = PrettyTable(header, **kwargs)
        with_sorted_header = operator.itemgetter(*header)

        for item in data:
            ptable.add_row(with_sorted_header(item))

        return ptable

    def pretty_pr(self, **kwargs):
        data = self.get_pull_requests_data()
        pprs = self._pretty(data, **kwargs)
        print pprs
        return pprs

    def pretty_general(self, **kwargs):
        data = self.get_general_info()
        pprs = self._pretty(data, **kwargs)
        print pprs
        return pprs

    def _csv(self, data):
        if not data:
            raise ValueError("data argument is empty!")

        header = data[0].keys()

        path = self.settings['STATKUBE_CSV_PATH']
        with open(path, 'wb') as fp:
            writer = csv.DictWriter(fp, fieldnames=header)
            writer.writeheader()
            writer.writerows(data)

        print "Data has been saved to {}".format(os.path.abspath(path))

    def csv_pr(self):
        return self._csv(self.get_pull_requests_data())

    def csv_general(self):
        return self._csv(self.get_general_info())


gh = GithubSession()
