# faketwitch
Emulate Twitch's chat API for other services. Only tested with Dead Cells but other things may work too, who knows.

## Installation
Hooooooooo boy this sucks.
1. Get a DNS name that has 18 total characters, same as `irc.chat.twitch.tv`.
2. Set up Let's Encrypt with your favorite web server (I like nginx) to get a real, trustworthy SSL cert on that domain. Make sure you stop the server once you have the cert.
3. Link your Dead Cells account to your actual Twitch account so the options panel appears.
4. Install `nmap` on your server - although we don't actually need `nmap`, just `ncat` which is bundled with it.
5. Use a hex editor or `sed` or something to replace `irc.chat.twitch.tv` with your new domain in either `deadcells.exe` or `hlboot.dat`.
6. On your server, run `ncat -lvCk --output /dev/tty -p 443 --ssl --ssl-cert /etc/letsencrypt/live/<your domain>/fullchain.pem --ssl-key /etc/letsencrypt/live/<your domain>/privkey.pem --sh-exec "ncat --ssl irc.chat.twitch.tv 443"`. This will let you snoop on the actual connection to Twitch.
7. Fire up Dead Cells in streamer mode (I recommend a burner save just in case) and let it connect to your fake Twitch chat server. The first line it sends should be logged on your server as `PASS oauth:<token>`. Quit Dead Cells before you kill the `ncat` server.
8. Clone this repository to somewhere on your server and `python setup.py install` (might be `python3`).
9. Copy `config.example.py` to `config.py` and fill in that token.
10. Do whatever platform-specific setup you want - those instructions are available below.
11. To run this server, run `ncat -lvCk -p 443 --ssl --ssl-cert /etc/letsencrypt/live/<your domain>/fullchain.pem --ssl-key /etc/letsencrypt/live/<your domain>/privkey.pem --sh-exec "python faketwitch.py"` (might have to use `python3` on Linux).

## Mixer Setup

## YouTube Live Setup
1. Make a project in the [Google Developers Console](https://console.developers.google.com/) and give it access to the YouTube Data API.
2. Set up credentials. You're using the YouTube Data API from an Other UI and accessing user data. Your consent screen will need `youtube` and `youtube.force_ssl` scopes. You will get a scary warning about verification here; you can ignore it. Download the credentials as JSON.
3. Take the entire JSON file and dump it in `config.py`.
