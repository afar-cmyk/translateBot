import os, discord, requests, uuid
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Enviroment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
AZURE_KEY = os.getenv('AZURE_KEY')
AZURE_ENDPOINT = os.getenv('AZURE_ENDPOINT')
AZURE_LOCATION = os.getenv("AZURE_LOCATION")

# Default language
defaultLang = 'es' 

# Discord bot settings
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

# Query function to Azure servers
async def azureQuery(language:str, text:str):
  constructed_url = AZURE_ENDPOINT + '/translate'
  
  params = {
    'api-version': '3.0',
    'to': language
    }

  headers = {
      'Ocp-Apim-Subscription-Key': AZURE_KEY,
      'Ocp-Apim-Subscription-Region': AZURE_LOCATION,
      'Content-type': 'application/json',
      'X-ClientTraceId': str(uuid.uuid4())
    }

  body = [{'text':text}]
  
  request = requests.post(constructed_url, params=params, headers=headers, json=body)
  response = request.json()
  
  translated_text = response[0]['translations'][0]['text']
  
  return translated_text

# Console message on successful connection
@bot.event
async def on_ready():
    print(f'{bot.user.name} se ha conectado a Discord!')
    
# Bot command to translate from any language to spanish
@bot.tree.command(name='translate', description='Translates the given text to Spanish. Usage: /tr[text]')
async def translate(interaction: discord.Interaction, *, text:str):
  await interaction.response.send_message(f"{await azureQuery(defaultLang, text)}")
  
# Bot command to translate text from any language to a given language
@bot.tree.command(name='response', description='Translate the given text to the given language. Usage: /re [language] [text]')
async def response(interaction: discord.Interaction, *, language:str, text:str):
  await interaction.response.send_message(f"{await azureQuery(language, text)}")

# Bot command to force an update
@bot.command()
async def forceSync(ctx):
  await bot.tree.sync()
  await ctx.send("Bot ready!")

bot.run(DISCORD_TOKEN)
