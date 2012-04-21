from jsonrpc import JSONRPCException

COMMANDS = { 'deposit':0, 'balance':0, 'withdraw':1 }


def is_float(val):
	try:
		float(val)
	except ValueError:
		return False
	return True

def do_command(bot, bitcoin, from_, target, command, args):
	nick = from_[0]
	try:
		if command == 'deposit':
			address = bitcoin.jsonrpc.getaccountaddress(nick)
			bot.notice(nick, 'Your deposit address is: ' + address)

		if command == 'balance':
			balance = float(bitcoin.jsonrpc.getbalance(nick, 1))
			bot.notice(nick, 'Your current balance is: ' + str(balance))
		if command == 'withdraw':
			address = args[0]
			valid = bitcoin.jsonrpc.validateaddress(address)['isvalid']
			if not valid:
				bot.notice(nick, 'Please enter a valid bitcoin address')
				return
			balance = float(bitcoin.jsonrpc.getbalance(nick, 1))
			amount = balance
			if len(args) == 2:
				if not is_float(args[1]):
					bot.notice(nick, 'Please enter a valid amount')
					return
				amount = float(args[1])
				if amount > balance:
					bot.notice(nick, 'You can\'t withdraw more than ' + str(balance) + ' BTC')
					return

			tx_id = bitcoin.jsonrpc.sendfrom(nick, address, amount)
			bot.notice(nick, 'Sent ' + str(amount) + ' BTC to ' + address + ', transaction: ' + tx_id)
			balance = float(bitcoin.jsonrpc.getbalance(nick, 1))
			if balance < 0: # take care of any tax that was applied
				bitcoin.jsonrpc.move('buffer', nick, abs(balance))
	except JSONRPCException:
		bot.notice(nick, 'An error has occured communicating with bitcoind, please report this to bool_')

def usage(bot, target, command):
	if command == 'deposit':
		bot.notice(target, 'USAGE: +deposit')
	elif command == 'balance':
		bot.notice(target, 'USAGE: +balance')
	elif command == 'withdraw':
		bot.notice(target, 'USAGE: +withdraw <address>')
