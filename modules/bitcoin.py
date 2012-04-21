

COMMANDS = ['deposit', 'balance']

def do_command(bot, bitcoin, from_, target, command, args):
	nick = from_[0]
	try:
		if command == 'deposit':
			address = bitcoin.jsonrpc.getaccountaddress(nick)
			bot.notice(nick, 'Your deposit address is: ' + address)

		if command == 'balance':
			balance = float(bitcoin.jsonrpc.getbalance(nick, 1))
			bot.notice(nick, 'Your current balance is: ' + str(balance))
	except JSONRPCException:
		bot.notice(nick, 'An error has occured communicating with bitcoind, please report this to bool_')
