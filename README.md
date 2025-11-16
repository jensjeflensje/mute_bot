# Mute bot
As seen on
[YouTube](https://www.youtube.com/shorts/nKP6PcDVCqg)
/
[TikTok](https://www.tiktok.com/@jensderouter/video/7564812838670290198)
/
[Instagram](https://www.instagram.com/p/DQMoJPmjni2/)
.
My Discord bot that automatically mutes you
when you are too loud in a Discord voice channel.

> ⚠️ Please understand that this is just a DEMO.
> This project is in no way intended to use in a production environment.
> Even if you improve the code to use it in a public Discord, then please
> understand that moderating based on volume is a really, really bad way
> of moderating! 😅

## How to run
Copy the example env and fill it with your bot token.
```shell
cp .env.example .env
```
> ❗️ Make sure to also export the variables to your session using `source .env`.
> The script doesn't do this automatically

Install the dependencies.
```shell
pip install -r requirements.txt
```

Run the bot.
```shell
python bot.py
```

Join a VC, execute `!mutebot` and be sure to be LOUD! 🗣️