import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import spacy
import requests
from bs4 import BeautifulSoup


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

# Define a function to handle incoming messages
def handle_message(update, context):
    message = update.message.text
    # Process the user's message with the NLP model
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


def main():
    # Create an instance of the Updater class and pass in your bot's token
    updater = Updater(token='572928607:AAExZtc_sCMwHltg4d2Rump8RNqIxcxKLAM', use_context=True)
    # Get a reference to the dispatcher object
    dispatcher = updater.dispatcher
    # Register a message handler function
    message_handler = MessageHandler(Filters.text, handle_message)
    dispatcher.add_handler(message_handler)
    # Start polling for new messages
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
