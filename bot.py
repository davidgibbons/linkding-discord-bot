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
from urllib.parse import urlparse


def init_logger(verbose=False):
    """ Set our logging options """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO
    )

def extract_urls(text):
    words = text.split()
    urls = []

    for word in words:
        parsed_url = urlparse(word)
        if parsed_url.scheme and parsed_url.netloc:
            urls.append(word)

    return urls


def extract_tags(text, urls):
    words = text.split()
    tags = []

    for word in words:
        if word not in urls:
            tags.append(word)

    return tags

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
 
    @discord_client.event
    async def on_ready():
        logging.info("We have logged in as %s", {discord_client.user})
        
    @discord_client.event
    async def on_message(message):
        if message.author == discord_client.user:
                return
        urls = extract_urls(message.content)
        tags = extract_tags(message.content, urls)
        #url, tags = parse_url(message.content)
        #tags = uniq(tags.split())
        logging.debug("Url: %s\n tags: %s", url, tags)
        for url in urls:
            created_bookmark = await linkding_client.bookmarks.async_create(
                url,
                tag_names=tags
            )
            logging.info("Created bookmark: %s", created_bookmark)
            # Reply with the created bookmark's URL
            reply = f"Bookmark created: {created_bookmark.url}"
            await message.channel.send(reply)
    discord_client.run(arguments.discord_token)


if __name__ == "__main__":
    main()
