Installation
============
```
$ git clone https://github.com/gitfred/statkube.git
$ cd statkube
$ python setup.py install
```

Usage
=====

Place the settings in `settings.yaml` on in some other place and set
env var `STATKUBE_SETTINGS_FILE`.
You can also set and environment variable for every setting in settings.yaml:

`STATKUBE_USERNAME=gitfred python statkube.py`

```
usage: statkube [-h] [-n] [-c CSV_PATH]
                [-s {username,id,title,state,comments,url,labels}]
                [-t {general,prs}] [-u USERNAME] [-p PASSWORD] [-a]
                [--token TOKEN] [--users USERS [USERS ...]]
                [--from-date FROM_DATE] [--to-date TO_DATE]
                [-l {day,week,month}] [-g GROUP] [-q QUERY_EXTRA]
                [--show-default-settings]

Fetch pull requests stats from GitHub. Place your settings in settings.yaml or
setup custom path by settings env: STATKUBE_SETTINGS_FILE.

optional arguments:
  -h, --help            show this help message and exit
  -n, --no-pretty
  -c CSV_PATH, --csv-path CSV_PATH
  -s {username,id,title,state,comments,url,labels}, --sortby {username,id,title,state,comments,url,labels}
  -t {general,prs}, --type {general,prs}
  -u USERNAME, --username USERNAME
                        Github Username use to login
  -p PASSWORD, --password PASSWORD
                        Github password use to login
  -a, --ask-for-password
                        Force ask for password
  --token TOKEN         Access token to Github.
  --users USERS [USERS ...]
                        GitHub usernames for lookup for example: ./statkube.py
                        -a --users gitfred pigmej nhlfr
  --from-date FROM_DATE
                        Created FROM date, format: YYYY-MM-DD
  --to-date TO_DATE     Created TO date, format: YYYY-MM-DD
  -l {day,week,month}, --last {day,week,month}
  -g GROUP, --group GROUP
                        The group of users must be defined first in
                        'settings.yaml' as 'STATKUBE_GROUP_<custom_name>'.
                        Then pass <custom_name> as an argument here.
  -q QUERY_EXTRA, --query-extra QUERY_EXTRA
                        This will be added to GH query. As a reference please
                        see GitHub search API. Env var: STATKUBE_QUERY_EXTRA
  --show-default-settings
                        Shows the localization of default settings file which
                        can be copied and changed. Use then
                        STATKUBE_SETTINGS_FILE env var.
```

Authentication
==============

Run `./statkube -a` or with password provided in `settings.yaml` or in env var.

```
sylwester➜~/devment/statkube(master✗)» ./statkube.py -a
GitHub Password for gitfred:
+---------------+------+--------+
|    username   | open | closed |
+---------------+------+--------+
|    Frostman   |  1   |   0    |
| andreykurilin |  4   |   2    |
|    asalkeld   |  5   |   6    |
|      dims     |  8   |   9    |
|    dshulyak   |  0   |   2    |
|    gitfred    |  1   |   3    |
|     nebril    |  2   |   1    |
|     nhlfr     |  6   |   2    |
|    tnachen    |  0   |   2    |
|    vefimova   |  2   |   1    |
|     zefciu    |  1   |   1    |
+---------------+------+--------+
```

Now GH access token is saved to `.ghtoken` file. You do not need use your
password any more, just run `./statkube.py`

```
sylwester➜~/devment/statkube(master✗)» ./statkube.py
+---------------+------+--------+
|    username   | open | closed |
+---------------+------+--------+
|    Frostman   |  1   |   0    |
| andreykurilin |  4   |   2    |
|    asalkeld   |  5   |   6    |
|      dims     |  8   |   9    |
|    dshulyak   |  0   |   2    |
|    gitfred    |  1   |   3    |
|     nebril    |  2   |   1    |
|     nhlfr     |  6   |   2    |
|    tnachen    |  0   |   2    |
|    vefimova   |  2   |   1    |
|     zefciu    |  1   |   1    |
+---------------+------+--------+
```

In case of `422 Validation error`, remove your current keys from
https://github.com/settings/tokens


Example run for general (default) info:
=======================================

```
sylwester➜~/devment/statkube(master✗)» ./statkube.py -a -s username --last week
GitHub Password for gitfred:
+----------+------+--------+
| username | open | closed |
+----------+------+--------+
| asalkeld |  1   |   2    |
|  nhlfr   |  1   |   0    |
| vefimova |  1   |   0    |
+----------+------+--------+
```

Example run for prs type info:
==============================

```
sylwester➜~/devment/statkube(master)» ./statkube.py -a -s username --last day -t prs
GitHub Password for gitfred:
+----------+------------------------------------------------------+-----------------------------------------------------+---------------------------------------------+----------+-------+-------+
| username |                        title                         |                         url                         |                    labels                   | comments | state |   id  |
+----------+------------------------------------------------------+-----------------------------------------------------+---------------------------------------------+----------+-------+-------+
|  nhlfr   | [WIP] Return (bool, error) in Authorizer.Authorize() | https://github.com/kubernetes/kubernetes/pull/28281 | cla: yes, release-note-label-needed, size/L |    0     |  open | 28281 |
+----------+------------------------------------------------------+-----------------------------------------------------+---------------------------------------------+----------+-------+-------+
```

Example use of custom query:
============================

```
sylwester➜~/devment/statkube(master✗)» ./statkube.py -a -s username --last week -t prs -q "label:lgtm"
GitHub Password for gitfred:
+----------+--------------------------------------------------------+-----------------------------------------------------+---------------------------------------------------------------------------------------------------------+----------+--------+-------+
| username |                         title                          |                         url                         |                                                  labels                                                 | comments | state  |   id  |
+----------+--------------------------------------------------------+-----------------------------------------------------+---------------------------------------------------------------------------------------------------------+----------+--------+-------+
| asalkeld |       Fix startup type error in initializeCaches       | https://github.com/kubernetes/kubernetes/pull/28002 | area/storage, cherrypick-approved, cla: yes, lgtm, priority/P0, release-note-none, size/L, team/cluster |    35    | closed | 28002 |
| asalkeld | Ignore cmd/libs/go2idl/generator when running coverage | https://github.com/kubernetes/kubernetes/pull/28166 |                                cla: yes, lgtm, release-note-none, size/XS                               |    8     | closed | 28166 |
+----------+--------------------------------------------------------+-----------------------------------------------------+---------------------------------------------------------------------------------------------------------+----------+--------+-------+
```

Example use of defined users group:
===================================

```
# settings.yaml:
...
# Define groups as "STATKUBE_GROUP_<custom_name>"
STATKUBE_GROUP_POZNAN:
  - gitfred
  - nebril
  - nhlfr
  - zefciu
...


sylwester➜~/devment/statkube(master)» ./statkube.py -a -s username --last week -t prs -g POZNAN                                                                                           [15:02:12]
GitHub Password for gitfred:
+----------+------------------------------------------------------+-----------------------------------------------------+---------------------------------------------+----------+-------+-------+
| username |                        title                         |                         url                         |                    labels                   | comments | state |   id  |
+----------+------------------------------------------------------+-----------------------------------------------------+---------------------------------------------+----------+-------+-------+
|  nhlfr   | [WIP] Return (bool, error) in Authorizer.Authorize() | https://github.com/kubernetes/kubernetes/pull/28281 | cla: yes, release-note-label-needed, size/L |    1     |  open | 28281 |
+----------+------------------------------------------------------+-----------------------------------------------------+---------------------------------------------+----------+-------+-------+
```
