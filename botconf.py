import os
from telegram import Bot
from telegram import BotCommand


token = os.getenv('TGTOKEN')
bot = Bot(token=token)

def main():
    commands = [
        BotCommand("active_problems", "See active problems details")
        ]
    set_commands = bot.set_my_commands(commands=commands)
    return set_commands
