import collections
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import stf_parser
import database_script

MARKS = collections.defaultdict(list)


def start(bot, update):
    update.message.reply_text('Hi, @{}!'.format(update.effective_user.username))
    database_script.check_user_to_be_in_db(update.effective_user.username)


def echo(bot, update):
    update.message.reply_text(update.message.text)


def add_mark(bot, update, args):
    if update.effective_user.username == 'wokinshopash':
        MARKS[args[0]].append(int(args[1]))
        update.message.reply_text(
            'Successfully added {} for @{}'.format(args[1], args[0]))
    else:
        update.message.reply_text('Sorry, u can\'t add marks! :(')


def count_answers(bot, update, args):
    html = stf_parser.get_html_doc(args[0])
    if html is None:
        update.message.reply_text("Connection error")

    answer = stf_parser.get_answer_quantity(html)
    if answer is None:
        update.message.reply_text("It is not stackoverflow question link")
    update.message.reply_text(answer)


def show_marks(bot, update, args):
    if update.effective_user.username == 'wokinshopash':
        if not args:
            # Show ALL Marks
            response_lines = ['All marks:']
            for user, marks in sorted(MARKS.items()):
                response_lines.append('@{}: {} (mean: {})'.format(user,
                                                                  ', '.join(
                                                                      map(str,
                                                                          marks)),
                                                                  sum(
                                                                      marks) / len(
                                                                      marks)))
            update.message.reply_text('\n'.join(response_lines))
        else:
            # Show marks for given person
            user = args[0]
            if user in MARKS:
                marks = MARKS[args[0]]
                response = 'Marks: {}\n*Mean*: {}'.format(
                    ', '.join(map(str, marks)), sum(marks) / len(marks))
                update.message.reply_markdown(response)
            else:
                update.message.reply_text(
                    'Sorry, no marks for @{}'.format(user))
    else:
        # Show marks for user
        user = update.effective_user.username
        if user in MARKS:
            marks = MARKS[user]
            response = 'Marks: {}\n*Mean*: {})'.format(
                ', '.join(map(str, marks)), sum(marks) / len(marks))
            update.message.reply_markdown(response)
            if sum(marks) / len(marks) < 5:
                update.message.reply_sticker('CAADAgADGAIAAmkSAAJWHyklsyrFUQI')
        else:
            update.message.reply_text('Sorry, no marks for yo')


def main():
    updater = Updater(open('token').read())
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add_mark", add_mark, pass_args=True))
    dp.add_handler(CommandHandler("show_marks", show_marks, pass_args=True))
    dp.add_handler(CommandHandler('count_answers',
                                  count_answers, pass_args=True))
    # # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
