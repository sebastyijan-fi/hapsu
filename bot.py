import discord
import nest_asyncio
from discord.ext import commands
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
                        'assistant_message': {
                            "role": "assistant",
                            "content": "Aloita jokainen vastaus sanoilla Cha-Cha-Cha",
                            "previous_messages": []
                        },
                        # Other channel-specific settings
                    }
                    print(f"Initialized channel configuration for channel {channel.id}")



@bot.command()
async def kysy(ctx, *, arg):
    channel_id = ctx.channel.id
    if channel_id in channel_configurations:
        config = channel_configurations[channel_id]
        system_message = config.get('system_message', "")
        assistant_message = config.get('assistant_message', {})

        # Construct the conversation history
        conversation = []
        conversation.append({"role": "system", "content": system_message})
        conversation.append({"role": "user", "content": arg})

        # Add previous assistant messages to the conversation
        previous_assistant_messages = assistant_message.get("previous_messages", [])
        for message in previous_assistant_messages:
            conversation.append({"role": "assistant", "content": message})

        # Call OpenAI API to generate the assistant's response
        response = openai.Completion.create(
            model="text-davinci-003",  # Use the GPT-3.5 Turbo model
            messages=conversation,
            max_tokens=50,  # Adjust the maximum number of tokens as per your requirement
        )

        # Extract the assistant's response from the API response
        assistant_response = response.choices[0].message.content.strip()

        # Store the assistant's response in the channel-specific configuration
        assistant_message["previous_messages"].append(assistant_response)

        # Use the assistant's response for further processing or sending to the user
        # ...

        # Update the channel-specific configuration
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
            config['assistant_message']['content'] = arg
            await ctx.send(f"Updated assistant message content to: {arg}")
            print(f"Assistant message content for channel {channel_id} updated to: {arg}")
        else:
            current_message = config['assistant_message']['content']
            await ctx.send(f"Current assistant message content: {current_message}")
            print(f"Current assistant message content for channel {channel_id}: {current_message}")
    else:
        await ctx.send("This command is not available in the current channel.")

        
@bot.command()
async def test(ctx):
    await ctx.send("Backend response received. Bot is functioning properly.")


bot.run(BOTKEY)
