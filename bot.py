import random
import discord
from discord.ext import commands
from discord.utils import get
import praw
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_corona.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Summative 2 Test").sheet1

client = commands.Bot(command_prefix = 'bot ')

reddit_id = 'FZn52ihQDcTDyw'
reddit_secret = 'ZEa-HEA9IHfDAJlqTci01oIVYnI'

client.remove_command('help')
i_dont_have_a_name = 0
counter = 1

@client.event
async def on_ready():
    print ("Bot is activated")
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Type "bot help" for help'))

@client.event
async def on_member_remove(member):
    print (member, "has left the server.")

@client.event
async def on_command_error(ctx, error):
    global i_dont_have_a_name
    if i_dont_have_a_name == 1:
        await ctx.send('That country isn\'t on the list. Type "bot countries" for a list of all countries.')
        i_dont_have_a_name = 0

@client.event
async def on_message(message):
    global counter
    if message.author.id == 733312139162288148:
        if counter == 15:
            channel = message.channel
            my_id = '<@733312139162288148>'
            typee = await channel.send(f"{my_id} your opinion is not needed.")
            time.sleep(2)
            await typee.delete()
            counter = 1
            await client.process_commands(message)
        else:
            counter += 1
            await client.process_commands(message)
    else:
        await client.process_commands(message)

@client.command()
async def countries(ctx):
    embed=discord.Embed(title='Countries for the "bot covid (country)" command')
    embed.add_field(name="--------------------------------------------------------------------------------------------------", value="Afghanistan, Albania, Algeria, Angola, Antigua and Barbuda, Argentina, Armenia, Aruba, Australia, Austria, Azerbaijan, Bahamas, Bahrain, Bangladesh, Barbados, Belarus, Belgium, Belize, Benin, Bhutan, Bolivia, Bosnia-herzegovina, Botswana, Brazil, Brunei, Bulgaria, Burkina Faso, Burundi, Cabo Verde, Cambodia, Cameroon, Canada, Central African Republic, Chad, Channel Islands, Chile, China, Hong Kong, Macau, Taiwan, Colombia, Comoros, Congo, Costa Rica, Cote D'ivoire, Croatia, Cuba, Curacao, Cyprus, Czech Republic, Dpr Korea, Dr Congo, Denmark, Djibouti, Dominican Republic, Ecuador, Egypt, El Salvador", inline=False)
    embed.add_field(name="--------------------------------------------------------------------------------------------------", value="Equatorial Guinea, Eritrea, Estonia, Eswatini, Ethiopia, Fiji, Finland, France, French Guiana, French Polynesia, Gabon, Gambia, Georgia, Germany, Ghana, Greece, Grenada, Guadeloupe, Guam, Guatemala, Guinea, Guinea-bissau, Guyana, Haiti, Honduras, Hungary, Iceland, India, Indonesia, Iran, Iraq, Ireland, Israel, Italy, Jamaica, Japan, Jordan, Kazakhstan, Kenya, Kiribati, Kuwait, Kyrgyzstan, Laos, Latvia, Lebanon, Lesotho, Liberia, Libya, Lithuania, Luxembourg, Madagascar",inline = False)
    embed.add_field(name="--------------------------------------------------------------------------------------------------", value="Malawi, Malaysia, Maldives, Mali, Malta, Martinique, Mauritania, Mauritius, Mayotte, Mexico, Micronesia (Fed. States of), Mongolia, Montenegro, Morocco, Mozambique, Myanmar, Namibia, Nepal, Netherlands, New Caledonia, New Zealand, Nicaragua, Niger, Nigeria, N. Macedonia, Norway, Oman, Pakistan, Panama, Papua New Guinea, Paraguay, Peru, Philippines, Poland, Portugal, Puerto Rico, Qatar, S. Korea, Moldova, Reunion, Romania, Russia, Rwanda, Saint Lucia, Saint Vincent, Samoa, Sao Tome and Principe, Saudi Arabia, Senegal, Serbia, Seychelles, Sierra Leone, Singapore, Slovakia, Slovenia, Solomon Islands, Somalia",inline=False)
    embed.add_field(name="--------------------------------------------------------------------------------------------------", value="S. Africa, S. Sudan, Spain, Sri Lanka, Palestine, Sudan, Suriname, Sweden, Switzerland, Syria, Tajikistan, Thailand, Timor-leste, Togo, Tonga, Trinidad and Tobago, Tunisia, Turkey, Turkmenistan, Uganda, Ukraine, Uae, United Kingdom, Tanzania, United States, Us Virgin Islands, Uruguay, Uzbekistan, Vanuatu, Venezuela, Vietnam, Western Sahara, Yemen, Zambia, Zimbabwe, San Marino, Monaco, Andorra, Liechtenstein, Faeroe Islands, Gibraltar, Vatican City, Saint Barthelemy, Saint Martin, Cayman Island, Kosovo, Greenland, Montserrat, Sint Maarten, Bermuda, Isle of Man, Dominica, Turks and Caicos, British Virgin Islands, St.kitts and Nevis, Anguilla, Northern Mariana Islands, Falkland Islands, Caribbean Netherlands, Saint Pierre Miquelon", inline=False)
    await ctx.channel.send(embed=embed)

