from jsonrpc import JSONRPCException
import random

COMMANDS = { 'raffle':0 }
TIPPING_POINT = 0.04
TICKET_PRICE = 0.01
COMMISSION_ACCOUNT = 'bool_'

tickets = []

def select_winner(bot, bitcoin, nick):
	global tickets
	winner = random.choice(tickets)
	balance = float(bitcoin.getbalance('raffle', 1))
	winnings = round(balance * 0.75, 3)
	commission = round(balance * 0.1, 3)
	bitcoin.move('raffle', winner, winnings)
	bitcoin.move('raffle', COMMISSION_ACCOUNT, commission)
	bot.notice(winner, 'Congratulations, you have won ' + str(winnings) + ' BTC in the raffle!')
	bot.privmsg('##btcbot', 'Congratualtions to ' + winner + ' who has won ' + str(winnings) + ' BTC in the raffle!')
	tickets = []

def is_int(val):
	try:
		int(val)
	except ValueError:
		return False
	return True

def do_command(bot, bitcoin, from_, target, command, args):
	nick = from_[0].lower()
	try:
		if command == 'raffle':
			ticket_count = 1
			if len(args) > 0:
				if not is_int(args[0]):
					bot.notice(nick, 'Please enter a valid ticket count')
					return
				ticket_count = int(args[0])
			balance = float(bitcoin.getbalance(nick, 1))
			price = ticket_count * TICKET_PRICE
			if price > balance:
				bot.notice(nick, 'Sorry, you don\'t have ' + str(price) + ' BTC in your balance')
				return
			bitcoin.move(nick, 'raffle', price)
			for x in range(0, ticket_count):
				tickets.append(nick)
				random.shuffle(tickets)
			bot.notice(nick, 'You have purchased ' + str(ticket_count) + ' tickets for ' + str(price) + ' BTC')
			if len(tickets) * TICKET_PRICE >= TIPPING_POINT:
				select_winner(bot, bitcoin, from_[0])
	except JSONRPCException:
		bot.notice(nick, 'An error has occured communicating with bitcoind, please report this to bool_')

def usage(bot, target, command):
	if command == 'raffle':
		bot.notice(target, 'USAGE: +raffle <tickets=1>')
