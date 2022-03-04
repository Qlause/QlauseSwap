from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from radixnetwork.wallet import Wallet
from radixnetwork.transaction import Transaction

updater = Updater(token='5168661312:AAFqcxksFOkJ0F1KhUQC7bCcOHyed0QrG0k', use_context=True)

from telegram import InlineQueryResultArticle, InputTextMessageContent
def inline_caps(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

from telegram.ext import InlineQueryHandler
inline_caps_handler = InlineQueryHandler(inline_caps)
updater.dispatcher.add_handler(inline_caps_handler)

updater.idle()