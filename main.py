import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
import openai
import whisper
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Set up OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

model = whisper.load_model('base.en', download_root="./.cached")


# Define a function to handle incoming messages to translate
async def handle_translation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the user's message
    message = update.message.text

    message = message.replace("/translate", "")

    # Use the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English."},
            {"role": "user", "content": "can you translate for \"Bạn có thể tới đây sớm không?\" in English"},
            {"role": "assistant", "content": "The translation for \"Bạn có thể tới đây sớm không?\" in English is \"Can you come here early?\"."},
            {"role": "user", "content": "vòng đeo tay"},
            {"role": "assistant", "content": "The translation for \"vòng đeo tay\" in English is \"bracelet\" or \"wristband\"."},
            {"role": "user", "content": message}],
        temperature=0,)

    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=response.choices[0].message.content,
        parse_mode='markdown')


# Define a function to handle incoming message to ask everything
async def handle_ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message.text
    msg = msg.replace("/ask", "")

    prompt = "As an AI language model, I have a vast amount of knowledge and can provide you with information on a wide range of topics. So, please feel free to ask me anything you want to know! Whether it's about science, history, geography, art, culture, or any other subject, I'm here to help you learn and expand your knowledge. So, go ahead and ask me any question you have in mind, and I'll do my best to provide you with a helpful answer."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": msg}
        ]
    )
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=response.choices[0].message.content
    )


# Define function to handle incoming voice to transcribe
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    voice = update.message.voice

    file = await context.bot.get_file(voice.file_id)
    oga = await file.download_to_drive()

    response = model.transcribe(str(Path(oga)), fp16=False)

    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=response['text'])

    os.remove(oga)


# main function
def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    bot = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    bot.add_handler(CommandHandler('translation', handle_translation))
    bot.add_handler(CommandHandler("ask", handle_ask))
    bot.add_handler(MessageHandler(filters.VOICE, handle_audio))
    bot.run_polling()


# Run the script
if __name__ == "__main__":
    print('bot started')
    main()
