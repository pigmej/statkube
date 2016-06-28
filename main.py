import os
from getpass import getpass
import operator
from itertools import groupby

from github3 import login
from prettytable import PrettyTable
import yaml


def get_settings(yaml_path=os.getenv('GITHUB_SETTINGS_FILE', 'settings.yaml')):
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
                               self.settings['GITHUB_USERNAME'])

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
                self.settings['GITHUB_USERNAME'],
                # password=self.settings['GITHUB_PASSWORD'])
                password=getpass())

    def _build_issue_query(self, type_='pr'):
        query = 'type:{} repo:{} '.format(type_, self.settings['GITHUB_REPO'])
        query += ' '.join(
            'author:{}'.format(user) for user in self.settings['GITHUB_USERS'])
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
        headers = data[0].keys()
        ptable = PrettyTable(headers, **kwargs)
        with_sorted_headers = operator.itemgetter(*headers)

        for pr in data:
            ptable.add_row(with_sorted_headers(pr))

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


gh = GithubSession()
