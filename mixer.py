import collections
import sys

from mixer_sample import chatty

# "borrowed" from mixer sample
from tornado.ioloop import IOLoop
import config

bad_ids = set()
def handle_chat(data, handle_message):
    # print('Got', data, file=sys.stderr)
    msg_type = data['type']
    try:
        if msg_type == 'reply':
            bad_ids.add(data['data']['id'])
    except KeyError:
        pass
    if msg_type == 'event':
        event = data['event']
        if event == 'ChatMessage':
            msg_id = data['data']['id']
            if msg_id not in bad_ids:
                name = data['data']['user_name']
                msg = ''.join(item["text"] for item in data['data']["message"]["message"])
                handle_message(name, msg, msg_id)

Config = collections.namedtuple('Config', [
    'BEAM_URI',
    'USERSCURRENT_URI',
    'CHATSCID_URI',
    'CHANNELID',
    'ACCESS_TOKEN',
    'CLIENTID',
    'CHATDEBUG',
])

config = Config(
    'https://mixer.com/api/v1/',
    'users/current',
    'chats/{cid}',
    config.MIXER_CHANNEL_ID,
    config.MIXER_ACCESS_TOKEN,
    config.MIXER_CLIENT_ID,
    False,
)

chat = chatty.create(config)

def init(handle_message):
    chat.authenticate()
    chat.on("message", lambda data: handle_chat(data, handle_message))

def send_message(msg):
    print('| Mixer: Sending', msg, file=sys.stderr)
    chat.message(msg)
