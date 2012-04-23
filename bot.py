import lurklib
import commands
import json

config = json.loads(open('config.json').read())

class BitBot(lurklib.Client):

	def on_connect(self):
		print('Connected to freenode')
		self.join_('##btcbot')
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
	print('Starting BitBot')
	commands.load_modules(config['modules'])
	commands.connect_bitcoind(config['bitcoin']['user'], config['bitcoin']['pass'], config['bitcoin']['server'], config['bitcoin']['port'])
	for server in config['servers']:
		bot = BitBot(server=server['server'], nick=server['nick'], user=server['user'], tls=False)
		bot.mainloop()
