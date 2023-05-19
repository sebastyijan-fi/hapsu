# Hapsu Discord Bot

Hapsu is a Discord bot that uses OpenAI's Language Model (3.5) to assist you in a variety of tasks. Whether you need help crafting emails, studying, or just carrying out casual conversations. 

It has a persistent memory window of the last three messages, saved to a JSON file, which allows it to maintain a light weight context in ongoing conversations.

Its setup process is straightforward, follow the [wiki](https://github.com/sebastyijan-fi/hapsu/wiki).

## Why Use Hapsu?

- **Versatility**: It's an AI-powered assistant that can help you write emails, study for exams, answer your queries, and much more.
  
- **Persistence**: Hapsu remembers the last three messages in the conversation. This is a light weight way to maintain the context.
  
- **Ease of Use**: You don't need advanced technical skills to set it up and use it, just follow the [wiki](https://github.com/sebastyijan-fi/hapsu/wiki)..

## Usage Guide

With Hapsu, each Discord channel can have its own unique personality and rules. The ask, role, and rule commands are customizable for every channel.

Here are the commands you can use:

- `.ask`: Use this command to ask Hapsu a question. Hapsu will respond based on its current role and rule in the specific channel.
- `.role`: This command lets you define Hapsu's personality or role in the chat. For example, `.role Pretend you are a Pirate` would instruct Hapsu to behave as a Pirate.
- `.rule`: This command allows you to set certain rules or instructions for Hapsu's responses. For example, `.rule Answer in 60 words max` would instruct Hapsu to answer with maximum of 60 words. Note that this command is part of the user message, but not part of the conversation history.
- `.helper`: Use this command to display a list of available commands in Discord.

Each channel has its own settings for `role` and `rule`, and maintains its own message history, Experiment with these commands to see what works best for you!

## Quick Setup recap

Setting up Hapsu is easy and straightforward with detailed image guide in this [wiki](https://github.com/sebastyijan-fi/hapsu/wiki). 

1. **Create Necessary Accounts**: Follow the image instructions.

2. **Set Up a Server**: Follow the image instructions.

3. **Run the Script in terminal**:

```bash
sudo curl -H 'Cache-Control: no-cache' -O https://raw.githubusercontent.com/sebastyijan-fi/hapsu/github/run_bot.sh && chmod +x run_bot.sh && ./run_bot.sh
```

This command will download the `run_bot.sh` script from the repository, make it executable, and run it. The script will:

- Install necessary dependencies.
- Prompt you to enter your OpenAI API keys and Discord Bot token with nano editor.
- Save these keys to a `.env` file.
- Keep everything updated with a cronjob.
- Start the bot and keep it running.





