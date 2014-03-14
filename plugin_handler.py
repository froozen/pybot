import connection
import time

commands = {}
triggers = {}
command_prefix = ")"
last_time = time.time()

def add_trigger(trigger, method):
    if trigger in triggers:
        triggers[trigger].append(method)
    
    else:
        triggers[trigger] = [method]

def handle_input(input):
    print input
    parsed_input = __parse_input(input)

    if parsed_input["type"] in triggers:
        for triggered_method in triggers[parsed_input["type"]]:
                triggered_method(parsed_input)

    if input.startswith("PING"):
        global last_time
        print time.time() - last_time
        last_time = time.time()
        connection.send_message(input.replace("PING", "PONG"))
        
    if parsed_input["type"] == "PRIVMSG":
        if parsed_input["content"].startswith(command_prefix):
            parsed_input["content"] = parsed_input["content"][1:len(parsed_input["content"])]
            print parsed_input["content"]
            for command in commands:
                if parsed_input["content"].startswith(command):
                    print "Running command: " + command
                    commands[command](parsed_input)

def __parse_input(input):
    parsed_input = {}
    split = input.split(" ")
    parsed_input["origin"] = split[0]

    if "!" in split[0]:
        parsed_input["name"] = split[0][1:split[0].find("!~")]

    parsed_input["type"] = split[1]
    if len(split) > 2:
        parsed_input["channel"] = split[2]

    if len(split) > 3:
        split[3] = split[3][1:len(split[3])]

        if len(split) > 4:
            parsed_input["content"] = " ".join(split[3:len(split)])

        else:
            parsed_input["content"] = split[3]

    return parsed_input

def __load_plugins():
    print "Loading plugins..."
    f = open("plugins.py")
    exec(f.read())
    f.close()

def init():
    global last_time
    last_time = time.time()
    __load_plugins()

