import asyncio
import shelve
import time
import datetime
import uuid
from dateutil.relativedelta import relativedelta

# CLASSES #
# TODO: Switch to multiPROCESSING wait maybe not
# TODO: Switch to seconds from now until datetime of reminder
# TODO: Calculate datetime of reminder by using timedelta


# Reminder Class
class Reminder:
    def __init__(self, author_id, length, message=None):

        # The user who requested the reminder
        self.author_id = author_id

        self.id = uuid.uuid4()

        # The datetime at which the reminder needs to be sent
        self.dispatch_datetime = self.calc_dispatch_datetime(length)

        # The message to send with the reminder
        self.message = "Hi! Here's your reminder as requested: \n"

        # If the user provided a message, append it to self.message
        if message is not None:
            self.message += message
        else:
            pass

    # Run the reminder
    async def run(self):

        print("RUNNING")

        # Calculate the amount of seconds from now
        sleep_time = self.calc_time_to_dispatch(self.dispatch_datetime)

        # If sleep_time is less than it means that the datetime has passed, so dispatch the reminder now
        if sleep_time <= 0:
            self.message += "\n \n (Sorry if I'm late, there must have been a server issue)"
            await dispatch(self.author_id, self.message, self)

        else:
            await asyncio.sleep(int(sleep_time))
            await dispatch(self.author_id, self.message, self)

    # Calculates the datetime to dispatch the notification given a length of time
    @staticmethod
    def calc_dispatch_datetime(length):

        now = datetime.datetime.now()

        # Minutes, Hours, Days, etc...
        l_period = length[-1:]

        # The amount of l_period
        period = length[0:-1]

        if l_period == "s":
            dispatch_dt = now + datetime.timedelta(seconds=int(period))

        elif l_period == "m":
            dispatch_dt = now + datetime.timedelta(minutes=int(period))

        elif l_period == "h":
            dispatch_dt = now + datetime.timedelta(hours=int(period))

        elif l_period == "d":
            dispatch_dt = now + datetime.timedelta(days=int(period))

        elif l_period == "w":
            dispatch_dt = now + datetime.timedelta(weeks=int(period))

        elif l_period == "t":
            dispatch_dt = now + relativedelta(months=int(period))

        else:
            dispatch_dt = -1

        return dispatch_dt

    @staticmethod
    def calc_time_to_dispatch(dispatch_datetime, now=None):

        # Check if a datetime corresponding to the current time (now) is passed
        if now is None:
            current_dt = datetime.datetime.now()

        elif now is datetime.datetime:
            current_dt = now

        else:
            raise TypeError("now must be a datetime")

        return (dispatch_datetime - current_dt).total_seconds()

    @staticmethod
    def valid_length(length):
        # If the last character in the string is not a valid length period
        return length[-1:] in ["s", "m", "h", "d", "w", "t"]


# Holds the client as a class so that it can be accessed in the separate thread that this entire file is ran on
class ClientWrapper:
    def __init__(self, client):
        self.client = client

    def update(self, client):
        self.client = client


# GLOBALS #

main_client = ClientWrapper(None)

# METHODS #


# Dispatches a custom event to the discord bot to tell it to send the reminder
async def dispatch(author_id, message, reminder_object):

    # Sending a custom event to the Discord Client
    main_client.client.dispatch("reminder_ready", author_id, message, reminder_object)

    # Removing the reminder object from the reminder_db as it has already been dispatched
    reminder_db = shelve.open("reminder_db", writeback=True)

    for reminder in reminder_db["reminders"]:

        if reminder_object.id == reminder.id:
            reminder_db["reminders"].remove(reminder)
            break

    reminder_db.close()


# Checks for new reminders every 10 seconds
async def check_new_reminders(loop):

    reminder_db = shelve.open("reminder_db", writeback=True)

    # Check the new reminders "table" of the database, then run all of the reminder tasks, finally move from new reminders to reminders
    for reminder in list(reminder_db["new_reminders"]):
        loop.create_task(reminder.run())

        # Add to the regular reminder database
        reminder_db["reminders"].append(reminder)

        # Remove from the new reminders database
        reminder_db["new_reminders"].remove(reminder)

    reminder_db.close()

    await asyncio.sleep(10)

    loop.create_task(check_new_reminders(loop))


# Called by main
async def start(loop):

    # Reminder database
    reminder_db = shelve.open("reminder_db", writeback=True)

    # List of task objects
    tasks = list(reminder_db["reminders"])

    for task in tasks:
        loop.create_task(task.run())

    reminder_db.close()

    print("DONE START")


def main(client):

    time.sleep(10)

    main_client.update(client)
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)

    # Runs start method
    event_loop.create_task(start(event_loop))

    # Runs check_new_reminders method
    event_loop.create_task(check_new_reminders(event_loop))

    event_loop.run_forever()


