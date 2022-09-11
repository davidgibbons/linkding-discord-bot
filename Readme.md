# Summary 
This bot is an open source, Discord bot that will capture urls from your discord channel and add them to a [linkding](https://github.com/sissbruecker/linkding) instance.

# Requirements

### Discord configuration
You must generate a discord bot token:
https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro

From the OAUTH settings in discord  
Give it the scope bot and the bot permission to read message history

Then copy the generated URL into a browser to invite the bot to your server.

### Linkding configuration
You also must get a Linkding REST token from `settings->integrations` and the URL to your linkding instance.

# Running locally with docker-compose
```
export DISCORD_TOKEN=<TOKEN>
export LINKDING_TOKEN=<TOKEN>
export LINKDING_URL=<path_to_linkding>
docker-compose build
docker-compose up
```


# 