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
		if message.author.bot:
			return

		text = message.content[len(prefix):]

		# extract information from the text
		command = text
		arg = ''
		find_space = text.find(' ')
		find_newline = text.find('\n')
		if find_space >= 0 or find_newline >= 0:
			split_index = min(find_space, find_newline)
			if find_space == -1:
				split_index = find_newline
			if find_newline == -1:
				split_index = find_space
			command = text[0:split_index]
			arg = text[split_index+1:]

		parameters = {'command': command, 'arg': arg, 'first_name': message.author.display_name, 'username': message.author.id}
		out = requests.post(config_base_url+config_path_generic, data=json.dumps(parameters)).json()
		
		await client.send_message(message.channel, out['text'])

client.run(config_discord_key)
