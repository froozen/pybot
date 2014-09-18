import connection
import random

def cmd_roll(parsed_input):
    split = parsed_input["content"].split(" ")

    if len(split) > 1:
        try:
            end = int(split[1])
            connection.send_privmsg(parsed_input["channel"], "You rolled %d." % (random.randint(1, end)))

        except ValueError:
            connection.send_privmsg(parsed_input["channel"], "Invalind input: %s." % split[1])

    else:
        connection.send_privmsg(parsed_input["channel"], "You rolled %d." % (random.randint(1, 6)))
