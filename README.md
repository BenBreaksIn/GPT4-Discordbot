# Chloe - Your Discord AI Assistant

Chloe is a highly interactive Discord bot developed using OpenAI's GPT-4 language model. With capabilities ranging from simple conversations to code generation, Chloe brings the power of advanced AI to your Discord server.

## Features

- Natural language conversations: Chloe uses the GPT-4 model to generate human-like text based on the prompts it receives.
- PDF text extraction: Chloe can extract and read text from PDF files sent as attachments in direct messages.
- User cooldowns: To prevent spam and ensure fair usage, Chloe implements a user cooldown system. Users must wait a certain amount of time between successive requests.

## Usage

1. Direct messages: You can directly message Chloe and it will respond to your prompts. If your message includes a PDF attachment, Chloe will read and respond to the text content in the PDF.
2. Mentions: You can mention Chloe in any server channel to interact with it. Just replace `@chloe` with the bot's username.

## Commands

- `!chloe_help`: Provides a brief description of how to interact with Chloe.

## Setup

Here are the steps to get Chloe running on your local machine for development and testing purposes:

1. Clone this repository to your local machine.
2. Install the required Python packages using pip: `pip install -r requirements.txt`. This includes the discord.py, aiohttp, and pdfplumber packages, among others.
3. Create a .env file in the root directory of the project. This file should contain your OpenAI API key and Discord bot token, like so:

   ```
   OPENAI_API_KEY=your_openai_api_key
   DISCORD_TOKEN=your_discord_bot_token
   ```

4. Run `python bot.py` to start the bot.

## Contributing

We welcome contributions of all kinds to Chloe. Please feel free to submit a pull request or open an issue if you encounter any problems or have any suggestions for improvements.

## License

Chloe is released under the MIT License. See the LICENSE file for more details.
