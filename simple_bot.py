from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import stf_parser
import database_script
import re

monitoring_list = dict()


def start(bot, update):
    update.message.reply_text('Hi, @{}!'.format(update.effective_user.username))
    if database_script.check_user_to_be_in_db(update.effective_user.username):
        update.message.reply_text('Let\'s get familiar with you')


def count_answers(bot, update, args):
    html = stf_parser.get_html_doc(args[0])
    if html is None:
        update.message.reply_text("Connection error")

    answer = stf_parser.get_answer_quantity(html)
    if answer is None:
        update.message.reply_text("It is not stackoverflow question link")
    update.message.reply_text(answer)


def form_link(question_id):
    return "https://stackoverflow.com/questions/" + str(question_id) + '/'


def callback_check_question(bot, job):
    for name, questions in monitoring_list.items():
        user_id = database_script.get_user_id(name)
        for question_id in questions:
            new_answer_quantity = \
                stf_parser.get_answer_quantity(form_link(question_id))
            if database_script.compare_answers(user_id,
                                               question_id,
                                               new_answer_quantity):
                continue

            text_message = "New answers \n(\"%s\")" \
                           % (form_link(question_id))
        bot.send_message(chat_id='@' + name, text=text_message)


def add_question(bot, update, args):
    question_id = 0
    try:
        question_id = int(args[0])
    except Exception:
        question_id = int(re.search(r'/[^0-9]*/', args[0]).group(0))
    user_name = update.effective_user.username
    monitoring_list[user_name].add(question_id)
    database_script.add_question(question_id)


def del_question(bot, update, args):
    """Delete the question from monitoring list"""
    question_id = 0
    try:
        question_id = int(args[0])
    except Exception:
        question_id = int(re.search(r'/[^0-9]*/', args[0]).group(0))
    try:
        user_name = update.effective_user.username
        monitoring_list[user_name].remove(question_id)
        user_id = database_script.get_user_id(user_name)
        database_script.delete_question(user_id, question_id)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Successfully deleted question")
    except Exception:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Sorry, no question to delete")


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='It is wrong command')


def fill_monitoring_list():
    """Fill monitoring list"""
    names = database_script.get_all_user_names()
    for name in names:
        monitoring_list[name] = database_script.get_question_by_user_id(name)


def main():
    updater = Updater(open('token').read())
    dp = updater.dispatcher
    fill_monitoring_list()

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('count_answers',
                                  count_answers, pass_args=True))
    dp.add_handler(CommandHandler('add_question',
                                  add_question, pass_args=True))
    dp.add_handler(CommandHandler('del_question',
                                  del_question, pass_args=True))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.job_queue.run_repeating(callback_check_question,
                                    interval=60,
                                    first=0)
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
