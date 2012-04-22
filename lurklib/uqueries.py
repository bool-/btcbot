#    This file is part of Lurklib.
#    Copyright (C) 2011  LK-
#
#    Lurklib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#    Lurklib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Lurklib.  If not, see <http://www.gnu.org/licenses/>.
""" User queries and such. """

from __future__ import with_statement


class _UserQueries(object):
    """ Defines user queries and such. """
    def who(self, target):
        """
        Runs a WHO on a target
        Required arguments:
        * target - /WHO <target>
        Returns a dictionary, with a nick as the key and -
            the value is a list in the form of;
           [0] - Username
           [1] - Priv level
           [2] - Real name
           [3] - Hostname
        """
        with self.lock:
            self.send('WHO %s' % target)
            who_lst = {}

            while self.readable():
                msg = self._recv(expected_replies=('352', '315'))
                if msg[0] == '352':
                    raw_who = msg[2].split(None, 7)
                    prefix = raw_who[5].replace('H', '', 1).replace('*', '', 1)
                    channel = raw_who[0]
                    nick = raw_who[4]
                    if prefix == '~':
                        self.channels[channel]['USERS'][nick] = \
                           ['~', '', '', '', '']
                    elif prefix == '&':
                        self.channels[channel]['USERS'][nick] = \
                           ['', '&', '', '', '']
                    elif prefix == '@':
                        self.channels[channel]['USERS'][nick] = \
                           ['', '', '@', '', '']
                    elif prefix == '%':
                        self.channels[channel]['USERS'][nick] = \
                           ['', '', '', '%', '']
                    elif prefix == '+':
                        self.channels[channel]['USERS'][nick] = \
                           ['', '', '', '', '+']
                    else:
                        self.channels[channel]['USERS'][nick] = \
                           ['', '', '', '', '']
                    who_lst[raw_who[4]] = raw_who[1], prefix, \
                        raw_who[7], raw_who[2]
                elif msg[0] == '315':
                    return who_lst

    def whois(self, nick):
        """
        Runs a WHOIS on someone.
        Required arguments:
        * nick - Nick to whois.
        Returns a dictionary:
            IDENT == The user's ident.
            HOST == The user's host.
            NAME == The user's real name.
            SERVER == The server the user is on.
            SERVER_INFO == The name of the server the user is on.
            CHANNELS == A list of channels the user is on.
            IDLE == The user's idle time.
            AWAY, present if the user is away,
                returns a string containing their away message.
            OP == Present if the user is an IRC operator.
            ETC == Other data sent in response to the WHOIS query.
        """
        with self.lock:
            self.send('WHOIS %s' % nick)
            whois_r = {'CHANNELS': []}

            while self.readable():
                msg = self._recv()
                info = msg[2].split(None, 4)
                if msg[0] == '311':
                    whois_r['IDENT'] = info[1]
                    whois_r['HOST'] = info[2]
                    whois_r['NAME'] = info[4][1:]
                elif msg[0] == '312':
                    whois_r['SERVER'] = info[1]
                    whois_r['SERVER_INFO'] = ' '.join(info[2:])[1:]
                elif msg[0] == '319':
                    whois_r['CHANNELS'].append(' '.join(info[1:])[1:].split())
                elif msg[0] == '317':
                    whois_r['IDLE'] = info[2]
                elif msg[0] == '301':
                    whois_r['AWAY'] = info[1][1:]
                elif msg[0] == '313':
                    whois_r['OP'] = ' '.join(info[1:])[1:]
                elif msg[0] == '318':
                    break
                else:
                    if 'ETC' in whois_r:
                        whois_r['ETC'].append(msg[2])
                    else:
                        whois_r['ETC'] = [msg[2]]

            return whois_r

    def whowas(self, nick):
        """
        Runs a WHOWAS on someone.
        Required arguments:
        * nick - Nick to run a WHOWAS on.
        Returns a list:
           [0] The user's nick.
           [1] The user's ident.
           [2] The user's host.
           [3] The user's real name.
        """
        with self.lock:
            self.send('WHOWAS %s' % nick)

            rwhowas = []
            while self.readable():
                msg = self._recv(expected_replies=('314', '312', '369'))
                if msg[0] == '314':
                    raw_whowas = msg[2].split()
                    rwhowas = raw_whowas[0], raw_whowas[1], \
                        raw_whowas[2], raw_whowas[4][1:]
                elif msg[0] == '312':
                    pass
                elif msg[0] == '369':
                    return rwhowas
