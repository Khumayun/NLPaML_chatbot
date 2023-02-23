import telepot
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


def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        message = msg['text']
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
            bot.sendMessage(chat_id, best_sent.text)
        else:
            bot.sendMessage(chat_id, "Sorry, I couldn't find an answer to your question.")

# Replace YOUR_BOT_TOKEN with your actual bot token
bot = telepot.Bot('572928607:AAGbOuBN9EhePacIUg-h3NtlPAV2I4P1XWQ')
bot.message_loop(handle_message)

print('Listening for messages...')
while True:
    pass
