import imp

COMMANDS = { 'reload': 0 }
PERMISSIONS = [ 'botadmin' ]

# TODO add configuration reloading
def do_command(context, from_, target, command, args):
	nick = from_[0]
	modules = context['modules']
	bot = context['bot']
	if command == 'reload':
		for module in modules:
			imp.reload(module)
			bot.notice(nick, module.__name__ + ' has been reloaded.')


def usage(bot, target, command):
	if command == 'reload':
		bot.notice(target, 'USAGE: +reload')
		
