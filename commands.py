from jsonrpc import ServiceProxy
import imp

context = { }

def load_modules(modules):
	global MODULES
	MODULES = []
	for module in modules:
		imp_module = __import__(module, globals(), locals(), [module.split('.')[1]], -1)
		MODULES.append(imp_module)

def connect_bitcoind(user, password, host, port):
	global bitcoin
	bitcoin = ServiceProxy('http://' + user + ':' + password + '@' + host + ':' + str(port) + '/')

def parse_command(bot, config, from_, target, message):
	nick = from_[0]
	message_tokens = message.split()
	command = message_tokens[0]
	args = message_tokens[1:]
	context['bot'] = bot
	context['bitcoin'] = bitcoin
	context['config'] = config

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

	# TODO better way to handle bot operators
	if nick in config['operators']:
		if command == 'reload':
			for module in MODULES:
				imp.reload(module)
				bot.notice(nick, module.__name__ + ' reloaded')
	
	for module in MODULES:
		if command in module.COMMANDS:
			if module.NEEDS_OP:
				if nick not in config['operators']:
					return
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
	
