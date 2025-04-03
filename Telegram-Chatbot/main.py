import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import openai
import os

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Check if API keys are loaded correctly
if not TELEGRAM_BOT_TOKEN or not openai.api_key:
    raise ValueError("Error: TELEGRAM_BOT_TOKEN or OPENAI_API_KEY not set in .env file")

# Logging
logging.basicConfig(level=logging.INFO)

# Class to Store Previous Responses
class Reference:
    """
    A class to store previous responses from the OpenAI API
    """
    def __init__(self) -> None:
        self.response = ""  # Corrected attribute name

reference = Reference()
model_name = "gpt-3.5-turbo"

# Initialize Bot and Dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot)

# Command to Clear Chat History
@dispatcher.message_handler(commands=['clear'])
async def command_clear_handler(message: types.Message):
    reference.response = ""  # Corrected logic
    await message.reply("History has been cleared.")

# Command to Start the Bot
@dispatcher.message_handler(commands=['start'])
async def command_start_handler(message: types.Message):
    await message.reply("Hi! I am an Echo Bot powered by Aiogram.")

# ChatGPT Message Handler
@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    logging.info(f">> USER: {message.text}")

    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "assistant", "content": reference.response},
                {"role": "user", "content": message.text}
            ]
        )

        reference.response = response['choices'][0]['message']['content']
        logging.info(f">> CHATGPT Response: {reference.response}")

        await message.reply(reference.response)

    except Exception as e:
        logging.error(f"Error in OpenAI API Call: {str(e)}")
        await message.reply("Sorry, there was an error processing your request.")

# Run the Bot
if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
    # executor.start_polling(dispatcher, skip_updates=False) # if we make it False then if for example the application is offline then it will used the users respones and reply when available
