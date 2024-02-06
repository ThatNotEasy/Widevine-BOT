import telebot
import getmac
import requests
import json
from telebot import types
from modules.logging import setup_logging
from modules.config import load_configurations

config = load_configurations()
logger = setup_logging()

TOKEN = config["TELEGRAM"]["TOKEN"]
AUTHORIZED_USER_IDS = json.loads(config["TELEGRAM"]["ID"])
ENDPOINT = config["API"]["ENDPOINT"]

bot = telebot.TeleBot(TOKEN)

start_menu_markup = types.InlineKeyboardMarkup(row_width=2)
astrogo_button = types.InlineKeyboardButton("🔓 ASTRO GO", callback_data='astrogo_callback')
netflix_button = types.InlineKeyboardButton("🔓 NETFLIX", callback_data='netflix_callback')
viu_button = types.InlineKeyboardButton("🔓 VIU", callback_data='viu_callback')
start_menu_markup.add(astrogo_button, netflix_button, viu_button)


def get_user_ip():
    try:
        url = "https://ipv4.jsonip.com/"
        response = requests.get(url)
        response.raise_for_status()
        ip_address = response.json()["ip"]
        return ip_address
    except requests.RequestException as e:
        logger.error(f"Error fetching IP address: {e}")
        return None

def get_user_mac():
    try:
        mac_address = getmac.get_mac_address()
        return mac_address
    except Exception as e:
        logger.error(f"Error fetching MAC address: {e}")
        return None

@bot.message_handler(commands=['start', 'stop', 'about', 'help', 'payment'])
def handle_commands(message):
    user_id = message.from_user.id

    if message.text.startswith('/start'):
        user_id, username, chat_id = message.from_user.id, message.from_user.username, message.chat.id
        ip_address, mac_address = get_user_ip(), get_user_mac()

        welcome_message = (
            f"👋 Hello there! Welcome to the Widevine Extractor BOT.\n\n"
            f"UserID: {user_id}\n"
            f"Username: {username}\n\n"
            # f"IP Address: {ip_address}\n"
            # f"MAC Address: {mac_address}\n\n"
            "Explore the following features:\n"
            "- Need assistance? Just type /help anytime.\n\n"
            f"- Maxis Sabah BOT: https://t.me/maxshits_bot\n"
            f"- Author: https://t.me/SurpriseMTFK"
        )

        bot.send_message(chat_id, welcome_message, reply_markup=start_menu_markup)
        logger.info(f"User {user_id} ({username}) started the bot.")

    elif message.text.startswith('/stop'):
        logger.info(f"User {user_id} stopped the bot.")
        bot.send_message(message.chat.id, "⛔ The bot has been stopped. If you have questions, feel free to start it again.")

    elif message.text.startswith('/about'):
        logger.info(f"User {user_id} requested information about the bot.")
        bot.send_message(message.chat.id, "🤖 Widevine Extractor BOT is designed to help you decrypt VOD content. "
                                          "Feel free to explore its features.")

    elif message.text.startswith('/help'):
        logger.info(f"User {user_id} requested help.")
        help_message = (
            "📋 Command list:\n"
            "/start - Start the bot\n"
            "/stop - Stop the bot\n"
            "/about - About the bot\n"
            "/help - Display this help message\n"
            "/payment - Initiate a payment (coming soon)"
        )
        bot.send_message(message.chat.id, help_message)

    elif message.text.startswith('/payment'):
        logger.info(f"User {user_id} initiated a payment. (Payment feature coming soon)")

        # Check if the user is authorized
        if user_id not in AUTHORIZED_USER_IDS:
            send_unauthorized_image(message.chat.id, user_id)
        else:
            bot.send_message(message.chat.id, "💳 The payment feature is currently under development. Stay tuned!")

def send_unauthorized_image(chat_id, user_id):
    qr_code_path = 'qrcode.png'
    with open(qr_code_path, 'rb') as qr_code_image:
        bot.send_photo(
            chat_id,
            qr_code_image,
            caption="🚫 Access Denied!\n\n"
                    "Oops! It seems like you don't have full access to this bot's features. "
                    "To get full access, please follow these steps:\n\n"
                    "1. Scan the QR Code below with your Touch'nGo app to make the payment.\n"
                    "2. Take a screenshot of the transaction.\n"
                    "3. Send the screenshot along with your Telegram user ID to get full access.\n\n"
                    "Thank you for your cooperation!",
        )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    # Remove the inline keyboard after any button is clicked
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=None)

    if call.data == 'astrogo_callback':
        logger.info(f"User {user_id} clicked 'Decrypt VOD' button.")
        options_markup = types.InlineKeyboardMarkup(row_width=2)
        buttons = [
            types.InlineKeyboardButton("🔑 Season/Episode Decrypt", callback_data='single_decrypt'),
            types.InlineKeyboardButton("🎬 Movie Decrypt", callback_data='massive_decrypt'),
            types.InlineKeyboardButton("📺 Channel Decrypt", callback_data='channel_decrypt'),
        ]
        options_markup.add(*buttons)
        bot.send_message(chat_id, "Choose the decryption option:", reply_markup=options_markup)

    elif call.data == 'single_decrypt':
        if str(user_id) not in map(str, AUTHORIZED_USER_IDS):
            return send_unauthorized_image(chat_id, user_id)
        else:
            logger.info(f"User {user_id} selected 'Season/Episode Decrypt' option.")
            msg = bot.send_message(chat_id, "🔑 Please provide Season/Show (Episode) URL/ID:")
            bot.register_next_step_handler(msg, lambda m: perform_single_decrypt(user_id, m, options_markup))

    elif call.data == 'massive_decrypt':
        if str(user_id) not in map(str, AUTHORIZED_USER_IDS):
            return send_unauthorized_image(chat_id, user_id)
        else:
            logger.info(f"User {user_id} selected 'Movie Decrypt' option.")
            msg = bot.send_message(chat_id, "🔑 Please provide the Movie VOD URL/ID:")
            bot.register_next_step_handler(msg, lambda m: perform_massive_decrypt(user_id, m, options_markup))

    elif call.data == 'channel_decrypt':
        if str(user_id) not in map(str, AUTHORIZED_USER_IDS):
            return send_unauthorized_image(chat_id, user_id)
        else:
            logger.info(f"User {user_id} selected 'Channel Decrypt' option.")
            msg = bot.send_message(chat_id, "🔑 Please provide the Channel ID:")
            bot.register_next_step_handler(msg, lambda m: perform_channel_decrypt(user_id, m, options_markup))
    else:
        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)

