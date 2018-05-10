from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import stf_parser
import database_script


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


def callback_check_question


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='It is wrong command')


def main():
    updater = Updater(open('token').read())
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('count_answers',
                                  count_answers, pass_args=True))
    dp.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
