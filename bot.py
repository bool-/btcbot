import lurklib
import commands
import json
import sys


class BitBot(lurklib.Client):
	def __init__(self, name, server, port, nick, user, channels):
		super().__init__(server=server, port=port, nick=nick, user=user, tls=False)
		self.serv_name = name
		self.auto_join_channels = channels

	def on_connect(self):
		print('Connected to ' + self.serv_name)
		for channel in self.auto_join_channels:
			self.join_(channel)
		self.identified_users = []
	def on_chanmsg(self, from_, channel, message):
		if message.startswith('+'):
			message = message[1:]
			commands.parse_command(self, config, from_, channel, message)
	def on_privmsg(self, from_, message):
		if message.startswith('+'):
			message = message[1:]
			commands.parse_command(self, config, from_, from_[0], message)
	def on_quit(self, from_, reason):
		if from_[0] in self.identified_users:
			self.identified_users.remove(from_[0])
	def on_part(self, from_, channel, reason):
		if from_[0] in self.identified_users:
			self.identified_users.remove(from_[0])

if __name__ == '__main__':
	global config
	if len(sys.argv) > 1:
		try:
			data = open(sys.argv[1]).read()
			if data != None:
				config = json.loads(data)
			else:
				print('USAGE: python bot.py <config=config.json>')
				sys.exit()
		except IOError:
			print('USAGE: python bot.py <config=config.json>')
			sys.exit()
	else:
		config = json.loads(open('config.json').read())
	print('Starting BitBot')
	commands.load_modules(config['modules'])
	commands.connect_bitcoind(config['bitcoin']['user'], config['bitcoin']['pass'], config['bitcoin']['server'], config['bitcoin']['port'])
	for name, server in config['servers'].items():
		bot = BitBot(name, server['server'], server['port'], server['nick'], server['user'], server['channels'])
		bot.mainloop()
