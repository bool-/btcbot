from jsonrpc import ServiceProxy
import imp

def load_modules(modules_):
	global modules
	modules = []
	for module in modules_:
		imp_module = __import__(module, globals(), locals(), [module.split('.')[1]], -1)
		modules.append(imp_module)
		print('Loaded module: ' + imp_module.__name__)

def connect_bitcoind(user, password, host, port):
	global bitcoin
	bitcoin = ServiceProxy('http://' + user + ':' + password + '@' + host + ':' + str(port) + '/')

def parse_command(bot, config, from_, target, message):
	nick = from_[0]
	message_tokens = message.split()
	command = message_tokens[0]
	args = message_tokens[1:]
	context = {
			'bot': bot,
			'bitcoin': bitcoin,
			'config': config,
			'modules': modules
			}

	if command == 'ident':
		if nick in bot.identified_users:
			bot.notice(nick, 'You\'re already identified with the bot')
		elif is_identified(bot, nick):
			bot.identified_users.append(nick)
			bot.notice(nick, 'You\'re now identified with the bot')
		else:
			bot.notice(nick, 'You must be identified with NickServ to use this bot')
	elif nick not in bot.identified_users:
		bot.notice(nick, 'You must identify by using the command +ident before you can use the bot')
		return
	
	for module in modules:
		if command in module.COMMANDS:
			if len(module.PERMISSIONS) >  0:
				if nick not in config['operators']:
					continue
				permissions = config['operators'][nick]
				for required in module.PERMISSIONS:
					if required not in permissions:
						continue
			# check for minimum command arity
			if len(args) < module.COMMANDS[command]:
				module.usage(bot, nick, command)
			else:
				try:
					module.do_command(context, from_, target, command, args)
				except Exception as ex:
					bot.notice(nick, 'An error has occured that prevented the module from working properly')


def is_identified(bot, nick):
	data = bot.whois(nick)

	if 'ETC' in data:
		for line in data['ETC']:
			if 'is logged in' in line:
				return True
	return False
	
