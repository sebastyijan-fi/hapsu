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

openai.api_key = os.getenv("ATOKEN")
BOTKEY = os.getenv('BOTKEY')

#PERSISTENT MEMORY

import sqlite3
conn = sqlite3.connect('config.db')  # Creates a file named mydatabase.db
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS channel_configurations
             (channel_id text, system_message text, assistant_message text, previous_messages text)''')
conn.commit()

def get_channel_configurations(channel_id):
    c.execute("SELECT * FROM channel_configurations WHERE channel_id=?", (channel_id,))
    return c.fetchone()

def set_channel_configurations(channel_id, system_message, assistant_message, previous_messages):
    # Convert the previous_messages list to a string to store in SQLite
    previous_messages_str = json.dumps(previous_messages)
    data = (channel_id, system_message, assistant_message, previous_messages_str)

    # Insert a row of data
    c.execute("INSERT OR REPLACE INTO channel_configurations VALUES (?,?,?,?)", data)
    conn.commit()


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

logging.basicConfig(level=logging.INFO)

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
    for guild in bot.guilds:
        for channel in guild.channels:
            initialize_channel(channel)

@bot.event
async def on_guild_channel_create(channel):
    initialize_channel(channel)

@bot.command(description="Kysy avustajalta")
async def kysy(ctx, *, arg):
    channel_id = str(ctx.channel.id)
    config = get_channel_configurations(channel_id)
    if config is not None:
        system_message, assistant_message, previous_messages_str = config[1:]
        previous_messages = json.loads(previous_messages_str)

        # Add the user's message to the conversation
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
        set_channel_configurations(channel_id, system_message, assistant_message, previous_messages)

        # Send the assistant's response to the user
        await ctx.send(assistant_response)


@bot.command(description="Luo ja hallitse avustajan hahmoa. Voit määrittää 'järjestelmäviestin', joka ohjeistaa AI:n käyttäytymään tietyllä tavalla.")
async def hahmo(ctx, *, arg=None):
    channel_id = str(ctx.channel.id)
    config = get_channel_configurations(channel_id)
    if config is not None:
        system_message, assistant_message, previous_messages_str = config[1:]
        previous_messages = json.loads(previous_messages_str)
        if arg is not None:
            system_message = arg
            set_channel_configurations(channel_id, system_message, assistant_message, previous_messages)
            await ctx.send(f"Päivitit hahmosi: {arg}")
            print(f"System message content for channel {channel_id} updated to: {arg}")
        else:
            await ctx.send(f"Hahmosi: {system_message}")
            print(f"Current system message content for channel {channel_id}: {system_message}")
    else:
        await ctx.send("Joku meni vikaan...Apuva.")

@bot.command(description="Päivitä tai näytä avustajan ohje. Tämä ohje antaa suoran neuvon tai ohjeistuksen avustajalle, joka vaikuttaa sen vastauksiin.")
async def ohje(ctx, *, arg=None):
    channel_id = str(ctx.channel.id)
    config = get_channel_configurations(channel_id)
    if config is not None:
        system_message, assistant_message, previous_messages_str = config[1:]
        previous_messages = json.loads(previous_messages_str)
        if arg is not None:
            assistant_message = arg
            set_channel_configurations(channel_id, system_message, assistant_message, previous_messages)
            await ctx.send(f"Päivitit ohjeesi: {arg}")
            print(f"Assistant message content for channel {channel_id} updated to: {arg}")
        else:
            await ctx.send(f"Ohjeesi: {assistant_message}")
            print(f"Current assistant message content for channel {channel_id}: {assistant_message}")
    else:
        await ctx.send("Joku meni vikaan...Apuva.")


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
