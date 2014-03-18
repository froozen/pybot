import connection

users = {}

def on_353(parsed_input):
    split = parsed_input["content"].split(" ")

    if len(split) > 2:
        split.pop(0)
        split[1] = split[1][1:len(split[1])]
        for user in split[1:len(split)]:
            if user.startswith("@") or user.startswith("+"):
                    user = user[1:len(user)]

            if user in users:
                users[user]["channels"].append(split[0])

            else:
                __create_user(user)
                users[user]["channels"] = [split[0]]

def on_join(parsed_input):
    if parsed_input["name"] != connection.config["name"]:
        if parsed_input["name"] in users:
            users[parsed_input["name"]]["channels"].append(parsed_input["channel"])

        else:
            __create_user(parsed_input["name"])
            users[parsed_input["name"]]["channels"] = [parsed_input["channel"]]

def on_part(parsed_input):
    if len(users[parsed_input["name"]]["channels"]) > 1:
        users[parsed_input["name"]]["channels"].remove(parsed_input["channel"])

    else:
        del(users[parsed_input["name"]])

def on_quit(parsed_input):
    del(users[parsed_input["name"]])

def on_privmsg(parsed_input):
    if parsed_input["name"] in users:
        if users[parsed_input["name"]]["status"] == "afk":
            users[parsed_input["name"]]["status"] = "online"
            if "message" in users[parsed_input["name"]]:
                del(users[parsed_input["name"]]["message"])

            connection.send_privmsg(parsed_input["channel"], "%s is back." % parsed_input["name"])

def on_nick(parsed_input):
    if parsed_input["name"] in users:
        #username is in channel because of some random design decission in the irc protocol
        users[parsed_input["channel"][1:len(parsed_input["channel"])]] = users[parsed_input["name"]]
        del(users[parsed_input["name"]])

def __create_user(name):
    print "Creating user", name
    users[name] = {}
    users[name]["status"] = "online"

def cmd_status(parsed_input):
    args = parsed_input["content"].split(" ")
    if len(args) > 1:
        if args[1] in users:
            if "message" in users[args[1]]:
                connection.send_privmsg(parsed_input["channel"], "%s is currently %s (%s)" % (args[1], users[args[1]]["status"], users[args[1]]["message"]))
            
            else:
                connection.send_privmsg(parsed_input["channel"], "%s is currently %s" % (args[1], users[args[1]]["status"]))

        else:
            connection.send_privmsg(parsed_input["channel"], "%s is currently offline." % args[1])

def cmd_afk(parsed_input):
    users[parsed_input["name"]]["status"] = "afk"
    
    args = parsed_input["content"].split(" ")
    if len(args) > 1:
        users[parsed_input["name"]]["message"] = " ".join(args[1:len(args)])
    
    connection.send_privmsg(parsed_input["channel"], "%s is now afk." % parsed_input["name"])

