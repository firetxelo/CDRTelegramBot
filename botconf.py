import os
from telegram import Bot
from telegram import BotCommand


token = os.getenv('TGTOKEN')
bot = Bot(token=token)

def main():
    commands = [
        BotCommand("start", "Start Bot"),
        BotCommand("list_hostgroup", "List all host groups"),
        BotCommand("list_hosts", "List all host in a group"),
        BotCommand("list_problems_by_host", "List problems by host"),
        BotCommand("detail_items_with_problem_id", "Detail items related to a problem"),
        BotCommand("detail_items_with_graph", "Send all graphs related to problem"),
        BotCommand("send_graph", "Get Graph by item ID")
        ]
    set_commands = bot.set_my_commands(commands=commands)
    return set_commands
