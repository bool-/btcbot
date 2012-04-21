from modules import bitcoin
from jsonrpc import ServiceProxy
import imp

# TODO figure out a way to load this dynamically
MODULES = [ bitcoin ]


# TODO relocate this code and add functions to help with bitcoin distribution
class BitcoinHelper():
	def __init__(self):
		self.jsonrpc = ServiceProxy('http://btcbot:password@127.0.0.1:8332')

bitcoin = BitcoinHelper()

def parse_command(bot, from_, target, message):
	nick = from_[0]
	message_tokens = message.split()
	command = message_tokens[0]
	args = message_tokens[1:]

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
	elif nick in bot.identified_users and nick == 'bool_':
		if command == 'reload':
			for module in MODULES:
				imp.reload(module)
				bot.notice(nick, str(module) + ' reloaded')
	for module in MODULES:
		if command in module.COMMANDS:
			module.do_command(bot, bitcoin, from_, target, command, args)


def is_identified(bot, nick):
	data = bot.whois(nick)

	if 'ETC' in data:
		for line in data['ETC']:
			if 'is logged in' in line:
				return True
	return False
	
