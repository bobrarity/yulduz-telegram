# Yulduz - Voice Assistant Telegram Bot

## Overview

Initially, the project was build as a voice-assistant that provides the information related to MohirDev company (courses, mentors, skills etc). This project integrates a Telegram chatbot with OpenAI's language model (LLM) to provide conversational responses to
user queries. The chatbot is capable of processing text and voice messages (by using speech recognition) in multiple languages (English, Russian, Uzbek) and generating appropriate responses
using the OpenAI language model + MohirAI (in case of Uzbek language).

## Setup

1. **Clone the Repository**: `git clone url_to_the_project`
2. **Install Dependencies**: `pip install requirements.txt`
3. **Set up Telegram Bot**:

- Create a new bot on Telegram using the BotFather and obtain the API token.
- Replace `'TELEGRAM_API_KEY'` and `'MOHIR_API_KEY'` with your actual API keys.

## Usage

1. **Run the Bot**:
2. **Interact with the Bot**:

- Start a conversation by choosing the language and sending either the text or voice message to the bot in your Telegram app.
- Send messages to the bot and it will reply with responses (text messages).

## Functionality

- The bot can process messages in multiple languages and respond accordingly.
- Messages sent by users are processed by the appropriate language model to generate conversational responses.
- The bot replies to user messages in real-time within the Telegram chat interface.

## Configuration

- Paste the required API KEYS (OpenAI and MohirAI ones)