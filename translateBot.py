import os
import discord
import requests, uuid
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} se ha conectado a Discord!')

@bot.tree.command(name='translate', description='Translates the given text to Spanish. Usage: /translate [text]')
async def translate(interaction: discord.Interaction, *, text:str):
    api_key = os.getenv('AZURE_KEY')
    endpoint = os.getenv('AZURE_ENDPOINT')
    location = os.getenv("AZURE_LOCATION")

    path = '/translate'
    constructed_url = endpoint + path
    
    params = {
    'api-version': '3.0',
    'to': ['es']
    }

    headers = {
      'Ocp-Apim-Subscription-Key': api_key,
      'Ocp-Apim-Subscription-Region': location,
      'Content-type': 'application/json',
      'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{        'text': text    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    
    translated_text = response[0]['translations'][0]['text']
    await interaction.response.send_message(f"{translated_text}")
  
@bot.command()
async def syncronize(ctx):
  await bot.tree.sync()
  await ctx.send("Listo!")

bot.run(TOKEN)
