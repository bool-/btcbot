from jsonrpc import JSONRPCException

COMMANDS = { 'ubalance':1 }
PRIVILEGES = 2

def do_command(context, from_, target, command, args):
	nick = from_[0].lower()
	bot = context['bot']
	bitcoin= context['bitcoin']
	try:
		if command == 'ubalance':
			balance = float(bitcoin.getbalance(args[0], 1))
			bot.notice(nick, args[0] +'\'s current balance is: ' + str(balance))
	except JSONRPCException:
		bot.notice(nick, 'An error has occured commincating with bitcoind, please report this to bool_')

def usage(bot, target, command):
	if command == 'ubalance':
		bot.notice(target, 'USAGE: +ubalance <account>')
