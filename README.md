Usage
=====

Place the settings in `settings.yaml` on in some other place and set
env var `STATKUBE_SETTINGS_FILE`.

```
usage: statkube.py [-h] [-n] [-c CSV_PATH]
                   [-s {username,title,url,labels,comments,state,id}]
                   [-t {general,prs}] [-u USERNAME] [-p PASSWORD] [-a]

Fetch pull requests stats from GitHub.Place your settings in settings.yaml or
setup custom path by settings env: STATKUBE_SETTINGS_FILE.

optional arguments:
  -h, --help            show this help message and exit
  -n, --no-pretty
  -c CSV_PATH, --csv-path CSV_PATH
  -s {username,title,url,labels,comments,state,id}, --sortby {username,title,url,labels,comments,state,id}
  -t {general,prs}, --type {general,prs}
  -u USERNAME, --username USERNAME
                        Github Username use to login
  -p PASSWORD, --password PASSWORD
                        Github password use to login
  -a, --ask-for-password
                        Force ask for password
```

