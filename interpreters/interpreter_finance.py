import requests
import discord

# PRE-MADE EMBEDS #

QUOTE_EMBED = discord.Embed()
QUOTE_EMBED.add_field(name="", value="", inline=True)
QUOTE_EMBED.add_field(name="Price", value="", inline=False)
QUOTE_EMBED.add_field(name="Change", value=" ", inline=True)
QUOTE_EMBED.add_field(name="Open", value="", inline=True)
QUOTE_EMBED.add_field(name="Volume", value="", inline=True)

DESC_EMBED = discord.Embed()
DESC_EMBED.add_field(name="Desc", value="", inline=True)
DESC_EMBED.add_field(name="Sector", value="", inline=True)
DESC_EMBED.add_field(name="Industry", value="")
DESC_EMBED.add_field(name="Exchange", value="", inline=False)
DESC_EMBED.add_field(name="CEO", value="", inline=False)
DESC_EMBED.add_field(name="Website", value="", inline=False)


def main_interpreter(message):

    # The message split into stock symbol and descriptor
    message_breakdown = message.split(" ")

    # The message_breakdown should contain only a symbol and a descriptor
    if len(message_breakdown) == 2:

        # Checking if the descriptor is valid
        if message_breakdown[1] in DESCRIPTOR_DICTIONARY.keys():

            # Passing the descriptor to the dictionary and returning the value of its respective function
            return DESCRIPTOR_DICTIONARY[message_breakdown[1]](message_breakdown[0])

        else:
            return "Invalid Descriptor"

    # There should not be anymore than 2 elements to the message_breakdown
    elif len(message_breakdown) > 2:
        return "Invalid Descriptor"

    # Otherwise it will just be the symbol, so as a default run the quote parser
    else:
        return parse_quote(message_breakdown[0])


# Simple and fast quote
def parse_quote(symbol):

    data = requests.get("https://api.iextrading.com/1.0/stock/" + symbol + "/quote").json()

    # Embed's color is dependent on stock being positive or negative
    if float(data["change"]) >= 0:
        QUOTE_EMBED.colour = 0x007213
        change_indicator = "+"
    else:
        QUOTE_EMBED.colour = 0xAB1212
        change_indicator = "-"

    # final_send = """```yaml\n{} | ({:.2f}%)```""".format(float(data["change"].__abs__()), data["changePercent"] * 100)

    # Editing Embed
    QUOTE_EMBED.set_field_at(0, name=symbol.upper(), value=data["companyName"], inline=True)
    QUOTE_EMBED.set_field_at(1, name="Price", value="${:.2f}".format(data["latestPrice"]), inline=False)
    QUOTE_EMBED.set_field_at(2, name="Change", value=change_indicator + "{:.2f} | ({:.2f}%)".format(float(data["change"].__abs__()), data["changePercent"] * 100), inline=True)
    QUOTE_EMBED.set_field_at(3, name="Prev. Close", value="${}".format(data["previousClose"]), inline=True)
    QUOTE_EMBED.set_field_at(4, name="Volume", value=data["latestVolume"], inline=True)

    return QUOTE_EMBED


# Uses IEX TOPS
def parse_tops(symbol):

    data = requests.get("https://api.iextrading.com/1.0/tops?symbols=" + symbol).json()
    ...


def parse_earnings(symbol):
    ...


# Gives details about a company
def parse_description(symbol):

    data = requests.get("https://api.iextrading.com/1.0/stock/" + symbol + "/company").json()

    DESC_EMBED.colour = 0x007213

    # Embed Fields
    DESC_EMBED.set_field_at(0, name=symbol.upper() + " Description", value=data["description"], inline=True)
    DESC_EMBED.set_field_at(1, name="Sector", value=data["sector"], inline=True)
    DESC_EMBED.set_field_at(2, name="Industry", value=data["industry"])
    DESC_EMBED.set_field_at(3, name="Exchange", value=data["exchange"], inline=False)
    DESC_EMBED.set_field_at(4, name="CEO", value=data["CEO"], inline=False)
    DESC_EMBED.set_field_at(5, name="Website", value=data["website"], inline=False)

    return DESC_EMBED


def parse_news(symbol):
    ...


def parse_virtual_portfolio():
    ...


DESCRIPTOR_DICTIONARY = {
    "e": parse_earnings,
    "d": parse_description,
    "n/": parse_news
}
