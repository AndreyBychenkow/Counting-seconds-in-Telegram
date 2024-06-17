import os

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


def set_timer(chat_id, message):
    delay_seconds = pytimeparse.parse(message)
    start_message_id = bot.send_message(
        chat_id, f"Запуск таймера {delay_seconds} секунд"
    )

    def notify_progress(secs_left):
        if secs_left > 0:
            progress_bar = render_progressbar(delay_seconds, secs_left)
            bot.update_message(
                chat_id,
                start_message_id,
                f"Осталось {secs_left} секунд\n{progress_bar}",
            )
        else:
            bot.update_message(chat_id, start_message_id, f"Осталось 0 секунд")
            bot.send_message(chat_id, "Время вышло")

    bot.create_countdown(delay_seconds, notify_progress)


if __name__ == "__main__":
    load_dotenv()
    TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TG_CHAT_ID = os.getenv("TG_CHAT_ID")

    bot = ptbot.Bot(TG_TOKEN)
    bot.send_message(TG_CHAT_ID, "Бот запущен")
    bot.send_message(TG_CHAT_ID, "На сколько запускаем таймер ?")
    bot.reply_on_message(set_timer)
    bot.run_bot()
