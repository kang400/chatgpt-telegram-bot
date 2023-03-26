import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
import openai
from dotenv import load_dotenv
from pathlib import Path
import ffmpeg

load_dotenv()

# Set up OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define a function to handle incoming messages


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the user's message
    message = update.message.text

    # {"role": "system", "content": "You are a helpful assistant."},
    # Use the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English."},
            {"role": "user", "content": message}],
        temperature=0,)

    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=response.choices[0].message.content,
        parse_mode='markdown')
    
async def translate_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text

    prompt = """
        I want you to act as an English translator, spelling corrector and improver.
        I will speak to you in any language and you will detect the language,
        translate it and answer in the corrected and improved version of my text, in English.
        I want you to replace my simplified A0-level words and sentences with more beautiful and elegant,
        upper level English words and sentences. Keep the meaning same, but make them more literary.
        I want you to only reply the correction, the improvements and nothing else,
        do not write explanations.
        My first sentence is \"{}\""""
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt.format(message),
    )

    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=response.choices[0].text
    )

async def handle_davinci(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the user's message
    message = update.message.text

    # {"role": "system", "content": "You are a helpful assistant."},
    # Use the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English."},
            {"role": "user", "content": message}],
        temperature=0,)

    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=response.choices[0].message.content,
        parse_mode='markdown')
    
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    print("function working...")
    voice = update.message.voice

    file = await context.bot.get_file(voice.file_id)
    oga = await file.download_to_drive()

    # out = str(Path(oga)) + '.mp3'

    # ffmpeg.input(oga).output(out, format='mp3').run(capture_stdout=True)

    # f = open(out, 'rb')

    # response = openai.Audio.transcribe('whisper-1', f)

    # # remove cache file
    # os.remove(oga)
    # os.remove(out)

    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text=response.text)
    
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mess = update.message

    print(mess)
    
# def moderate_message(
#     message: str, user: str
# ) -> Tuple[str, str]:  # [flagged_str, blocked_str]
#     moderation_response = openai.Moderation.create(
#         input=message, model="text-moderation-latest"
#     )
#     category_scores = moderation_response.results[0]["category_scores"] or {}

#     blocked_str = ""
#     flagged_str = ""
#     for category, score in category_scores.items():
#         if score > MODERATION_VALUES_FOR_BLOCKED.get(category, 1.0):
#             blocked_str += f"({category}: {score})"
#             logger.info(f"blocked {user} {category} {score}")
#             break
#         if score > MODERATION_VALUES_FOR_FLAGGED.get(category, 1.0):
#             flagged_str += f"({category}: {score})"
#             logger.info(f"flagged {user} {category} {score}")
#     return (flagged_str, blocked_str)


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    bot = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    # application.add_handler(MessageHandler(filters.TEXT, handle_message))
    bot.add_handler(CommandHandler('husky', handle_message))
    bot.add_handler(CommandHandler('any2en', translate_prompt))
    bot.add_handler(MessageHandler(filters.VOICE, handle_audio))
    # bot.add_handler(MessageHandler(filters.ALL, handler))
    bot.run_polling()


if __name__ == "__main__":
    print('bot started')
    main()
