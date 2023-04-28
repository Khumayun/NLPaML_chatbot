import requests
from bs4 import BeautifulSoup
import spacy
import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Download and load the NLP model
nlp = spacy.load('en_core_web_sm')

# Extract the text from the documentation index
url = 'https://raw.githubusercontent.com/sphinx-doc/sphinx/master/doc/index.rst'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
text = soup.get_text()

# Process the text with the NLP model
doc = nlp(text)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.message.from_user
    logging.info(f"Received command /start from {user.first_name} ({user.username})")
    update.message.reply_text('Hi! I can help you with your documentation questions. Just send me a message and I will do my best to help you.')


def help(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    user = update.message.from_user
    logging.info(f"Received command /help from {user.first_name} ({user.username})")
    update.message.reply_text('Just send me a message with your question and I will do my best to help you!')


# Define the echo function
def echo(update, context):
    """Echoes the user's message."""
    message = update.message.text
    chat_type = update.message.chat.type
    if chat_type == 'private':
        # If the message was sent in a private chat, process it with the NLP model
        user_doc = nlp(message)
        # Find the most relevant sentence in the documentation
        best_sent = None
        best_score = 0
        for sent in doc.sents:
            score = user_doc.similarity(sent)
            if score > best_score:
                best_sent = sent
                best_score = score
        # Send the best sentence as a reply
        if best_sent is not None:
            update.message.reply_text(best_sent.text)
        else:
            update.message.reply_text("Sorry, I couldn't find an answer to your question.")
    elif chat_type == 'group':
        # If the message was sent in a group chat, check if the bot was mentioned
        message_text = message.lower()
        bot_username = context.bot.username.lower()
        if f'@{bot_username}' in message_text:
            # If the bot was mentioned, process the message with the NLP model
            user_doc = nlp(message)
            # Find the most relevant sentence in the documentation
            best_sent = None
            best_score = 0
            for sent in doc.sents:
                score = user_doc.similarity(sent)
                if score > best_score:
                    best_sent = sent
                    best_score = score
            # Send the best sentence as a reply
            if best_sent is not None:
                update.message.reply_text(best_sent.text)
                logging.info(
                    f"{update.message.from_user.name} ({update.message.from_user.username}): {update.message.text} -> {best_sent.text}")
            else:
                update.message.reply_text("Sorry, I couldn't find an answer to your question.")
                logging.info(
                    f"{update.message.from_user.name} ({update.message.from_user.username}): {update.message.text} -> No relevant sentence found.")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token='572928607:AAExZtc_sCMwHltg4d2Rump8RNqIxcxKLAM')

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    # Add message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()
    logging.info("Bot started. Press Ctrl-C to stop.")

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
