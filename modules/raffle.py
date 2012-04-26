from jsonrpc import JSONRPCException
import random
import bitcoinutil as btc

COMMANDS = { 'raffle':0 }
PERMISSIONS = []

tickets = []

def select_winner(context, bitcoin, nick):
	global tickets
	bot = context['bot']
	commission_mul = context['config']['raffle']['commission']
	winnings_mul = context['config']['raffle']['winnings']
	beneficiaries = context['config']['beneficiaries']
	winner = random.choice(tickets)
	balance = btc.getbalance(bitcoin, 'raffle')
	winnings = balance * winnings_mul
	commission = balance * commission_mul
	bitcoin.move('raffle', winner, btc.to_float(winnings))
	for name, mul in beneficiaries.items():
		bitcoin.move('raffle', name, btc.to_float(commission * mul))
	bot.notice(winner, 'Congratulations, you have won ' + btc.to_string(winnings) + ' BTC in the raffle!')
	bot.privmsg('##btcbot', 'Congratualtions to ' + winner + ' who has won ' + btc.to_string(winnings) + ' BTC in the raffle!')
	tickets = []

def is_int(val):
	try:
		int(val)
	except ValueError:
		return False
	return True

def do_command(context, from_, target, command, args):
	nick = from_[0].lower()
	bot = context['bot']
	bitcoin = context['bitcoin']
	config = context['config']['raffle']
	ticket_price = config['ticket_price']
	tipping_point = config['tipping_point']
	try:
		if command == 'raffle':
			ticket_count = 1
			if len(args) > 0:
				if not is_int(args[0]):
					bot.notice(nick, 'Please enter a valid ticket count')
					return
				ticket_count = int(args[0])
			balance = btc.getbalance(bitcoin, nick)
			price = ticket_count * ticket_price
			price = btc.to_btc(price)
			if price > balance:
				bot.notice(nick, 'Sorry, you don\'t have ' + btc.to_string(price) + ' BTC in your balance')
				return
			bitcoin.move(nick, 'raffle', btc.to_float(price))
			for x in range(0, ticket_count):
				tickets.append(nick)
				random.shuffle(tickets)
			bot.notice(nick, 'You have purchased ' + str(ticket_count) + ' tickets for ' + btc.to_string(price) + ' BTC')
			if len(tickets) >= tipping_point:
				select_winner(context, bitcoin, from_[0])
	except JSONRPCException:
		bot.notice(nick, 'An error has occured communicating with bitcoind, please report this to bool_')

def usage(bot, target, command):
	if command == 'raffle':
		bot.notice(target, 'USAGE: +raffle <tickets=1>')
