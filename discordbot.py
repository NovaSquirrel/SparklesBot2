import discord, asyncio, json
from botconfig import *

prefix = "bot."

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	if message.content.startswith(prefix):
		text = message.content[len(prefix):]

		# extract information from the text
		command = text
		arg = ''
		find_space = text.find(' ')
		# split command into command and argument
		if find_space >= 0:
			command = text[0:find_space]
			arg = text[find_space+1:]

		parameters = {'command': command, 'arg': arg}
		out = requests.post(config_base_url+config_path_generic, data=json.dumps(parameters)).json()
		
		await client.send_message(message.channel, out['text'])

client.run(config_discord_key)
