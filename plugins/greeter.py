import connection
import user_data

welcome_msgs = {}

def afk_token(parsed_input):
    afks = ""
    for name, user in user_data.users.iteritems():
        if parsed_input["channel"] in user["channels"] and user["status"] == "afk":
            afks += name + " "

    return afks

special_tokens = {
    "%afk%" : afk_token,
}

def render_welcome_msg(parsed_input):
    msg = welcome_msgs[parsed_input["name"]]
    for old, new_func in special_tokens.iteritems():
        msg = msg.replace(old, new_func(parsed_input))
    return msg

def on_join(parsed_input):
    if parsed_input["name"] != connection.config["name"]:
        if parsed_input["name"] in welcome_msgs:
            connection.send_privmsg(parsed_input["channel"], render_welcome_msg(parsed_input))

        else:
            connection.send_privmsg(parsed_input["channel"], "Welcome on %s, %s." % (parsed_input["channel"], parsed_input["name"])) 

def cmd_welcomemsg(parsed_input):
    split = parsed_input["content"].split(" ")

    if len(split) > 1:
        welcome_msg = " ".join(split[1:len(split)])
        welcome_msgs[parsed_input["name"]] = welcome_msg
        save_welcome_msgs()

def init():
    print "Loading welcome messages from 'plugins/welcomemsgs'"
    f = open("plugins/welcomemsgs")

    for line in f.readline():
        line = line[0:-1]

        #format: name msg
        split = line.split(" ")
        
        if len(split) > 1:
            welcome_msgs[split[0]] = " ".join(split[1:len(split)])

    f.close()

def save_welcome_msgs():
    f = open("plugins/welcomemsgs", "w")
    f.truncate()

    for name in welcome_msgs:
        f.write("%s %s\n" % (name, welcome_msgs[name]))

    f.close()

