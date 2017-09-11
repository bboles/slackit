# slackit

Send a message to someone in Slack from the commandline.

Requires a Slack API token in order to function.  More about getting a token here:
https://api.slack.com/tokens

Requires `slackclient` and `argparse` modules:
```
pip install slackclient argparse
```

```
$ python3 slackit.py -h
usage: slackit.py [-h] [-v] -u USER -m MESSAGE

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Turn on debug messages.

required arguments:
  -u USER, --user USER  Email address used for the Slack user you want the
                        message to go to.
  -m MESSAGE, --message MESSAGE
                        Text to send user.
```

```
$ python3 slackit.py -u bb@zbeba.com -m "This is a test." -v
GMT 2016-10-20 20:27:26.675 Begin execution.
GMT 2016-10-20 20:27:26.675 Get user list...
GMT 2016-10-20 20:27:26.679 Starting new HTTPS connection (1): slack.com
GMT 2016-10-20 20:27:27.220 "POST /api/users.list HTTP/1.1" 200 None
GMT 2016-10-20 20:27:27.518 Starting new HTTPS connection (1): slack.com
GMT 2016-10-20 20:27:27.820 "POST /api/chat.postMessage HTTP/1.1" 200 168
Message sent successfully.
GMT 2016-10-20 20:27:27.822 End execution.
```
