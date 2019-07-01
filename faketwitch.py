import sys
from datetime import timedelta
import time
import ssl
import os.path

from tornado.iostream import PipeIOStream
from tornado.ioloop import IOLoop, PeriodicCallback
import tornado
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado import gen

import config

# set up logging
raw_print = print

def parse_fake_message(line: str):
    [_, _, text] = line.split(' ', maxsplit=2)
    text = text.lstrip(':')
    print('| Sending', text)
    config.backend.send_message(text)

class FakeTwitchServer(TCPServer):
    streams = []

    async def handle_stream(self, stream, address):
        async def input():
            result = await stream.read_until(b"\n")
            result = result.decode().rstrip("\r\n")
            raw_print('>', result)
            return result
        async def print(*args):
            line = ' '.join(args) + '\r\n'
            raw_print('<', line.rstrip('\r\n'))
            return await stream.write(line.encode())
        async def iprint(*args):
            return await print(':tmi.twitch.tv', *args)
        pw = await input()
        _, actual_token = pw.split(' ', 1) # check the oauth token from PASS
        if actual_token != config.EXPECTED_TWITCH_OAUTH:
            print('| Actual token', repr(actual_token), 'did not match expected token', repr(config.EXPECTED_TWITCH_OAUTH))
            exit(1)

        nick = await input()
        _, twitch_channel = nick.split(' ', 1) # use the channel name from NICK
        self.twitch_channel = twitch_channel
        await iprint('001', twitch_channel, ':Welcome, GLHF!')
        await iprint('002', twitch_channel, ':Your host is tmi.twitch.tv')
        await iprint('003', twitch_channel, ':This server is rather new')
        await iprint('004', twitch_channel, ':-')
        await iprint('375', twitch_channel, ':-')
        await iprint('372', twitch_channel, ':You are in a maze of twisty passages, all alike.')
        await iprint('376', twitch_channel, ':>')

        await input() # ignore CAP REQ membership
        await input() # ignore CAP REQ tags
        await input() # ignore CAP REQ commands
        await input() # ignore JOIN

        await iprint('CAP * ACK :twitch.tv/membership')
        await iprint('CAP * ACK :twitch.tv/tags')
        await iprint('CAP * ACK :twitch.tv/commands')

        await print(':' + twitch_channel + '!' + twitch_channel + '@' + twitch_channel + '.tmi.twitch.tv JOIN #' + twitch_channel)
        await print(':' + twitch_channel + '.tmi.twitch.tv 353', twitch_channel, '= #' + twitch_channel, ':' + twitch_channel)
        await print('@badge-info=;badges=broadcaster/1;color=#8A2BE2;display-name=' + twitch_channel + ';emote-sets=0,1512298;mod=0;subscriber=0;user-type= :tmi.twitch.tv USERSTATE #' + twitch_channel)
        await print('@emote-only=0;followers-only=-1;r9k=0;rituals=0;room-id=123456789;slow=0;subs-only=0 :tmi.twitch.tv ROOMSTATE #' + twitch_channel)
        
        self.streams.append(stream)
        while True:
            try:
                data = await input()
                parse_fake_message(data)
            except StreamClosedError:
                break
        self.streams.remove(stream)
    
    async def new_real_message(self, name, msg, msg_id):
        cruft = {
            '@badge-info': '',
            'badges': '',
            'color': '#ABC123',
            'display-name': name,
            'emotes': '',
            'flags': '',
            'id': msg_id,
            'mod': '0',
            'room-id': '123456789',
            'subscriber': '0',
            'tmi-sent-ts': str(int(time.time() * 1000)),
            'turbo': '0',
            'user-id': '123456789',
            'user-type': '',
        }
        cruft = ';'.join('='.join(x) for x in cruft.items())
        name = ':{0}!{0}@{0}.tmi.twitch.tv'.format(name)
        for stream in self.streams:
            text = cruft + ' ' + name + ' PRIVMSG #' + self.twitch_channel + ' :' + msg + '\r\n'
            await stream.write(text.encode())

ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_ctx.load_cert_chain(os.path.join(sys.argv[1], "fullchain.pem"),
                        os.path.join(sys.argv[1], "privkey.pem"))
server = FakeTwitchServer(ssl_options=ssl_ctx)
server.listen(443)

def new_real_message(name, msg, msg_id):
    async def yeet():
        await server.new_real_message(name, msg, msg_id)
    IOLoop.instance().add_callback(yeet)

config.backend.init(new_real_message)

IOLoop.instance().start()
