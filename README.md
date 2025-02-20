# Lon-Lon-MilkBar-Support-AI
This is the repository for Lon Lon Milkbar Support AI. Here you can find all of the code needed to build this AI.

**There are three important folders in this project listed below:**

## [The AI](AI)
- This is the actual AI that connects to Gemini or Ollama.

## [Discord Bot](Discord-Bot)
- This is the code for the discord bot.

## [Website](Website)
- This is the code for the website.

## How to run:
(I would recommend doing all of these in screen sessions if you're on Linux).

# The AI
- Download python and add it to PATH (there should be an option when you first launch the installer).
- Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and click 'Create API Key'.
- Open 'app.py' and put in the API key.
- Run `pip install -r requirements.txt` then `python3 app.py` in a Command Prompt or Terminal.

# The Discord Bot
- Download python and add it to PATH (there should be an option when you first launch the installer).
- Go to the [Discord Developer Portal](https://discord.com/developers/applications) and make a New Application.
- Go to the bot tab on the left side of the screen.
- Click 'Reset Token' and copy it.
- Open 'secrets.json' and put in the token.
- Run `python3 app.py` in a Command Prompt or Terminal.

# The Website
- Use a webserver like Apache2 if you want to self host it.