def perform_single_decrypt(user_id, message, options_markup):
    try:
        show_id_payload = {"show_id": message.text, "JWTs": message.text}
        show_url = f"{ENDPOINT}/dev/widevine/decryptShowVod"

        bot.send_message(user_id, "Please be patient .. ❗️")

        response = requests.post(show_url, json=show_id_payload)
        response.raise_for_status()

        response_data = response.json().get('responseData', {})
        if response_data:
            key = response_data.get('key')
            kid = response_data.get('kid')
            mpd_url = response_data.get('mpdURL')

            success_message = (
                f"🔓 Decryption request successful!\n\n"
                f"Key: {key}\n"
                f"KID: {kid}\n"
                f"MPD: {mpd_url}\n\n"
                "You can use this information for further playback."
            )

            bot.send_message(user_id, success_message)
            logger.info(f"Decryption successful for user {user_id}: Key={key}, KID={kid}, MPD={mpd_url}")
        else:
            bot.send_message(user_id, "❌ Decryption response format is invalid. Please try again later.", reply_markup=options_markup)

    except requests.RequestException as e:
        logger.error(f"Error sending KID Key request for user {user_id}: {e}")
        bot.send_message(user_id, "❌ An error occurred while processing your request. Please try again later.", reply_markup=options_markup)

def perform_massive_decrypt(user_id, message, options_markup):
    try:
        vod_id_payload = {"vod_id": message.text, "JWTs": message.text}
        vod_url = f"{ENDPOINT}/dev/widevine/decryptVod"
        bot.send_message(user_id, "Please be patient .. ❗️")

        response = requests.post(vod_url, json=vod_id_payload)
        response.raise_for_status()

        response_data = response.json().get('responseData', {})
        if response_data:
            key = response_data.get('key')
            kid = response_data.get('kid')
            mpd_url = response_data.get('mpdURL')

            success_message = (
                f"🔓 Decryption request successful!\n\n"
                f"Key: {key}\n"
                f"KID: {kid}\n"
                f"MPD: {mpd_url}\n\n"
                "You can use this information for further playback."
            )

            bot.send_message(user_id, success_message)
            logger.info(f"Decryption successful for user {user_id}: Key={key}, KID={kid}, MPD={mpd_url}")
        else:
            bot.send_message(user_id, "❌ Decryption response format is invalid. Please try again later.", reply_markup=options_markup)

    except requests.RequestException as e:
        logger.error(f"Error sending KID Key request for user {user_id}: {e}")
        bot.send_message(user_id, "❌ An error occurred while processing your request. Please try again later.", reply_markup=options_markup)

def perform_channel_decrypt(user_id, message, options_markup):
    try:
        channel_id_payload = {"channel_id": message.text, "JWTs": message.text}
        channel_url = f"{ENDPOINT}/dev/widevine/decryptChannel"
        bot.send_message(user_id, "Please be patient .. ❗️")

        response = requests.post(channel_url, json=channel_id_payload)
        response.raise_for_status()

        response_data = response.json().get('responseData', {})
        if response_data:
            key = response_data.get('key')
            kid = response_data.get('kid')
            mpd_url = response_data.get('mpdURL')

            success_message = (
                f"🔓 Decryption request successful!\n\n"
                f"Key: {key}\n"
                f"KID: {kid}\n"
                f"MPD: {mpd_url}\n\n"
                "You can use this information for further playback."
            )

            bot.send_message(user_id, success_message)
            logger.info(f"Decryption successful for user {user_id}: Key={key}, KID={kid}, MPD={mpd_url}")
        else:
            bot.send_message(user_id, "❌ Decryption response format is invalid. Please try again later.", reply_markup=options_markup)

    except requests.RequestException as e:
        logger.error(f"Error sending KID Key request for user {user_id}: {e}")
        bot.send_message(user_id, "❌ An error occurred while processing your request. Please try again later.", reply_markup=options_markup)

logger.info("WIDEVINE BOT START")

# Start polling
bot.polling()