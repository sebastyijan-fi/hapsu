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
    with open('channel_configurations.json', 'w') as f:
        json.dump(channel_configurations, f)

        
def load_channel_configs():
    try:
        with open('channel_configurations.json', 'r') as f:
            channel_configurations = json.load(f)
    except FileNotFoundError:
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
        if channel.id not in channel_configurations:
            channel_configurations[channel.id] = {
                'system_message': "Olet kiltti avustaja botti. Vastaat aina kohteliaasti.",
                'assistant_message': "Aloita jokainen vastaus sanoilla Cha-Cha-Cha",
                'previous_messages': [],
            }
            logging.info(f"Initialized channel configuration for channel {channel.id}")
            save_channel_configs(channel_configurations)  # Save the configurations after initializing them

@bot.event
async def on_ready():
    global channel_configurations
    channel_configurations = load_channel_configs()  # Load the configurations at bot startup
    for guild in bot.guilds:
        for channel in guild.channels:
            # Only initialize the channel if it's not already in channel_configurations
            if channel.id not in channel_configurations:
                initialize_channel(channel)

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
    global channel_configurations  # Declare that you're using the global variable here
    channel_id = ctx.channel.id
    if channel_id in channel_configurations:
        config = channel_configurations[channel_id]
        if arg is not None:
            config['system_message'] = arg
            await ctx.send(f"Päivitit hahmosi: {arg}")
            print(f"System message content for channel {channel_id} updated to: {arg}")
        else:
            current_message = config['system_message']
            await ctx.send(f"Hahmosi: {current_message}")
            print(f"Current system message content for channel {channel_id}: {current_message}")
    else:
        await ctx.send("Joku meni vikaan...Apuva.")
    save_channel_configs(channel_configurations)  # Save the configurations after modifying them


@bot.command(description="Päivitä tai näytä avustajan ohje. Tämä ohje antaa suoran neuvon tai ohjeistuksen avustajalle, joka vaikuttaa sen vastauksiin.")
async def ohje(ctx, *, arg=None):
    global channel_configurations
    channel_id = ctx.channel.id
    if channel_id in channel_configurations:
        config = channel_configurations[channel_id]
        if arg is not None:
            config['assistant_message'] = arg
            await ctx.send(f"Päivitit ohjeesi: {arg}")
            print(f"Assistant message content for channel {channel_id} updated to: {arg}")
        else:
            current_message = config['assistant_message']
            await ctx.send(f"Ohjeesi: {current_message}")
            print(f"Current assistant message content for channel {channel_id}: {current_message}")
    else:
        await ctx.send("Joku meni vikaan...Apuva.")
    save_channel_configs(channel_configurations)  # Save the configurations after modifying them

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


bot.run(BOTKEY)
