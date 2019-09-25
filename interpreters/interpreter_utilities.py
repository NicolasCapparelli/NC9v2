import asyncio
import shelve
import remindme


def main_interpreter(message_object):

    # Removes the NC9 Signal as well as any extra whitespace then turns all letters to lowercase
    clean_message_text = message_object.content.replace("&", "").strip().lower()

    command = clean_message_text.split(" ")[0]

    if command in UTIL_COMMANDS.keys():

        return UTIL_COMMANDS[command](clean_message_text.replace(command, "").strip(), message_object)

    else:
        return "Not a command"  # Create reaction libary like in valery


# Adds a reminder to the new reminder database
def remind_me(command, message_object):

    # Remove remindme from the command, leaving only the time frame and message in an array
    message_split = command.split(" ")

    if not remindme.Reminder.valid_length(message_split[0]):
        return "Invalid Time Frame"

    # Checking if there is a reminder message
    if len(message_split) > 1:
        # Join together everything after the first element which is the message
        reminder_message = " ".join(message_split[1:])

    else:
        reminder_message = None

    # Creating the reminder itself
    reminder = remindme.Reminder(author_id=message_object.author.id, length=message_split[0], message=reminder_message)

    # Opening up remindme db
    remind_db = shelve.open("reminder_db", writeback=True)

    # Adding the reminder to the new reminders table in our db
    remind_db["new_reminders"].append(reminder)

    # Closing db
    remind_db.close()

    # Return message to reply to the user
    return "Reminder created! I will be messaging you in " + message_split[0]


UTIL_COMMANDS = {

    "remindme": remind_me,

}
