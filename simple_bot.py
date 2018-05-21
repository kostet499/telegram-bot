from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import stf_parser
import database_script
import re
import collections
import config


def start(bot, update):
    update.message.reply_text('Hi!')
    if database_script.check_user_to_be_in_db(update.message.chat_id,
                                              update.effective_user.username):
        update.message.reply_text('Let\'s get familiar with you')


def count_answers(bot, update, args):
    question_id = retreive_question_id(args[0])
    answer = stf_parser.get_answer_quantity(form_link(question_id), True)
    if answer is None:
        update.message.reply_text("It is not stackoverflow question link")
    update.message.reply_text(str(answer))


def form_link(question_id):
    return "https://stackoverflow.com/questions/" + str(question_id) + '/'


def retreive_question_id(link):
    question_id = 0
    try:
        question_id = int(link)
    except Exception:
        question_id = int(
            re.search(r'[0-9]+', re.search(r'/[0-9]+/', link).group(0)).group(
                0))
    return question_id


def callback_check_question(bot, job):
    deleted_question = collections.defaultdict(int)
    for chat_id, questions in config.monitoring_list.items():
        for question_id in questions:
            new_answer_quantity = stf_parser.get_answer_quantity(
                form_link(question_id), True)
            if new_answer_quantity is None:
                bot.send_message(chat_id=chat_id,
                                 text="Bad link deleted " + form_link(
                                     question_id))
                database_script.delete_question(chat_id, question_id)
                deleted_question[chat_id] = question_id
                continue
            if database_script.compare_answers(chat_id,
                                               question_id,
                                               new_answer_quantity):
                continue

            text_message = "New answers \n(\"%s\")" % (form_link(question_id))
            bot.send_message(chat_id=chat_id, text=text_message)

    for chat_id, question_id in deleted_question.items():
        config.monitoring_list[chat_id].remove(question_id)


def add_question(bot, update, args):
    """Add question to db and monitoring list"""
    question_id = retreive_question_id(args[0])
    ans_count = stf_parser.get_answer_quantity(form_link(question_id), True)
    if ans_count is None:
        update.message.reply_text("Link is bad")
        return
    chat_id = update.message.chat_id
    config.monitoring_list[chat_id].add(question_id)
    database_script.add_question(question_id)
    database_script.insert_into_user_question(chat_id, question_id, ans_count)
    message = 'Answers ' + str(ans_count)
    update.message.reply_text(message)


def del_question(bot, update, args):
    """Delete the question from db and monitoring list"""
    question_id = retreive_question_id(args[0])
    try:
        chat_id = update.message.chat_id
        config.monitoring_list[chat_id].remove(question_id)
        database_script.delete_question(chat_id, question_id)
        bot.send_message(chat_id=chat_id,
                         text="Successfully deleted question")
    except Exception:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Sorry, no question to delete")


def unknown(bot, update):
    """Operate with unknown command"""
    bot.send_message(chat_id=update.message.chat_id,
                     text='It is wrong command')


def fill_monitoring_list():
    """Load user data from database"""
    for chat_id in database_script.get_all_user_id():
        config.monitoring_list[chat_id] = set(
            database_script.get_question_by_user_id(chat_id))


def main():
    updater = Updater(open('token').read())
    dp = updater.dispatcher

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
                                    interval=10,
                                    first=10)
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
