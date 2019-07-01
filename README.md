# faketwitch
Emulate Twitch's chat API for other services. Only tested with Dead Cells but other things may work too, who knows.

## Installation
Hooooooooo boy this sucks. Assumes you're on Windows and playing Dead Cells.
1. Get a DNS name that has 18 total characters, same as `irc.chat.twitch.tv`.
2. Set up Let's Encrypt with your favorite web server (I like nginx) to get a real, trustworthy SSL cert on that domain. Make sure you stop the server once you have the cert.
3. Link your Dead Cells account to your actual Twitch account so the options panel appears.
4. Install `nmap` on your server - although we don't actually need `nmap`, just `ncat` which is bundled with it.
5. Download the Linux version of Dead Cells - easiest in a Linux VM.
6. Run `sed -i s/irc.chat.twitch.tv/<your domain>/ hlboot.dat` in the VM's Dead Cells directory.
7. Steal your patched `hlboot.dat` from the VM's Dead Cells directory and put it in your actual Dead Cells directory.
8. Download the [HashLink runtime](https://github.com/HaxeFoundation/hashlink/releases) and steal `hl.exe`. Rename it to `deadcells.exe` and stick it in your Dead Cells directory.
9. On your server, run `ncat -lvCk --output /dev/tty -p 443 --ssl --ssl-cert /etc/letsencrypt/live/<your domain>/fullchain.pem --ssl-key /etc/letsencrypt/live/<your domain>/privkey.pem --sh-exec "ncat --ssl irc.chat.twitch.tv 443"`. This will let you snoop on the actual connection to Twitch.
10. Fire up Dead Cells in streamer mode (I recommend a burner save just in case) and let it connect to your fake Twitch chat server. The first line it sends should be logged on your server as `PASS oauth:<token>`. Quit Dead Cells before you kill the `ncat` server.
11. Clone this repository to somewhere on your server and `python setup.py install` (might be `python3`).
12. Copy `config.example.py` to `config.py` and fill in that token.
13. Do whatever platform-specific setup you want - those instructions are available below.
14. To run this server, run `python faketwitch.py /etc/letsencrypt/live/<your domain>` (might have to use `python3` on Linux).

## Mixer Setup
1. Get your Mixer channel ID as described in `config.py`.
2. Get your Mixer access token - the easy way is to steal it from [the Mixer chat API example](https://dev.mixer.com/guides/chat/chatbot) by clicking the `'Click here to get your Token!'` in the Node example.
3. Get your Mixer OAuth client ID by making a new Mixer OAuth application.
4. Dump all those in `config.py`.
5. Uncomment `import mixer as backend` in `config.py`.

## YouTube Live Setup (doesn't work yet)
1. Make a project in the [Google Developers Console](https://console.developers.google.com/) and give it access to the YouTube Data API.
2. Set up credentials. You're using the YouTube Data API from an Other UI and accessing user data. Your consent screen will need `youtube` and `youtube.force_ssl` scopes. You will get a scary warning about verification here; you can ignore it. Download the credentials as JSON.
3. Take the entire JSON file and dump it in `config.py`.
4. Uncomment `import youtube as backend` in `config.py`.
