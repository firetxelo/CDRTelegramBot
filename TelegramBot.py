import os
from functools import wraps
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from botconf import main as config_bot
from ZBXfunctions import zbx_list_hostgroup
from ZBXfunctions import zbx_list_hosts_in_group
from ZBXfunctions import zbx_list_problems_by_hostid
from ZBXfunctions import get_graph_by_item_id
from ZBXfunctions import detail_items_related_to_problem
from ZBXfunctions import list_items_related_to_problem
from ZBXfunctions import get_item_name


ADMINS = [111111111,22222222,3333333]


def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ADMINS:
            message = (f"Unauthorized acess denied for {user_id}.")
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            return
        return func(update, context, *args, **kwargs)
    return wrapped


@restricted
def start(update, context):
    message = 'Seja bem vindo'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


@restricted
def echo(update, context):
    message = 'echo'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


@restricted
def unknown(update, context):
    message = 'unknown'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


@restricted
def list_hostgroup(update, context):
    message = zbx_list_hostgroup()
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

@restricted
def list_hosts(update, context):
    id = 0
    if context.args:
        id = context.args[0]
    message = zbx_list_hosts_in_group(id)
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

@restricted
def list_problems_by_host(update, context):
    id = 0
    if context.args:
        id = context.args[0]
    message = zbx_list_problems_by_hostid(id)
    context.bot.send_message(chat_id=update.message.chat_id, text=message)


@restricted
def send_graph(update, context):
    message = "Informe o ID do item"
    if len(context.args) == 2:
        itemid = context.args[0]
        time = context.args[1]
        message = get_graph_by_item_id(itemid, time)
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open(f'{message}', 'rb'))

    elif len(context.args) == 1:
        itemid = context.args[0]
        message = get_graph_by_item_id(itemid)
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open(f'{message}', 'rb'))
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=message)


@restricted
def detail_items_with_problem_id(update, context):
    id = 0
    if context.args:
        id = context.args[0]
    message = detail_items_related_to_problem(id)
    context.bot.send_message(chat_id=update.message.chat_id, text=message)


@restricted
def detail_items_with_graph(update, context):
    message = "Informe o ID do item"
    if context.args:
        id = context.args[0]
        listitems = list_items_related_to_problem(id)
        for item in listitems:
            message = get_item_name(item)
            context.bot.send_message(chat_id=update.message.chat_id, text=message)
            photo = get_graph_by_item_id(item)
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open(f'{photo}', 'rb'))
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=message)



token = os.getenv('TGTOKEN')

def main():
    conf = config_bot()
    print(conf)
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('list_hostgroup', list_hostgroup))
    dispatcher.add_handler(CommandHandler('list_hosts', list_hosts))
    dispatcher.add_handler(CommandHandler('list_problems_by_host', list_problems_by_host))
    dispatcher.add_handler(CommandHandler('detail_items_with_problem_id', detail_items_with_problem_id))
    dispatcher.add_handler(CommandHandler('detail_items_with_graph', detail_items_with_graph))
    dispatcher.add_handler(CommandHandler('send_graph', send_graph))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
