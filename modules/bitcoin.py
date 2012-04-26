from jsonrpc import JSONRPCException
import urllib.request
import bitcoinutil as btc

COMMANDS = { 'deposit':0, 'balance':0, 'withdraw':1 }
PERMISSIONS = []

def is_float(val):
	try:
		float(val)
	except ValueError:
		return False
	return True

def resolve_firstbits(address):
	try:
		response = urllib.request.urlopen('http://blockchain.info/q/resolvefirstbits/' + address)
		address = response.read()
		address = address.decode('utf-8')
		if len(address) < 31:
			return None
		return address
	except urllib.error.URLError as e:
		return None

def do_command(context, from_, target, command, args):
	nick = from_[0]
	nick = nick.lower()
	bot = context['bot']
	bitcoin = context['bitcoin']
	try:
		if command == 'deposit':
			address = bitcoin.getaccountaddress(nick)
			bot.notice(nick, 'Your deposit address is: ' + address)
		if command == 'balance':
			balance = btc.getbalance(bitcoin, nick)
			bot.notice(nick, 'Your current balance is: ' + btc.to_string(balance))
		if command == 'withdraw':
			address = args[0]
			if len(address) < 31:
				new_address = resolve_firstbits(address)
				if new_address == None:
					bot.notify(nick, 'Sorry, that firstbits address could not be resolved, please use a bitcoin address')
					return
				address = new_address
			else:
				valid = bitcoin.validateaddress(address)['isvalid']
				if not valid:
					bot.notice(nick, 'Please enter a valid bitcoin address')
					return
			balance = btc.getbalance(bitcoin, nick)
			amount = balance
			if len(args) == 2:
				if not is_float(args[1]):
					bot.notice(nick, 'Please enter a valid amount')
					return
				amount = btc.to_btc(float(args[1]))
				if balance == 0:
					bot.notice(nick, 'You don\'t have any BTC to withdraw')
					return
				if amount > balance:
					bot.notice(nick, 'You can\'t withdraw more than ' + btc.to_string(balance) + ' BTC')
					return

			tx_id = bitcoin.sendfrom(nick, address, btc.to_float(amount))
			bot.notice(nick, 'Sent ' + btc.to_string(amount) + ' BTC to ' + address + ', transaction: ' + tx_id)
			balance = btc.getbalance(bitcoin, nick)
			if balance < 0: # take care of any tax that was applied
				bitcoin.move('buffer', nick, btc.to_float(abs(balance)))
	except JSONRPCException as ex:
		if ex.error['code'] == -4:
			bot.notice(nick, 'This transaction requires a fee of 0.0005, please subtract this from your withdrawl amount')
		bot.notice(nick, 'An error has occured communicating with bitcoind, please report this to bool_')

def usage(bot, target, command):
	if command == 'deposit':
		bot.notice(target, 'USAGE: +deposit')
	elif command == 'balance':
		bot.notice(target, 'USAGE: +balance')
	elif command == 'withdraw':
		bot.notice(target, 'USAGE: +withdraw <address>')
