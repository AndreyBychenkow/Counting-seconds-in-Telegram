import os
from functools import partial

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
    if secs_left > 0:
        progress_bar = render_progressbar(delay_seconds, secs_left)
        bot.update_message(
            chat_id,
            start_message_id,
            f"Осталось {secs_left} секундn{progress_bar}",
        )
    else:
        bot.update_message(chat_id, start_message_id, f"Осталось 0 секунд")
        bot.send_message(chat_id, "Время вышло")


def set_timer(bot, chat_id, message):
    delay_seconds = pytimeparse.parse(message)
    start_message_id = bot.send_message(
        chat_id, f"Запуск таймера на {delay_seconds} секунд"
    )

    notify = partial(notify_progress, bot, chat_id,
                     start_message_id, delay_seconds)

    bot.create_countdown(delay_seconds, notify)


def main():
    load_dotenv()
    tg_token = os.getenv("TELEGRAM_TOKEN")
    tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    bot = ptbot.Bot(tg_token)
    bot.send_message(tg_chat_id, "Бот запущен")
    bot.send_message(tg_chat_id, "На сколько запускаем таймер?")

    bot.reply_on_message(lambda chat_id, message:
                         set_timer(bot, tg_chat_id, message))
    bot.run_bot()


if __name__ == "__main__":
    main()
