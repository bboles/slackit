import os, json, logging, time
from argparse import ArgumentParser
from slackclient import SlackClient

logging.Formatter.converter = time.gmtime

if 'SLACK_TOKEN' not in os.environ:
    print ("Please set SLACK_TOKEN in your environment.")
    sys.exit(1)

#SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
SLACK_TOKEN = 'xoxp-2156392767-19815126276-33228244965-c56e084c6c'
slack_client = SlackClient(SLACK_TOKEN)

def test_slack(slack_client):
    slack_client.api_call("api.test")

def get_users(slack_client):
    logging.debug("Get user list...")
    users = (slack_client.api_call("users.list"))
    users = json.dumps(users)
    users = json.loads(str(users))
    return users


def display_users(slack_client, users):
    # display active users
    for i in users['members']:
        # don't display slackbot
        if i['profile']['real_name'] != "slackbot":
            # don't display deleted users
            if not i['deleted']:
                # display real name
                # print (i['profile']['real_name'])
                logging.debug("{0}".format(i['profile']['real_name']))


def find_user(users, channel): 
    for i in users['members']:
        if not i['deleted']:
            if i['profile']['real_name'] != "slackbot":
                try:                                        # not every profile has an email
                    if i['profile']['email'] == channel:
                        return(i['id'])
                except:
                    pass


def message_user(slackid, message):
    slackresponse = slack_client.api_call(
            "chat.postMessage",
            channel=slackid,
            username="tagoverlordbot",
            text=message,
            as_user="false",
            link_names=1,
            unfurl_links="true"
    )

    if slackresponse.get('ok'):
        logging.debug("Message sent successfully.")
        return True
    else:
        logging.warning("=== There was a problem and message was not sent. ===")
        # TODO: add more debug here so we can what the problem was
        # print(slackresponse)
        return False


def slackit(channel, message):
    logging.warning("channel: {0}".format(channel))
    logging.warning("message: {0}".format(message))
    users = get_users(slack_client)

    if ('@' in channel):
        slackid = find_user(users, channel)
    else:
        slackid = channel

    success = message_user(slackid, message)
    return success      # should be True or False


def main():
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', action="store_true", help='Turn on debug messages.')
    # need to make this flag mutually exclusive with -u and -m before we can use it
    # parser.add_argument('-t', '--test', action="store_true", help='Test connectivity to Slack API.')
    requiredargs = parser.add_argument_group('required arguments')
    requiredargs.add_argument('-u', '--user', action="store", help='Email address or channel used for the Slack user you want the message to go to.', required=True)
    requiredargs.add_argument('-m', '--message', action="store", help='Text to send user.', required=True)

    args = parser.parse_args()

    channel = args.user
    message = args.message
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s.%(msecs)d %(message)s',datefmt='%Y-%m-%dT%H:%M:%S')

    logging.debug("Begin execution.")

    # if args.test:
    # test_slack(slack_client)

    # users = get_users(slack_client)
    # # display_users(slack_client, users)
    # slackid = find_user(users, channel)
    # message_user(slackid, message)
    slackit(channel, message)

    logging.debug("End execution.")

if __name__ == '__main__':
    main()
