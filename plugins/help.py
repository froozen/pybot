import connection, plugins, logging
import pkgutil

commands = []
help_text = {}

def init():
    __load_commands()
    __load_help_text()


def cmd_help(parsed_input):
    split = parsed_input["content"].split(" ")
    if len(split) > 1:
        if split[1] in help_text:
            connection.send_privmsg(parsed_input["channel"], help_text[split[1]])
        
        else:
            connection.send_privmsg(parsed_input["channel"], "Can't find help text for: %s." % split[1])

    else:
        connection.send_privmsg(parsed_input["channel"], "Available commands: %s" % ", ".join(commands))

def __load_commands():
    package = plugins
    prefix = package.__name__ + "."
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
        if modname != "help":
            module = __import__(modname, fromlist = "dummy")
            dirs = dir(module)
        
            for method in dirs:
                if method.startswith("cmd_"):
                    command_name = method[4:len(method)]
                    commands.append(command_name)

def __load_help_text():
    f = open("plugins/help_text")
    print "Loading help text from 'plugins/help_text'"
    logging.append_to_log("Loading help text from 'plugins/help_text'")

    for line in f.readlines():
        split = line.split(" ")
        if len(split) > 1:
            help_text[split[0]] = " ".join(split[1:len(split)])

    f.close()
