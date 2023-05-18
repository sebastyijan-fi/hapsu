import discord
import nest_asyncio
from discord.ext import commands
from discord.ext.commands import Command
from discord import Permissions
import os
from dotenv import load_dotenv
import openai
import logging
import json

load_dotenv()
nest_asyncio.apply()

# Persisten data layer in JSON
# Your JSON file reading/writing functions
async def load_channel_configurations():
    try:
        with open("channel_configurations.json", "r") as file:
            logging.debug("Opened channel_configurations.json for reading")
            configurations = json.load(file)
            logging.debug(f"Loaded configurations: {configurations}")
            return configurations
    except FileNotFoundError:
        logging.warning("channel_configurations.json not found, returning empty dict")
        return {}


def save_channel_configurations():
    with open("channel_configurations.json", "w") as file:
        logging.debug("Opened channel_configurations.json for writing")
        json.dump(channel_configurations, file)
        logging.debug(f"Wrote configurations: {channel_configurations}")


openai.api_key = os.getenv("ATOKEN")
BOTKEY = os.getenv('BOTKEY')

channel_configurations = {}

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

logging.basicConfig(level=logging.DEBUG)

def initialize_channel(channel):
    if isinstance(channel, discord.TextChannel):
        if channel.id not in channel_configurations:
            channel_configurations[channel.id] = {
                'system_message': "Olet kiltti avustaja botti. Vastaat aina kohteliaasti.",
                'assistant_message': "Aloita jokainen vastaus sanoilla Cha-Cha-Cha",
                'previous_messages': [],
            }
            logging.info(f"Initialized channel configuration for channel {channel.id}")
            
@bot.event
async def on_ready():
    global channel_configurations
    channel_configurations = load_channel_configurations()
    for guild in bot.guilds:
        for channel in guild.channels:
            if channel.id not in channel_configurations:
                initialize_channel(channel)
            else:
                logging.info(f"Configuration already exists for channel {channel.id}")



@bot.event
async def on_guild_channel_create(channel):
    initialize_channel(channel)

@bot.command(description="Kysy avustajalta")
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

@bot.command(description="Luo ja hallitse avustajan hahmoa. Voit määrittää 'järjestelmäviestin', joka ohjeistaa AI:n käyttäytymään tietyllä tavalla.")
async def hahmo(ctx, *, arg=None):
    channel_id = ctx.channel.id
    if channel_id in channel_configurations:
        config = channel_configurations[channel_id]
        if arg is not None:
            config['system_message'] = arg
            channel_configurations[channel_id] = config  # Update the configurations
            await ctx.send(f"Päivitit hahmosi: {arg}")
            print(f"System message content for channel {channel_id} updated to: {arg}")
            save_channel_configurations()  # Save changes
        else:
            current_message = config['system_message']
            await ctx.send(f"Hahmosi: {current_message}")
            print(f"Current system message content for channel {channel_id}: {current_message}")

@bot.command(description="Päivitä tai näytä avustajan ohje. Tämä ohje antaa suoran neuvon tai ohjeistuksen avustajalle, joka vaikuttaa sen vastauksiin.")
async def ohje(ctx, *, arg=None):
    channel_id = ctx.channel.id
    if channel_id in channel_configurations:
        config = channel_configurations[channel_id]
        if arg is not None:
            config['assistant_message'] = arg
            channel_configurations[channel_id] = config  # Update the configurations
            await ctx.send(f"Päivitit ohjeesi: {arg}")
            print(f"Assistant message content for channel {channel_id} updated to: {arg}")
            save_channel_configurations()  # Save changes
        else:
            current_message = config['assistant_message']
            await ctx.send(f"Ohjeesi: {current_message}")
            print(f"Current assistant message content for channel {channel_id}: {current_message}")



@bot.command()
async def apua(ctx):
    embed = discord.Embed(
        title="Hapsu Botin Ohjeet",
        description="Hapsu on avustaja Discord-botti, joka hyödyntää OpenAI:n tekstigenerointipalvelua vastatakseen käyttäjän viesteihin. Tässä ovat käytettävissä olevat komennot:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Aloita keskustely",
        value="Aloita keskustelu Hapsu-botin kanssa. Käyttö: `.kysy ...`",
        inline=False
    )
   
    embed.add_field(
    name="Muokkaa tai katso nykyinen hahmo",
    value="Muokkaa botin hahmoa. `.ohje ...`\nKatso botin nykyinen hahmo. `.ohje`",
    inline=False
)

    embed.add_field(
    name="Muokkaa tai katso nykyinen ohje",
    value="Muokkaa botin ohjeita. `.ohje ...`\nKatso botin nykyinen ohje. `.ohje`",
    inline=False
)


    await ctx.send(embed=embed)


        
@bot.command()
async def test(ctx):
    await ctx.send("Backend response received. Bot is functioning properly.")


bot.run(BOTKEY)
