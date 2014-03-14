import connection
from plugins import user_data

messages = {}

def cmd_msg(parsed_input):
    split = parsed_input["content"].split(" ")
    
    if len(split) > 2:
        message = {}
        message["sender"] = parsed_input["name"]
        message["receiver"] = split[1]
        message["content"] = " ".join(split[2:len(split)])
        message["read"] = False
        
        if message["receiver"] in user_data.users:
            if user_data.users[message["receiver"]]["status"] == "online":
                connection.send_privmsg(message["receiver"], __message_to_str(message))

            elif user_data.users[message["receiver"]]["status"] == "afk":
                if not message["receiver"] in messages:
                    messages[message["receiver"]] = []

                messages[message["receiver"]].append(message)
                connection.send_privmsg(message["receiver"], "You got a new message!")
                save_messages()
        
        else:
            if message["receiver"] in messages:
                messages[message["receiver"]].append(message)
                save_messages()

            else:
                messages[message["receiver"]] = [message]

def cmd_cm(parsed_input):
    if parsed_input["name"] in messages:
        for message in messages[parsed_input["name"]]:
            connection.send_privmsg(parsed_input["name"], "%d.%s %s" % (messages[parsed_input["name"]].index(message)," New:" * (not message["read"]), __message_to_str(message)))
            message["read"] = True

        save_messages()

    else:
        connection.send_privmsg(parsed_input["name"], "There are no messages for you.")

def __message_to_str(message):
    return "'%s' - from %s" % (message["content"], message["sender"])

def on_join(parsed_input):
    if parsed_input["name"] in messages:
        new_messages = 0
        for message in messages[parsed_input["name"]]:
            if not message["read"]:
                new_messages += 1
                break

        if new_messages > 0:
            connection.send_privmsg(parsed_input["name"], "%s you have %d new message(s)." % (parsed_input["name"], new_messages))

def init():
    print "Loading messages from 'plugins/messages'"
    f = open("plugins/messages")
    
    for line in f.readlines():
        line = line[0:-1]
        #format: sender receiver read content
        split = line.split(" ")
        
        if len(split) > 3:
            message = {}
            message["sender"] = split[0]
            message["receiver"] = split[1]
            message["read"] = split[2] == "True"
            message["content"] = " ".join(split[3:len(split)])

            if message["receiver"] in messages:
                messages[message["receiver"]].append(message)
            
            else:
                messages[message["receiver"]] = [message]

        else:
            print "Error with saved message:", line

    f.close()

def save_messages():
    f = open("plugins/messages", 'w')
    f.truncate()

    for user_messages in messages:
        for message in messages[user_messages]:
            message_string = "%s %s %r %s\n" % (message["sender"], message["receiver"], message["read"], message["content"])
            f.write(message_string)
    
    f.close()

