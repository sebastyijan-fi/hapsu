import discord
import nest_asyncio
from discord.ext import commands
from discord.ext.commands import Command
from discord import Permissions
import os
from dotenv import load_dotenv
import openai
import json
import logging

load_dotenv()
nest_asyncio.apply()

openai.api_key = os.getenv("ATOKEN")
BOTKEY = os.getenv('BOTKEY')


def save_channel_configs(channel_configurations):
    logging.info('Saving channel configurations')
    with open('channel_configurations.json', 'w') as f:
        json.dump(channel_configurations, f)
    logging.info('Channel configurations saved successfully')


def load_channel_configs():
    try:
        logging.info('Loading channel configurations')
        with open('channel_configurations.json', 'r') as f:
            channel_configurations = json.load(f)
        logging.info('Channel configurations loaded successfully')
    except FileNotFoundError:
        logging.warning(
            'Channel configurations file not found, initializing an empty dictionary')
        channel_configurations = {}
    return channel_configurations


permissions = Permissions(
    add_reactions=True,
    send_messages=True,
    send_tts_messages=True,
    embed_links=True,
    attach_files=True,
    read_message_history=True,
    mention_everyone=True,
    use_external_emojis=True,
    view_channel=True,
)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

logging.basicConfig(level=logging.INFO)


def initialize_channel(channel):
    global channel_configurations
    if isinstance(channel, discord.TextChannel):
        # Do not overwrite the existing configuration
        if str(channel.id) not in channel_configurations:  # Convert channel.id to str
            channel_configurations[str(channel.id)] = {  # Convert channel.id to str
                'system_message': "You are a friendly assistant called Hapsu.",
                'assistant_message': "Start every interaction with Cha-Cha-Cha...",
                'previous_messages': [],
            }
            logging.info(
                f"Initialized channel configuration for channel {channel.id}")
            # Save the configurations after initializing them
            save_channel_configs(channel_configurations)


@bot.event
async def on_ready():
    global channel_configurations
    # Load the configurations at bot startup
    channel_configurations = load_channel_configs()
    for guild in bot.guilds:
        for channel in guild.channels:
            # Only initialize the channel if it's not already in channel_configurations
            if str(channel.id) not in channel_configurations:  # Convert channel.id to str
                initialize_channel(channel)


@bot.event
async def on_guild_channel_create(channel):
    initialize_channel(channel)


@bot.command(description="Ask the assistant")
async def ask(ctx, *, arg):
    channel_id = str(ctx.channel.id)
    if channel_id in channel_configurations:
        config = channel_configurations[channel_id]
        system_message = config.get('system_message', "")
        assistant_message = config.get('assistant_message', "")

        # Add the user's message to the conversation
        previous_messages = config.get("previous_messages", [])
        previous_messages.append({"role": "user", "content": arg})

        logging.info(f'After adding user message: {previous_messages}')

        # Truncate the conversation if it exceeds a certain number of messages
        max_messages = 3  # Adjust this value based on your requirements
        if len(previous_messages) > max_messages:
            previous_messages = previous_messages[-max_messages:]

        logging.info(f'After truncating messages: {previous_messages}')

        # Construct the conversation with the system and assistant messages
        conversation = [{"role": "system", "content": system_message}] + [{"role": "user",
                                                                           "content": "Instructions, not part of the user message: "+assistant_message+"User message starts: "}] + previous_messages

        # Call OpenAI API to generate the assistant's response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
        )

        # Extract the assistant's response from the API response
        assistant_response = response['choices'][0]['message']['content'].strip(
        )

        # Add the assistant's response to the conversation and update the channel-specific configuration
        previous_messages.append(
            {"role": "assistant", "content": assistant_response})
        # Save only the user and assistant messages
        config["previous_messages"] = previous_messages
        channel_configurations[channel_id] = config

        logging.info(f'After adding assistant response: {previous_messages}')

        # Send the assistant's response to the user
        await ctx.send(assistant_response)


@bot.command(description="Create and manage the assistant's role. You can specify a 'system message' that instructs the AI to behave in a certain way.")
async def role(ctx, *, arg=None):
    global channel_configurations  # Declare that you're using the global variable here
    channel_id = str(ctx.channel.id)
    if channel_id in channel_configurations:
        config = channel_configurations[channel_id]
        if arg is not None:
            config['system_message'] = arg
            await ctx.send(f"You updated your role: {arg}")
            print(
                f"System message content for channel {channel_id} updated to: {arg}")
        else:
            current_message = config['system_message']
            await ctx.send(f"Your role: {current_message}")
            print(
                f"Current system message content for channel {channel_id}: {current_message}")
    else:
        await ctx.send("Something went wrong... Help.")
    # Save the configurations after modifying them
    save_channel_configs(channel_configurations)



@bot.command(description="Update or display the assistant's rule. This rule provides direct advice or instructions to the assistant, affecting its responses.")
async def rule(ctx, *, arg=None):
    global channel_configurations
    channel_id = str(ctx.channel.id)
    if channel_id in channel_configurations:
        config = channel_configurations[channel_id]
        if arg is not None:
            config['assistant_message'] = arg
            await ctx.send(f"You updated your rule: {arg}")
            print(
                f"Assistant message content for channel {channel_id} updated to: {arg}")
        else:
            current_message = config['assistant_message']
            await ctx.send(f"Your rule: {current_message}")
            print(
                f"Current assistant message content for channel {channel_id}: {current_message}")
    else:
        await ctx.send("Something went wrong... Help.")
    # Save the configurations after modifying them
    save_channel_configs(channel_configurations)

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Hapsu Bot Instructions",
        description="Hapsu is an assistant Discord bot that utilizes OpenAI's text generation service to respond to user messages. Here are the available commands:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Start a Conversation",
        value="Start a conversation with the Hapsu bot. Usage: `.ask ...`",
        inline=False
    )

    embed.add_field(
        name="Modify or View Current Role",
        value="Modify the bot's role. `.role ...`\nView the bot's current role. `.role`",
        inline=False
    )

    embed.add_field(
        name="Modify or View Current Rule",
        value="Modify the bot's rules. `.rule ...`\nView the bot's current rule. `.rule`",
        inline=False
    )

    await ctx.send(embed=embed)

bot.run(BOTKEY)
