import subprocess, os, random

# COMMAND UTILITY FUNCTIONS

def temp_file(name):
	return '/tmp/'+name

def run_squirrel(text):
	file = open(temp_file('code.nut'), 'w') 
	file.write(text) 
	file.close()
	return subprocess.Popen('safesq '+temp_file('code.nut'), shell=True, stdout=subprocess.PIPE).stdout.read().decode()

def bytes_from_file(name):
	try:
		file = open(temp_file(name), 'rb') 
		data = file.read(100)
		file.close()
		output = ''
		for b in data:
			output += '%.2x ' % b
		return output
	except Exception:
		return "Couldn't open output file"

def remove_file(name):
	try:
		os.remove(filename)
	except Exception:
		pass

# COMMAND HANDLERS STARTS HERE

handlers = {}

def fn_echo(arg, p):
	return {'text': arg}
handlers['echo'] = fn_echo

def fn_sq(arg, p):
	return {'text': run_squirrel(arg)}
handlers['sq'] = fn_sq

def fn_calc(arg, p):
	return {'text': run_squirrel('print(%s)' % arg)}
handlers['calc'] = fn_calc

def fn_false(arg, p):
	file = open(temp_file('code.f'), 'w') 
	file.write(arg)
	file.close()
	text = subprocess.Popen('nsfalse '+temp_file('code.f'), shell=True, stdout=subprocess.PIPE).stdout.read().decode()
	return {'text': text}
handlers['false'] = fn_false

def fn_swapcase(arg, p):
	return {'text': arg.swapcase()}
handlers['swapcase'] = fn_swapcase

def fn_titlecase(arg, p):
	return {'text': arg.title()}
handlers['titlecase'] = fn_titlecase
def fn_uppercase(arg, p):
	return {'text': arg.upper()}
handlers['uppercase'] = fn_uppercase
def fn_lowercase(arg, p):
	return {'text': arg.lower()}
handlers['lowercase'] = fn_lowercase

def fn_help(arg, p):
	return {'text': 'http://t.novasquirrel.com/sparklesbot.html'};
handlers['help'] = fn_help

def fn_random(arg, p):
	param = arg.split(' ')
	if len(param) != 2:
		return {'text': 'Syntax: random min max'}
	else:
		minimum = int(param[0])
		maximum = int(param[1])
		return {'text': str(random.randint(minimum, maximum))}
handlers['random'] = fn_random

def fn_dice(arg, p):
	param = arg.split(' ')
	if len(param) != 2:
		return {'text': 'Syntax: dice num_dice num_sides'}
	else:
		dice = int(param[0])
		sides = int(param[1])
		sum = 0
		if dice < 1 or dice > 1000:
			return {'text': 'bad number of dice'}
		if sides < 1 or sides > 1000000000:
			return {'text': 'bad number of sides'}
		for i in range(dice):
			sum += random.randint(1, sides)
		return {'text': '%dd%d = %d' % (dice, sides, sum)}
handlers['dice'] = fn_dice

def fn_choice(arg, p):
	choices = arg.split('/')
	return {'text': random.choice(choices)}
handlers['choice'] = fn_choice

def fn_shuffle(arg, p):
	choices = arg.split('/')
	random.shuffle(choices)
	return {'text': choices}
handlers['shuffle'] = fn_shuffle

def fn_me(arg, p):
	return {'text': '* %s %s *' % (p['full_name'], arg)}
handlers['me'] = fn_me

def fn_backwards(arg, p):
	return {'text': arg[::-1]}
handlers['backwards'] = fn_backwards

def fn_whoami(arg, p):
	return {'text': 'first: %s\nlast: %s\nfull: %s\nuser: %s' % (p['first_name'], p['last_name'], p['full_name'], p['username'])}
handlers['whoami'] = fn_whoami

def fn_strlen(arg, p):
	return {'text': str(len(arg))}
handlers['strlen'] = fn_strlen

def fn_strlenb(arg, p):
	return {'text': str(len(arg.encode('utf-8')))}
handlers['strlenb'] = fn_strlenb

def fn_chr(arg, p):
	result = ''
	for x in arg.split(' '):
		result += chr(int(x))
	return {'text': result}
handlers['chr'] = fn_chr

def fn_chrx(arg, p):
	result = ''
	for x in arg.split(' '):
		result += chr(int(x, 16))
	return {'text': result}
handlers['chrx'] = fn_chrx

def fn_ord(arg, p):
	result = ''
	for c in arg:
		result += str(ord(c))+" "
	return {'text': result}
handlers['ord'] = fn_ord

def fn_ordx(arg, p):
	result = ''
	for c in arg:
		result += '%x ' % ord(c)
	return {'text': result}
handlers['ordx'] = fn_ordx

def fn_test(arg, p):
	return {'text': 'test 1 2 3 4 5 6'}
handlers['test'] = fn_test

def run_command(cmd, p):
	""" Attempt to run a command with given arguments """
	cmd = cmd.lower()

	try:
		arg = p['arg']
		if cmd in handlers:
			return handlers[cmd](arg, p)

	except Exception as e:
		return {'text': 'An exception was raised: '+str(e)}
	return None