@client.command()
async def help(ctx):
    embed=discord.Embed(title="Botsanaro Commands", color=0x00ff00)
    embed.add_field(name="bot ping", value="Find out how shit ur Internet is", inline=True)
    embed.add_field(name="bot pledge", value = "Pledge allegiance to America", inline = True)
    embed.add_field(name="bot clear (number)", value="max 15 messages", inline=True)
    embed.add_field(name="bot covid (country)", value="Find COVID-19 info on a country", inline=True)
    embed.add_field(name="bot countries", value="List of all countries for the COVID command", inline=True)
    embed.add_field(name="bot annoy (user)", value="Ghost ping someone 5 times and remove their Verified role", inline=True)
    await ctx.channel.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency*1000)} ms')
    if round(client.latency*1000) > 100:
        await ctx.send('Ur internet is shit. Stop using Rogers!')
    elif round(client.latency*1000) < 55:
        await ctx.send("U got hella fast internet.")
    else:
        await ctx.send("Nice internet!")

@client.command()
async def pledge(ctx):
    await ctx.send(f"{ctx.author.mention} pledges allegiance to the Flag of the United States of America, and to the Republic for which it stands, one Nation under God, indivisible, with liberty and justice for all.", file=discord.File('obama.jpg'))


@client.command()
async def clear(ctx, amount=1):
    if amount > 15:
        amount = 15
    await ctx.channel.purge(limit=amount+1)
    message = await ctx.send("Deleted " + str(amount) + " messages!")
    time.sleep(2.5)
    await message.delete()

@client.command()
async def covid(ctx, *, country='null'):
    if country == 'null':
        await ctx.send('Please use the format "bot covid (country)"\nFor example: bot covid brazil\nFor a list of all countries, type "bot countries"')
    else:
        global i_dont_have_a_name
        i_dont_have_a_name = 1
        cell = sheet.find(country.upper())
        if country.upper() in sheet.col_values(3):
            val1 = (format(int(sheet.cell(cell.row, (cell.col+1)).value), ',d'))
            val2 = (format(int(sheet.cell(cell.row, (cell.col+2)).value), ',d'))
            val3 = (format(int(sheet.cell(cell.row, (cell.col+3)).value), ',d'))
            await ctx.send("The number of COVID-19 cases in " + country.title() + " is " + val1 + "\nThe number of COVID-19 deaths in " + country.title() + " is " + val2 + "\nThe number of COVID-19 recoveries in " + country.title() + " is " + val3)
            i_dont_have_a_name = 0

@client.command()
async def annoy(ctx, member: discord.Member ):
    for i in range (5):
        annoying = await ctx.send(f"{member.mention} I'm hear to annoy u")
        time.sleep(0.5)
        await annoying.delete()
    verified_role = get(member.guild.roles, name='Verified')
    await member.remove_roles(verified_role)

client.run('NzMxMjQ3MDk3NTUwMjA5MTM5.XwjRKw.Q0xWTO2kGlUszA_dmgR1cSBeMhU')
