import connection

welcome_msgs = {}

def on_join(parsed_input):
    if parsed_input["name"] != connection.config["name"]:
        if parsed_input["name"] in welcome_msgs:
            connection.send_privmsg(parsed_input["channel"], welcome_msgs[parsed_input["name"]])

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

