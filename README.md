pybot
=====

pybot is an IRC-bot focused on extendability through plugins written in python.

#### Setting it up

First, make sure you have Python <= 2.7 installed. An example of how to check if it's installed down below (note that the information you have may not be exactly the same as the info here).<br>

```
$ python2 --version
  Python 2.7.10
```

Second, get a copy of pybot by running:<br>
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
            "password": "password_here",
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
The `port`, `password`, and `channels` configuration values are optional.<br>

**NOTE:**<br>
Don't use the same `name`-value twice, as it is used as filename for server data files.<br>

Now you can simply run:<br>
`$ ./main.py`

#### Adding plugins

Adding plugins is rather simple. To do that, you simply copy the plugin into the plugins folder and restart the bot.<br>
Some nice plugins that you might want can be found in [pybot-plugins](https://github.com/froozen/pybot-plugins).

If you are interested in writing your own plugins, make sure to take a look at the [wiki](https://github.com/froozen/pybot/wiki).
