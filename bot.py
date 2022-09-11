# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long
"""linkding-discord-bot

This script will connect to discord and linkding catching urls in
discord and adding them into linkding

"""

import logging
import re
import aiolinkding
import configargparse
import discord
import discordhealthcheck


def init_logger(verbose=False):
    """ Set our logging options """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO
    )

def parse_url(string):
    """ Returns our url and any tags as a string"""
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))\s?(.*)"
    url = re.search(regex,string)
    return url.group(1,6)

def parse_arguments():
    """ Get our arguments from cli or env """
    args = configargparse.ArgParser(default_config_files=['~/.linkding-bot'])
    args.add('-c', '--config', is_config_file=True, help='config file path')
    args.add_argument('-v', '--verbose', dest='verbose', help='verbose logging', action='store_true', default=False)
    args.add('-d', '--discord-token', required=True, help='Discord bot API token', env_var='DISCORD_TOKEN')
    args.add('-l', '--linkding-token', required=True, help='Linkding API token', env_var='LINKDING_TOKEN')
    args.add('-u', '--linkding-url',  required=True, help='Linkding Rest URL', env_var='LINKDING_URL')
    return args.parse_args()

def uniq(data):
    """ Returns a uniq list """
    temp = []
    for i in data:
        temp.append(i)

    for j in data:
        if data.count(j) < 2:
            temp.remove(j)
    return temp

def main():
    """ Main """
    arguments = parse_arguments()
    init_logger(verbose=arguments.verbose)
    intents = discord.Intents.default()
    intents.message_content = True

    discord_client = discord.Client(intents=intents)
    linkding_client = aiolinkding.Client(arguments.linkding_url, arguments.linkding_token)
    discordhealthcheck.start(discord_client, port=4040)
    @discord_client.event
    async def on_ready():
        logging.info("We have logged in as %s", {discord_client.user})
    @discord_client.event
    async def on_message(message):
        if message.author == discord_client.user:
            return

        url, tags = parse_url(message.content)
        tags = uniq(tags.split())
        logging.debug("Url: %s\n tags: %s", url, tags)

        created_bookmark = await linkding_client.bookmarks.async_create(
            url,
            tag_names=tags
        )
        logging.info("Created bookmark: %s", created_bookmark)

    discord_client.run(arguments.discord_token)


if __name__ == "__main__":
    main()
