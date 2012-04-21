from jsonrpc import JSONRPCException
import random

COMMANDS = { 'roulette':1 }
WAGER = 0.1

def is_int(val):
	try:
		int(val)
	except ValueError:
		return False
	return True

def roulette(chamber):
	chamber_fired = random.randint(1,6)
	if chamber_fired == chamber:
		return True
	return False

def do_command(bot, bitcoin, from_, target, command, args):
	nick = from_[0]
	try:
		if command == 'roulette':
			if not is_int(args[0]):
				bot.notice(nick, 'Please enter a valid chamber number')
				return
			chamber = int(args[0])
			if chamber < 1 or chamber > 6:
				bot.notice(nick, 'Please enter a valid chamber number 1-6')
				return
			balance = bitcoin.jsonrpc.getbalance(nick, 1)
			if WAGER > balance:
				bot.notice(nick, 'Sorry, you don\'t have ' + str(WAGER) + ' BTC in your balance')
				return
			bitcoin.jsonrpc.move(nick, 'roulette', WAGER)
			if roulette(chamber):
				roulette_bal = float(bitcoin.jsonrpc.getbalance('roulette', 1))
				roulette_bal = round(roulette_bal * 0.85, 3)
				bitcoin.jsonrpc.move('roulette', nick, roulette_bal)
				bot.notice(nick, 'The gun went *CLICK* and you won ' + str(roulette_bal) + ' BTC.')
				bot.privmsg('##btcbot', nick + '\'s gun went *CLICK*, winning them ' + str(roulette_bal) + ' BTC.')
			else:
				bot.notice(nick, 'The gun went *BANG* and you lost ' + str(WAGER) + ' BTC.')

	except JSONRPCException:
		bot.notice(nick, 'An error has occured communicating with bitcoind, please report this to bool_')


def usage(bot, target, command):
	if command == 'roulette':
		bot.notice(target, 'USAGE: +roulette <chamber>')
