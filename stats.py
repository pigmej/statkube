import requests
from collections import defaultdict
from itertools import ifilter, ifilterfalse


URL = ('https://api.github.com/search/issues?q=author:lukaszo+'
       'author:loles+author:gitfred+author:andreykurilin+'
       'author:dims+author:pigmej+author:nhlfr+author:dshulyak+'
       'author:asalkeld+author:vefimova+author:tnachen+'
       'author:Frostman+is:open+org:kubernetes+type:pr')


def get_data():
    page = 1
    ret = []
    while True:
        resp = requests.get(URL + '&page={}'.format(page))
        data = resp.json()['items']
        if not data:
            break
        ret.append(data)

    return resp.json()['items']


def get_stats():
    data = get_data()
    by_users = defaultdict(list)

    for d in data:
        by_users[d['user']['login']].append(d)

    to_print = ''

    key = lambda x: x['closed_at']
    to_print += 'closed: {}\t opened: {}\n\n'.format(
        len(list(ifilter(key, data))),
        len(list(ifilterfalse(key, data)))
    )

    for user, issues in by_users.iteritems():
        to_print += '\nuser: {}\n'.format(user)
        for pr in sorted(issues, key=key):
            to_print += '\t{} ({})\n\t\t{}\n'.format(
                pr['title'],
                'Closed' if pr['closed_at'] else 'Open',
                pr['pull_request']['html_url'])

    return to_print


if __name__ == '__main__':
    print get_stats()
