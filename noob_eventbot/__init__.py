import os
from flask import Flask, Blueprint
from flask_restful import Api, Resource, url_for
from slackeventsapi import SlackEventAdapter

import slack

app = Flask(__name__)

# Register Blueprints
from .root import root
app.register_blueprint(root)


slack_events_adapter = SlackEventAdapter(os.environ["SLACKSIGN"], "/slack/events", app)
slackclient = slack.WebClient(os.environ["SLACKCLIENT"])

@slack_events_adapter.on('app_mention')
def app_mention(event_data):
    message = event_data["event"]
    
    if message.get("subtype") is None:
        if "test welcome message" in message.get('text').lower():
            send_welcome_message(message.get('user'))
        else:
            channel = message.get("channel")
            message = f"You rang, <@{message.get('user')}>! :tada:"
            slackclient.chat_postMessage(channel=channel, text=message)


def send_welcome_message(user):
     # Get IM list
    team_info = slackclient.team_info()
    channels_info = slackclient.channels_list()
    bot_id = slackclient.auth_test().get("user_id")
    # Set the Team Name
    if team_info.get("ok"):
        team_name = team_info.get("team").get("name")
    else:
        team_name = "snhu_coders"

    # Get the general channel ID
    if channels_info.get("ok"):
        for channel in channels_info.get("channels"):
            channel_id = channel.get("id")
            name = channel.get("name")

            if name == "general":
                general = channel_id

    # open the IM channel to the new user
    im_channel = slackclient.im_open(user=user)

    greeting = """
_Welcome to *{0}*, <@{1}>!_
We're so happy that you've joined our community! Please introduce yourself in <#{3}>, and let us know what brings you to the team!
*{0}* is a place for people to _*learn*_, _*collaborate*_, _*network*_, and just hang out. Please be kind to each other, and _encourage_ learning!
I am <@{2}>, your friendly protocol droid. You may issue commands to me in any channel I'm present in _(even this one)_!
Use `<@{2}> help` to _*learn more about the commands*_ I respond to. For a _*detailed list of our channels*_, please issue the `<@{2}> channels` command.
*RULES TO LIVE BY:*
1. *Do not give away, nor expect, direct answers to homework assignments*. This is a learning community and cheating will not be tolerated.
2. *Do not post requests for help in multiple channels*. Find an appropriate channel for your request and be patient. Someone will be along to help you in time.
3. *Use code snippets*! See below for help posting code snippets. *Do not cut and paste code samples directly into chat*. It's impossible to read.
*More about Slack:*
_If you're new to Slack_, please check out the <https://get.slack.help/hc/en-us/articles/217626358-Tour-the-Slack-app#windows-app-1|Slack Tour>.
_A handy feature of Slack_ is the ability to <https://get.slack.help/hc/en-us/articles/204145658-Create-a-snippet|Create a Snippet>.
""".format(team_name, user, bot_id, general)

    slackclient.chat_postMessage(channel=im_channel.get("channel").get("id"), text=greeting)