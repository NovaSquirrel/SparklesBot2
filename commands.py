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
aliases = {}

def fn_echo(arg, p):
	return {'text': arg}
handlers['echo'] = fn_echo

def fn_sq(arg, p):
	return {'text': run_squirrel(arg)}
handlers['sq'] = fn_sq
aliases['squirrel'] = 'sq'

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
aliases['choices'] = 'choice'
aliases['choose'] = 'choice'

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

def fn_datediff(arg, p):
	two_dates = arg.split(' ')
	if len(two_dates) != 2:
		return {'text': 'Provide two dates to get a difference of, in M/D/Y format, or "now" for the current day'}
	d1 = date_from_string(two_dates[0])
	d2 = date_from_string(two_dates[1])
	difference = abs((d2 - d1).days)
	return {'text': '%d days (%d weeks %d days)' % (difference, difference/7, difference%7)}
handlers['datediff'] = fn_datediff

def fn_dateplus(arg, p):
	split = arg.split(' ')
	if len(split) != 2:
		return {'text': 'Provide a date in M/D/Y format and a number of days to add'}
	the_date = date_from_string(split[0]) + timedelta(days=int(split[1]))
	return {'text': the_date.strftime("%m/%d/%Y is a %A")}
handlers['dateplus'] = fn_dateplus

def fn_dayofweek(arg, p):
	the_date = date_from_string(arg)
	return {'text': the_date.strftime("%m/%d/%Y is a %A")}
handlers['dayofweek'] = fn_dayofweek

def fn_curtime(arg, p):
	return {'text': datetime.today().strftime("Now it's %m/%d/%Y, %I:%M %p")}
handlers['curtime'] = fn_curtime

def fn_gbaddr(arg, p):
	split = arg.split(':')
	if len(split) == 2:
		hex1 = int(split[0], 16)
		hex2 = int(split[1], 16)
		return {'text': '0x%x' % (hex1 * 0x4000 + hex2 - 0x4000)}
	else:
		hex = int(arg, 16)
		return {'text': '%x:%x' % (hex // 0x4000, 0x4000 + (hex % 0x4000))}
handlers['gbaddr'] = fn_gbaddr
aliases['gabddr'] = 'gbaddr'
aliases['gbadr']  = 'gbaddr'
aliases['gbadrd'] = 'gbaddr'
aliases['gbdadr'] = 'gbaddr'

def fn_nesgenie(arg, p):
	if len(arg) == 0:
		return {'text': 'Please give one of the following:\n6 or 8 character Game Genie code\nAAAA DD, where A=address, D=data (in hex)\nAAAA DD CC, where A=address, D=data C=compare\n'}
	arg = arg.upper()
	key = 'APZLGITYEOXUKSVN'

	split = arg.split(' ')
	if len(split) == 1:   # decode
		for c in arg:
			if key.find(c) == -1:
				return {'text': '"%s" is an invalid NES Game Genie character, use APZLGITYEOXUKSVN' % c}
		if len(arg) != 6 and len(arg) != 8:
			return {'text': 'NES Game Genie codes must be 6 or 8 characters long'}

		# start decoding
		n = []
		for c in arg:
			n.append(key.find(c))
		address = 0x8000 + (((n[3] & 7) << 12) | ((n[5] & 7) << 8) | ((n[4] & 8) << 8) \
			| ((n[2] & 7) << 4) | ((n[1] & 8) << 4) | (n[4] & 7) | (n[3] & 8));

		if len(arg) == 6:
			data = ((n[1] & 7) << 4) | ((n[0] & 8) << 4) | (n[0] & 7) | (n[5] & 8);
			return {'text': '%s is %.4X %.2x' % (arg, address, data)}
		else:
			data = ((n[1] & 7) << 4) | ((n[0] & 8) << 4) | (n[0] & 7) | (n[7] & 8);
			compare = ((n[7] & 7) << 4) | ((n[6] & 8) << 4) | (n[6] & 7) | (n[5] & 8);
			return {'text': '%s is %.4X %.2X (compare %.2X)' % (arg, address, data, compare)}
	elif len(split) == 2: # encode without compare
		addr   = int(split[0],16)
		data   = int(split[1],16)
		output = ''
		output += key[(data>>4 & 8) | (data & 7)];
		output += key[(addr>>4 & 8) | (data>>4 & 7)];
		output += key[0 | (addr>>4 & 7)];
		output += key[(addr & 8) | (addr>>12 & 7)];
		output += key[(addr>>8 & 8) | (addr & 7)];
		output += key[(data & 8) | (addr>>8 & 7)];
		return {'text': '%.4X %.2X = %s' % (addr, data, output)}
	elif len(split) == 3: # encode with compare
		addr    = int(split[0],16)
		data    = int(split[1],16)
		compare = int(split[2],16)
		output = ''
		output += key[(data>>4 & 8) | (data & 7)];
		output += key[(addr>>4 & 8) | (data>>4 & 7)];
		output += key[8 | (addr>>4 & 7)];
		output += key[(addr & 8) | (addr>>12 & 7)];
		output += key[(addr>>8 & 8) | (addr & 7)];
		output += key[(compare & 8) | (addr>>8 & 7)];
		output += key[(compare>>4 & 8) | (compare & 7)];
		output += key[(data & 8) | (compare>>4 & 7)];
		return {'text': '%.4X %.2X %.2X = %s' % (addr, data, compare, output)}

	return {'text': 'test'}
handlers['nesgenie'] = fn_nesgenie

def run_command(cmd, p):
	""" Attempt to run a command with given arguments """
	cmd = cmd.lower()

	try:
		arg = p['arg']
		if cmd in aliases:
			cmd = aliases[cmd]
		if cmd in handlers:
			return handlers[cmd](arg, p)

	except Exception as e:
		return {'text': 'An exception was raised: '+str(e)}
	return None
