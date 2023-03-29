import os, discord, requests, uuid
from discord.ui import Select
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
@bot.tree.command(name='response', description='Translate the given text to the selected language. Usage: /re [language] [text]')
async def response(interaction: discord.Interaction, *, language:str, text:str):
  await interaction.response.send_message(f"{await azureQuery(language, text)}")

# Bot command to force an update
@bot.command()
async def check(ctx):
  await bot.tree.sync()
  await ctx.send("Bot ready!")
  

@bot.command(name="prueba")
async def prueba(ctx):
    options = [
        discord.SelectOption(label="Chile", value="chile"),
        discord.SelectOption(label="Colombia", value="colombia"),
        discord.SelectOption(label="Argentina", value="argentina"),
    ]
    select = discord.ui.Select(
        placeholder="Selecciona una bandera",
        min_values=1,
        max_values=1,
        options=options
    )

    view = discord.ui.View()
    view.add_item(select)

    message = await ctx.send("Selecciona tu país", view=view)

    def check(interaction):
        return interaction.message.id == message.id and interaction.user.id == ctx.author.id

    interaction = await bot.wait_for("select_option", check=check)
    selected_option = interaction.component.selected_options[0]
    selected_country = selected_option.value

    await ctx.send(f"Eres de {selected_country.capitalize()}")

bot.run(DISCORD_TOKEN)
