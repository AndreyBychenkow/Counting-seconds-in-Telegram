import os
from time import sleep

import pytimeparse
from dotenv import load_dotenv

import ptbot


def render_progressbar(
    total, iteration, prefix="", suffix="", length=30, fill="░", zfill="█"
):
    iteration = min(total, iteration)
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * (length - filled_length) + zfill * filled_length
    return "{0} |{1}| {2}% {3}".format(prefix, pbar, percent, suffix)


def notify_progress(bot, chat_id, start_message_id, delay_seconds, secs_left):
    progress_bar = render_progressbar(total=delay_seconds, iteration=secs_left)
    bot.update_message(
        chat_id, start_message_id, f"Осталось {secs_left} секунд\n{progress_bar}"
    )
    if secs_left == 0:
        bot.send_message(chat_id, "Время вышло")


def set_timer(bot, chat_id, message):
    delay_seconds = pytimeparse.parse(message)
    start_message_id = bot.send_message(
        chat_id, f"Запуск таймера на {delay_seconds} секунд"
    )

    for secs_left in range(delay_seconds, -1, -1):
        notify_progress(bot, chat_id, start_message_id, delay_seconds, secs_left)
        sleep(1)


def main():
    load_dotenv()
    tg_token = os.getenv("TELEGRAM_TOKEN")
    tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    bot = ptbot.Bot(tg_token)
    bot.send_message(tg_chat_id, "Бот запущен")
    bot.send_message(tg_chat_id, "На сколько запускаем таймер?")

    bot.reply_on_message(lambda chat_id, message: set_timer(bot, chat_id, message))

    bot.run_bot()


if __name__ == "__main__":
    main()
