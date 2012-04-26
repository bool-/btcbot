from jsonrpc import JSONRPCException
from decimal import *
import random
import bitcoinutil as btc

COMMANDS = { 'roulette':1 }
PERMISSIONS = []

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

def do_command(context, from_, target, command, args):
	nick = from_[0]
	nick = nick.lower()
	bot = context['bot']
	bitcoin = context['bitcoin']
	config = context['config']['roulette']
	wager = config['wager']
	winnings = config['winnings']
	try:
		if command == 'roulette':
			if not is_int(args[0]):
				bot.notice(nick, 'Please enter a valid chamber number')
				return
			chamber = int(args[0])
			if chamber < 1 or chamber > 6:
				bot.notice(nick, 'Please enter a valid chamber number 1-6')
				return
			balance = btc.getbalance(bitcoin, nick)
			if wager > balance:
				bot.notice(nick, 'Sorry, you don\'t have ' + str(wager) + ' BTC in your balance')
				return
			bitcoin.move(nick, 'roulette', wager)
			if roulette(chamber):
				roulette_bal = btc.getbalance(bitcoin, 'roulette')
				roulette_bal = roulette_bal * winnings
				bitcoin.move('roulette', nick, btc.to_float(roulette_bal))
				bot.notice(nick, 'The gun went *CLICK* and you won ' + btc.to_string(roulette_bal) + ' BTC.')
				bot.privmsg('##btcbot', from_[0] + '\'s gun went *CLICK*, winning them ' + btc.to_string(roulette_bal) + ' BTC.')
			else:
				bot.notice(nick, 'The gun went *BANG* and you lost ' + str(wager) + ' BTC.')

	except JSONRPCException:
		bot.notice(nick, 'An error has occured communicating with bitcoind, please report this to bool_')


def usage(bot, target, command):
	if command == 'roulette':
		bot.notice(target, 'USAGE: +roulette <chamber>')
