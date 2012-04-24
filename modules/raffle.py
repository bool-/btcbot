from jsonrpc import JSONRPCException
import random

COMMANDS = { 'raffle':0 }

tickets = []

def select_winner(context, bitcoin, nick):
	global tickets
	bot = context['bot']
	commission_mul = context['raffle']['commission']
	winnings_mul = context['config']['raffle']['winnings']
	beneficiaries = context['config']['beneficiaries']
	winner = random.choice(tickets)
	balance = float(bitcoin.getbalance('raffle', 1))
	winnings = round(balance * winnings_mul, 3)
	commission = round(balance * commission_mul, 3)
	bitcoin.move('raffle', winner, winnings)
	for name, mul in beneficiaries:
		bitcoin.move('raffle', name, round(commission * mul, 3))
	bot.notice(winner, 'Congratulations, you have won ' + str(winnings) + ' BTC in the raffle!')
	bot.privmsg('##btcbot', 'Congratualtions to ' + winner + ' who has won ' + str(winnings) + ' BTC in the raffle!')
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
	config = context['raffle']
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
			balance = float(bitcoin.getbalance(nick, 1))
			price = ticket_count * ticket_price
			price = round(price, 3)
			balance = round(balance, 3)
			if price > balance:
				bot.notice(nick, 'Sorry, you don\'t have ' + str(price) + ' BTC in your balance')
				return
			bitcoin.move(nick, 'raffle', price)
			for x in range(0, ticket_count):
				tickets.append(nick)
				random.shuffle(tickets)
			bot.notice(nick, 'You have purchased ' + str(ticket_count) + ' tickets for ' + str(price) + ' BTC')
			if len(tickets) * ticket_price >= tipping_point:
				select_winner(context, bitcoin, from_[0])
	except JSONRPCException:
		bot.notice(nick, 'An error has occured communicating with bitcoind, please report this to bool_')

def usage(bot, target, command):
	if command == 'raffle':
		bot.notice(target, 'USAGE: +raffle <tickets=1>')
