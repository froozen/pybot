from plugins import greeter, user_data, messaging

commands["status"] = user_data.cmd_status
commands["afk"] = user_data.cmd_afk
commands["msg"] = messaging.cmd_msg
commands["cm"] = messaging.cmd_cm
commands["welcomemsg"] = greeter.cmd_welcomemsg

add_trigger("JOIN", greeter.on_join)
add_trigger("353", user_data.on_353)
add_trigger("JOIN", user_data.on_join)
add_trigger("PART", user_data.on_part)
add_trigger("QUIT", user_data.on_quit)
add_trigger("NICK", user_data.on_nick)
add_trigger("PRIVMSG", user_data.on_privmsg)
add_trigger("JOIN", messaging.on_join)

messaging.init()
greeter.init()
