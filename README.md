# Сhatbot ModHelper

**For the security of the game project, the real web addresses have been hidden.**
**This repository was created for my archive.**

Chatbot for monitoring requests for unbanning in the game project.
This chatbot was written in 2019 and is my first major single project.
As of 2019, it is also actively running without any glitches.

The task of the bot was to get the necessary data on player unblocking requests from the game project site and analyze them to notify the moderators via messenger. The bot itself is simple, but it facilitated the work of moderators and increased their productivity. And for the users of the game project reduced the waiting time for an answer to an unblocking request.

## Requirements

For permanent operation, you can run it on a VDS (Virtual Dedicated Server).
The recommended version to run it is python 3.5.

+ Modules:
  + vk_api
  + requests
  + bs4
  + telebot
  + pytz

## Launching

To run the chatbot in **VK** you can simply run the files `main.py` and `commands.py`.

```console
...\vk>$ python main.py
```

```console
...\vk>$ python commands.py
```

To run the chatbot in **Telegram**, run the `main.py` file.

```console
...\telegram>$ python main.py
```

