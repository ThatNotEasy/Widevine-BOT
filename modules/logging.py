import os, logging, socket, requests
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, types, executor
from colorama import Fore, Style, init

init(autoreset=True)

async def get_user_ip():
    try:
        # Get the user's external IP address using a public service
        response = requests.get('https://api64.ipify.org?format=json')
        data = response.json()
        external_ip = data.get('ip')

        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return external_ip, local_ip, hostname
    except Exception as e:
        print(f"Error getting user IP: {e}")
        return "Unknown", "Unknown", "Unknown"

async def response_ips(message: types.Message):
    external_ip, local_ip, hostname = await get_user_ip()
    welcome_text = (
        f"Hello, {message.from_user.username}!\n"
        f"Your Telegram ID: {message.from_user.id}\n"
        f"Your External IP address: {external_ip}\n"
        f"Your Local IP address: {local_ip}"
    )
    await message.reply(welcome_text, parse_mode=ParseMode.MARKDOWN)

def setup_logging():
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    logger = logging.getLogger("W1DEV1NE")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    log_file_path = os.path.join(logs_dir, "telegram.log")
    file_handler = logging.FileHandler(log_file_path, mode="a")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(f'{Fore.YELLOW}%(asctime)s{Style.RESET_ALL} - {Fore.GREEN}%(name)s - {Fore.CYAN}%(levelname)s - {Fore.RED}%(message)s{Style.RESET_ALL}', "%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger