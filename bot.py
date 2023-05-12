import discord
import nest_asyncio
from discord.ext import commands
from discord.ext.commands import Command
import os
from dotenv import load_dotenv
import openai

load_dotenv()
nest_asyncio.apply()

openai.api_key = os.getenv("ATOKEN")
BOTKEY = os.environ['BOTKEY']

# Channel-specific configurations
channel_configurations = {}  # Dictionary to store channel configurations

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                if channel.id not in channel_configurations:
                    channel_configurations[channel.id] = {
                        'system_message': "Olet kiltti avustaja botti. Vastaat aina kohteliaasti.",
                        'assistant_message': "Aloita jokainen vastaus sanoilla Cha-Cha-Cha",
                        'previous_messages': [],
                        # Other channel-specific settings
                    }
                    print(f"Initialized channel configuration for channel {channel.id}")

@bot.command()
async def kysy(ctx, *, arg):
    channel_id = ctx.channel.id
    if channel_id in channel_configurations:
        config = channel_configurations[channel_id]
        system_message = config.get('system_message', "")
        assistant_message = config.get('assistant_message', "")

        # Add the user's message to the conversation
        previous_messages = config.get("previous_messages", [])
        previous_messages.append({"role": "user", "content": arg})
        
        # Truncate the conversation if it exceeds a certain number of messages
        max_messages = 3  # Adjust this value based on your requirements
        if len(previous_messages) > max_messages:
            previous_messages = previous_messages[-max_messages:]

        # Construct the conversation with the system and assistant messages
        conversation = [{"role": "system", "content": system_message}] + [{"role": "user", "content": assistant_message}] + previous_messages

        # Call OpenAI API to generate the assistant's response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
        )

        # Extract the assistant's response from the API response
        assistant_response = response['choices'][0]['message']['content'].strip()

        # Add the assistant's response to the conversation and update the channel-specific configuration
        previous_messages.append({"role": "assistant", "content": assistant_response})
        config["previous_messages"] = previous_messages  # Save only the user and assistant messages
        channel_configurations[channel_id] = config

        # Send the assistant's response to the user
        await ctx.send(assistant_response)


@bot.command()
async def hahmo(ctx, *, arg=None):
    channel_id = ctx.channel.id
    if channel_id in channel_configurations:
        config = channel_configurations[channel_id]
        if arg is not None:
            config['system_message'] = arg
            await ctx.send(f"Updated system message content to: {arg}")
            print(f"System message content for channel {channel_id} updated to: {arg}")
        else:
            current_message = config['system_message']
            await ctx.send(f"Current system message content: {current_message}")
            print(f"Current system message content for channel {channel_id}: {current_message}")
    else:
        await ctx.send("This command is not available in the current channel.")


@bot.command()
async def ohje(ctx, *, arg=None):
    channel_id = ctx.channel.id
    if channel_id in channel_configurations:
        config = channel_configurations[channel_id]
        if arg is not None:
            config['assistant_message'] = arg
            await ctx.send(f"Updated assistant message content to: {arg}")
            print(f"Assistant message content for channel {channel_id} updated to: {arg}")
        else:
            current_message = config['assistant_message']
            await ctx.send(f"Current assistant message content: {current_message}")
            print(f"Current assistant message content for channel {channel_id}: {current_message}")
    else:
        await ctx.send("This command is not available in the current channel.")



        
@bot.command()
async def test(ctx):
    await ctx.send("Backend response received. Bot is functioning properly.")


bot.run(BOTKEY)
