from jsonrpc import JSONRPCException
import bitcoinutil as btc

COMMANDS = { 'ubalance':1 }
PERMISSIONS = [ 'btcadmin' ]

def do_command(context, from_, target, command, args):
	nick = from_[0].lower()
	bot = context['bot']
	bitcoin = context['bitcoin']
	try:
		if command == 'ubalance':
			balance = btc.getbalance(bitcoin, args[0])
			bot.notice(nick, args[0] +'\'s current balance is: ' + btc.to_string(balance))
	except JSONRPCException:
		bot.notice(nick, 'An error has occured commincating with bitcoind, please report this to bool_')

def usage(bot, target, command):
	if command == 'ubalance':
		bot.notice(target, 'USAGE: +ubalance <account>')
