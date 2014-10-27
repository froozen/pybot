pybot
=====

pybot is an IRC-bot focused on extendability trough plugins written in python.

#### Setting it up

First get a copy of pybot by running:<br>
```
$ git clone https://github.com/froozen/pybot.git
$ cd pybot
```

Next, you need to configure pybot. To do this, simply open `config.json` in your favorite editor:<br>
`$ vim config.json`

Now you need to add a server connection like this:<br>
```json
{
    "servers": [
        {
            "name": "freenode",
            "nick": "pybot",
            "host": "irc.freenode.net",
            "port": 6667,
            "channels": [ "#python" ]
        }
    ]
}
```

The bot will now connect to irc.freenode.net on port 6667, log in as pybot and join the #python channel.<br>
It is possible to have multiple servers and multiple channels per server, separated with commas.<br>
The `port` and `channels` configuration values are optional.<br>

**NOTE:**<br>
Don't use the same `name`-value twice, as it is used as filename for server data files.<br>

Now you can simply run:<br>
`$ ./main.py`

#### Adding plugins

Adding plugins is rather simple. To do that, you simply copy the plugin into the plugins folder and restart the bot.
