import os
from functools import wraps
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from botconf import main as config_bot
from ZBXfunctions import problem_by_severity, get_problem_detail, list_all_items_problem, item_detail
from ZBXfunctions import get_problem_host, problem_detail, item_graph
import logging


ADMINS = [111111111111,22222222222222,33333333333]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


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
def active_problems(update, context):
    user = update.message.from_user
    logger.info(f"User {user.first_name} started the conversation")
    problems = problem_by_severity()
    keyboard = []
    for problem in problems:
        name = get_problem_detail(problem)
        hostname = get_problem_host(problem)
        objectid = problem
        list = [InlineKeyboardButton(f"{hostname} - {name}", callback_data=f"{objectid}")]
        keyboard.append(list)
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f'Hello, {user.first_name}. Tap a problem to view it details...', reply_markup=reply_markup)

def button(update,context):
    query = update.callback_query
    query.answer()
    itemlist = list_all_items_problem(int(query.data))
    problemtext = problem_detail(query.data)
    context.bot.send_message(chat_id=query.message.chat_id, text=problemtext)
    for item in itemlist:
        text = item_detail(item)
        context.bot.send_message(chat_id=query.message.chat_id, text=text)
        photo = item_graph(item)
        context.bot.send_photo(chat_id=query.message.chat_id, photo=open(f'{photo}', 'rb'))

token = os.getenv('TGTOKEN')

def main():
    conf = config_bot()
    print(conf)
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('active_problems', active_problems))
    dispatcher.add_handler(CallbackQueryHandler(button))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
