# Widevine Extractor BOT

This Telegram bot, called **Widevine Extractor BOT**, is designed to help users decrypt VOD (Video On Demand) content using the Widevine DRM system. It allows users to initiate decryption requests for various VOD platforms like ASTRO GO, HOTSTAR, and VIU.

## Prerequisites
Before using this bot, make sure you have the following:
- A Telegram account
- Access to the Widevine Extractor BOT
- Bearer Token (if required by the platform)

## Features
- **Start Menu**: Upon starting the bot, users are presented with a menu to choose from ASTRO GO, HOTSTAR, and VIU.
- **Authorization**: Certain features may require authorization. Unauthorized users are prompted to make a payment to gain access to these features.
- **Commands**:
  - `/start`: Start the bot and display the welcome message along with the start menu.
  - `/stop`: Stop the bot.
  - `/about`: Get information about the bot.
  - `/help`: Display a list of available commands.
  - `/payment`: Initiate a payment for accessing certain features (coming soon).
- **Decryption**:
  - Users can initiate decryption requests for series, movies, and channels.
  - The bot handles decryption requests by sending requests to the API endpoint for content decryption.
  - Decryption responses include the key, KID (Key ID), and MPD (Media Presentation Description) URL.

## Getting Started
1. Start the Widevine Extractor BOT by sending `/start` command.
2. Choose a platform (ASTRO GO, HOTSTAR, VIU) from the start menu.
3. Follow the on-screen instructions to proceed with decryption requests.

## Note
This bot is still under development, and some features may not be fully functional yet.

For more information, contact the [author](https://t.me/SurpriseMTFK).
