import lurklib
import commands

class BitBot(lurklib.Client):

	def on_connect(self):
		print('Connected to freenode')
		self.join_('##btcbot')
		self.identified_users = []
	def on_chanmsg(self, from_, channel, message):
		if message.startswith('+'):
			message = message[1:]
			commands.parse_command(self, from_, channel, message)
	def on_privmsg(self, from_, message):
		if message.startswith('+'):
			message = message[1:]
			commands.parse_command(self, from_, from_[0], message)
	def on_quit(self, from_, reason):
		if from_[0] in self.identified_users:
			self.identified_users.remove(from_[0])
	def on_part(self, from_, channel, reason):
		if from_[0] in self.identified_users:
			self.identified_users.remove(from_[0])

if __name__ == '__main__':
	print('Starting BitBot')
	bot = BitBot(server='wright.freenode.net', nick=('btcbot', 'btcbot_'), user='btcbot', tls=False)
	bot.mainloop()
