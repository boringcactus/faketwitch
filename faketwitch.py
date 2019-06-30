import sys
import config

# set up logging
raw_input = input
raw_print = print

def input():
    result = raw_input()
    raw_print('>', result, file=sys.stderr)
    return result

def print(*args):
    raw_print('<', *args, file=sys.stderr)
    raw_print(*args)

def debug(*args):
    raw_print('|', *args, file=sys.stderr)

def iprint(*args):
    print(':tmi.twitch.tv', *args)

debug('Game has connected to fake Twitch chat')

_, actual_token = input().split(' ', 1) # check the oauth token from PASS
if actual_token != config.EXPECTED_TWITCH_OAUTH:
    exit(1)

_, twitch_channel = input().split(' ', 1) # use the channel name from NICK
iprint('001', twitch_channel, ':Welcome, GLHF!')
iprint('002', twitch_channel, ':Your host is tmi.twitch.tv')
iprint('003', twitch_channel, ':This server is rather new')
iprint('004', twitch_channel, ':-')
iprint('375', twitch_channel, ':-')
iprint('372', twitch_channel, ':You are in a maze of twisty passages, all alike.')
iprint('376', twitch_channel, ':>')

input() # ignore CAP REQ membership
input() # ignore CAP REQ tags
input() # ignore CAP REQ commands
input() # ignore JOIN

iprint('CAP * ACK :twitch.tv/membership')
iprint('CAP * ACK :twitch.tv/tags')
iprint('CAP * ACK :twitch.tv/commands')

print(':' + twitch_channel + '!' + twitch_channel + '@' + twitch_channel + '.tmi.twitch.tv JOIN #' + twitch_channel)
print(':' + twitch_channel + '.tmi.twitch.tv 353', twitch_channel, '= #' + twitch_channel, ':' + twitch_channel)
print('@badge-info=;badges=broadcaster/1;color=#8A2BE2;display-name=' + twitch_channel + ';emote-sets=0,1512298;mod=0;subscriber=0;user-type= :tmi.twitch.tv USERSTATE #' + twitch_channel)
print('@emote-only=0;followers-only=-1;r9k=0;rituals=0;room-id=52892078;slow=0;subs-only=0 :tmi.twitch.tv ROOMSTATE #' + twitch_channel)

def new_real_message(name, msg):
    cruft = {
        '@badge-info': '',
        'badges': 'premium/1',
        'color': '',
        'display-name': name,
        'emotes': '',
        'flags': '',
        'id': '00000000-0000-0000-0000-000000000000',
        'mod': '0',
        'room-id': '0',
        'subscriber': '0',
        'tmi-sent-ts': '0',
        'turbo': '0',
        'user-id': '0',
        'user-type': '',
    }
    cruft = ';'.join('='.join(x) for x in cruft.items())
    name = ':{0}!{0}@{0}.tmi.twitch.tv'.format(name)
    debug(name)
    print(cruft, name, 'PRIVMSG', '#' + twitch_channel, ':' + msg)

def parse_fake_message(line: str):
    [_, _, text] = line.split(' ', maxsplit=2)
    text = text.lstrip(':')
    debug('Sending', text)

new_real_message('GamesDoneQuick', 'pickme')

while True:
    parse_fake_message(input())
