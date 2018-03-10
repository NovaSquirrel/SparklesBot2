import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import telegram_api
from commands import run_command
from botconfig import *

class RequestHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		# Get the post data
		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length) # read post body
		post_data = bytes.decode(post_data)         # convert to text
		post_data = json.loads(post_data)           # convert to dictionary

		# Default message to send back
		message = {'ok': True}

		# Process the response
		if self.path == config_path_telegram:
			if ('edited_message' in post_data):
				post_data['message'] = post_data['edited_message']
			if ('message' in post_data) and ('text' in post_data['message']):
				message = post_data['message']
				chat_id = message['chat']['id']
				text = message['text']

				# extract sender information
				username = '?'
				first_name = '?'
				last_name = '?'
				full_name = '?'
				if 'from' in message:
					message_from = message['from']
					if 'first_name' in message_from:
						first_name = message_from['first_name']
						full_name = first_name
					if 'last_name' in message_from:
						last_name = message_from['last_name']
						full_name += ' '+last_name
					if 'username' in message_from:
						username = message_from['username']
					else:
						username = first_name

				# extract information from the text
				command = text[1:]
				arg = ''
				find_space = text.find(' ')
				# split command into command and argument
				if find_space >= 0:
					command = text[1:find_space]
					arg = text[find_space+1:]
				# trim /command@bot down to /command
				find_at = command.find('@')
				if find_at >= 0:
					command = command[0:find_at]

				# run the command
				params = {'arg': arg, 'username': username, 'first_name': first_name, 'last_name': last_name, 'full_name': full_name}
				result = run_command(command, params)
				if result != None:
					message = {'method': 'sendMessage', 'disable_web_page_preview': True, 'chat_id': chat_id, 'text': result['text']}
		elif self.path == config_path_generic:
			if ('command' in post_data) and ('arg' in post_data):
				first_name = '?'
				last_name = '?'
				username = '?'
				full_name = '?'
				if 'first_name' in post_data:
					first_name = post_data['first_name']
					full_name = first_name
				if 'last_name' in post_data:
					last_name = post_data['last_name']
					full_name += ' '+last_name
				if 'username' in post_data:
					username = post_data['username']

				# run the command
				params = {'arg': post_data['arg'], 'username': username, 'first_name': first_name, 'last_name': last_name, 'full_name': full_name}
				result = run_command(post_data['command'], params)
				if result != None:
					message = {'text': result['text']}
		else:
			print("Unrecognized path: "+self.path)

		# Set response code and headers
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()

		# Send the response
		self.wfile.write(bytes(json.dumps(message), "utf8"))
		return

	def do_GET(self):
		# Set response code and headers
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
 
		message = "Hello World!"

		# Send the response
		self.wfile.write(bytes(message, "utf8"))
		return

def run():
	print('starting server...')
	httpd = HTTPServer(('', config_port), RequestHandler)
	print('running server...')
	httpd.serve_forever()

telegram_api('setWebHook', {'url': config_base_url+config_path_telegram', 'max_connections': 10})
 
run()
