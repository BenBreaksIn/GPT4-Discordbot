import json
import re
import time
import discord
import aiohttp
from discord.ext import commands
import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Set API key and endpoint
api_key = os.environ.get('OPENAI_API_KEY')
api_url = "https://api.openai.com/v1/chat/completions"

# Initialize bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# Rate limiting
user_cooldowns = {}


def preprocess_code(code):
    # Remove any non-alphanumeric characters
    code = re.sub(r'\W+', ' ', code)

    # Remove any discord bot token-like strings
    code = re.sub(r'\b[a-zA-Z0-9_]{24}\.[a-zA-Z0-9_]{6}\.[a-zA-Z0-9_]{27}\b', 'DISCORD_BOT_TOKEN', code)
    # Remove any placeholder API keys
    code = re.sub(r'\b[a-zA-Z0-9_]{32}\b', 'API_KEY', code)

    return code


async def send_request(prompt):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    data = {
        "model": "gpt-4",
        "messages": [{"role": "system", "content": "You are talking to Chloe, an AI assistant."},
                     {"role": "user", "content": prompt}],
        "max_tokens": 6000,
        "n": 1,
        "temperature": 0.8
    }

    json_data = json.dumps(data, ensure_ascii=False).encode('utf8')
    escaped_data = json_data.decode('utf8')

    async with aiohttp.ClientSession() as session:
        response = None
        while True:
            try:
                async with session.post(api_url, headers=headers, data=escaped_data) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientResponseError as e:
                if response and response.status == 429:
                    retry_after = int(response.headers.get("Retry-After", "1"))
                    print(f"Rate limited. Retrying in {retry_after} seconds...")
                    time.sleep(retry_after)
                else:
                    print(f"Error occurred: {e}")
                    return None
            except Exception as e:
                print(f"Error occurred: {e}")
                return None


def parse_response(response_json):
    if response_json is None:
        return "An error occurred while processing your request. Please try again."
    try:
        return response_json["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return "An error occurred while processing your request. Please try again."


async def gpt4_response(prompt):
    prompt = preprocess_code(prompt)
    response_json = await send_request(prompt)
    return parse_response(response_json)


# Cooldown check
def is_on_cooldown(user_id):
    cooldown_time = 7  # Seconds
    if user_id in user_cooldowns:
        remaining_time = cooldown_time - (time.time() - user_cooldowns[user_id])
        if remaining_time > 0:
            return remaining_time
    user_cooldowns[user_id] = time.time()
    return False


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
        prompt = message.content
        remaining_time = is_on_cooldown(message.author.id)
        if remaining_time:
            await message.channel.send(f"You're on cooldown. Please wait {remaining_time:.0f} seconds.")
            return
        async with message.channel.typing():
            response = await gpt4_response(prompt)
            # If the message is too long, split it
            if len(response) > 2000:
                responses = [response[i:i + 2000] for i in range(0, len(response), 2000)]
                for res in responses:
                    await message.channel.send(res)
            else:
                await message.channel.send(response)
            user_cooldowns[message.author.id] = time.time()
    elif bot.user in message.mentions:
        prompt = message.content.replace(f"@{bot.user.name}", "").strip()
        remaining_time = is_on_cooldown(message.author.id)
        if remaining_time:
            await message.channel.send(f"You're on cooldown. Please wait {remaining_time:.0f} seconds.")
            return
        async with message.channel.typing():
            response = await gpt4_response(prompt)
            # If the message is too long, split it
            if len(response) > 2000:
                responses = [response[i:i + 2000] for i in range(0, len(response), 2000)]
                for res in responses:
                    await message.channel.send(res)
            else:
                await message.channel.send(response)
            user_cooldowns[message.author.id] = time.time()

    await bot.process_commands(message)


@bot.command(name="chloe_help")
async def chloe_help(ctx):
    help_message = (
        "Use the `@chloe` or `!chloe` followed by your message to interact with Chloe, the AI assistant. "
        "For example: `!chloe How's the weather today?`")
    await ctx.send(help_message)


bot.run(os.environ.get("DISCORD_TOKEN"))
