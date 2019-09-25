import discord
import datetime
import threading
import remindme
import asyncio
from interpreters import interpreter_finance, interpreter_utilities

# Client Object (Bot itself)
client = discord.Client(loop=asyncio.new_event_loop())

today_date = datetime.date.today()


# When the bot connects, log details into console
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


# Start Listening For Messages
@client.event
async def on_message(message):

    message_text = message.content

    # Finance related
    if message.content.startswith("#"):

        # Removes the NC9 Signal as well as any extra whitespace then turns all letters to lowercase
        clean_message = message_text.replace("#", "").strip().lower()

        response = interpreter_finance.main_interpreter(clean_message)

        await message.channel.send(embed=response)

    # Utility
    elif message.content.startswith("&"):

        # NOTE: This passes the Message OBJECT, not the message text
        response = interpreter_utilities.main_interpreter(message)

        await message.channel.send(response)

    elif message.content.startswith("^"):
        await client.logout()

    # DEBUG
    elif message.content.startswith("$"):

        user = message.author

        await user.send(client.get_user("REDACTED").name)


@client.event
async def on_reaction_add(reaction, user):
    ...


@client.event
async def on_reminder_ready(author_id, message, time):

    author = client.get_user(author_id)

    await author.send(message)


if __name__ == "__main__":

    reminder_thread = threading.Thread(target=remindme.main, args=[client])
    reminder_thread.start()

    client.run('KEY_HERE')

