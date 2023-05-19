# Hapsu Discord Bot

Hapsu is a versatile Discord bot that uses OpenAI's Language Model (LLM) to assist you in a variety of tasks. Whether you need help crafting emails, studying, or just carrying out casual conversations, Hapsu is your go-to assistant. It has a persistent memory window of the last three messages, saved to a JSON file, which allows it to maintain context in ongoing conversations.

Developed with a focus on user-friendliness, Hapsu is designed to be accessible to everyone. Its setup process is straightforward and requires only minimal technical knowledge.

## Why Use Hapsu?

- **Versatility**: Hapsu is not just an ordinary chatbot. It's an AI-powered assistant that can help you write emails, study for exams, answer your queries, and much more.
  
- **Persistence**: Hapsu remembers the last three messages in the conversation, maintaining the context and continuity.
  
- **Ease of Use**: I have strived to make Hapsu as easy to use as possible. You don't need advanced technical skills to set it up and use it.

## Usage Guide

Hapsu is designed to be flexible and adaptable to the needs of different channels. Here are some key commands you can use:

- `.kysy`: Use this command to ask Hapsu a question. Hapsu will respond based on its current settings and capabilities.
- `.hahmo`: This command lets you define Hapsu's personality or role in the chat. For example, `.hahmo Friendly Helper` would instruct Hapsu to behave as a friendly helper. This setting is specific to each channel, allowing for a customized experience.
- `.ohje`: This command allows you to set certain rules or instructions for Hapsu's responses. For example, `.ohje Respond in JSON format` would instruct Hapsu to format its responses in JSON. Note that this command is part of the user message, providing a more interactive and dynamic conversation.
- `.apua`: Use this command to display a list of available commands in Discord. It's a great way to learn what Hapsu can do or to remind yourself of a command.

Each channel has its own settings for `hahmo` and `ohje`, and maintains its own message history, providing a uniquely tailored experience for every channel. Explore and experiment with these commands to make Hapsu work best for your needs!

## Quick Setup

Setting up Hapsu on your Discord server is easy and straightforward with our detailed [wiki](https://github.com/sebastyijan-fi/hapsu/wiki). 

1. **Create Necessary Accounts**: Follow the instructions on our wiki to create the required accounts and obtain the necessary API keys.

2. **Set Up a Server**: Use our wiki to guide you through the process of setting up a server on DigitalOcean to host Hapsu.

If you already have your own server, accounts, and API keys, you can skip these steps and proceed to run the script:

3. **Run the Script**: 

```bash
sudo curl -H 'Cache-Control: no-cache' -O https://raw.githubusercontent.com/sebastyijan-fi/hapsu/github/run_bot.sh && chmod +x run_bot.sh && ./run_bot.sh
```

This command will download the `run_bot.sh` script from the repository, make it executable, and run it. The script will:

- Prompt you for your OpenAI and Discord Bot API keys.
- Save these keys to a `.env` file.
- Install necessary dependencies.
- Keep everything updated
- Start the bot.





