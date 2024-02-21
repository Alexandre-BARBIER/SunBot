from suntime import Sun, SunTimeException
from datetime import datetime, timedelta, date
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

from database import Database
from conf import TOKEN

bot = Bot(TOKEN)

database = Database()

delta = timedelta(seconds=1)
delta2 = timedelta(seconds=7700)
admin = "ZapyVR"

def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def sunsticker(context: CallbackContext) -> None:
    """Send the sun sticker."""
    job = context.job
    context.bot.send_sticker(job.context, sticker="CAACAgQAAxkBAAOcYW3dVp1qZnebjp5AZYy3gfKXPH4AAgEAA0DCtSvmoiwXb4fDeSEE")
    update_job_sunrise(job.context,context)

def moonsticker(context: CallbackContext) -> None:
    """Send the sun sticker."""
    job = context.job
    context.bot.send_sticker(job.context, sticker="CAACAgQAAxkBAAOgYW3dX6eyBpQTo9_LWjgbjuGQQQMAAgIAA0DCtSudUA1LAlEWOCEE")
    update_job_sunset(job.context,context)

def update_job_sunrise(chat_id, context:CallbackContext):
    localDatabase = Database()
    chat = localDatabase.get_chat(chat_id)
    timenow = datetime.utcnow()
    job_removed = remove_job_if_exists(str(chat_id)+"sunrise", context)
    sun = Sun(float(chat[2]),float(chat[3]))
    today_sr = sun.get_sunrise_time()
    sr_naive = today_sr.replace(tzinfo=None)
    queutime = sr_naive-timenow
    seconds_queu = int(queutime.total_seconds()) - 36300
    if seconds_queu <= 10:
        tomorrow_date = date.today() + timedelta(days=1)
        today_sr = sun.get_sunrise_time(tomorrow_date)
        sr_naive = today_sr.replace(tzinfo=None)
        queutime = sr_naive-timenow
        seconds_queu = int(queutime.total_seconds()) - 36300
    print(queutime)
    context.job_queue.run_once(sunsticker, seconds_queu, context=chat[1], name=str(chat[1])+"sunrise")

def update_job_sunset(chat_id, context:CallbackContext):
    localDatabase = Database()
    chat = localDatabase.get_chat(chat_id)
    timenow = datetime.utcnow()
    job_removed = remove_job_if_exists(str(chat_id)+"sunset", context)
    sun = Sun(float(chat[2]),float(chat[3]))
    today_ss = sun.get_sunset_time()
    ss_naive = today_ss.replace(tzinfo=None)
    queutime = ss_naive-timenow
    seconds_queu = int(queutime.total_seconds())
    if seconds_queu <= 10:
        tomorrow_date = date.today() + timedelta(days=1)
        today_ss = sun.get_sunset_time(tomorrow_date)
        ss_naive = today_ss.replace(tzinfo=None)
        queutime = ss_naive-timenow
        seconds_queu = int(queutime.total_seconds())
    print(queutime)
    context.job_queue.run_once(moonsticker, seconds_queu, context=chat[1], name=str(chat[1])+"sunset")

def start_command(update: Update, context: CallbackContext):
    """Start command"""
    update.message.reply_text("Salut, je suis le bonjour bot, j'envoie des ticker au levée et couchée du soleil")

def enable_command(update: Update, context: CallbackContext):
    """Add chat to database"""
    localDatabase = Database()
    chat = localDatabase.get_chat(update.message.chat.id)
    print(chat)
    print(type(chat))
    if chat is None:
        localDatabase.createChat(update.message.chat.id)
    chat = localDatabase.get_chat(update.message.chat.id)
    update_job_sunrise(chat[1],context)
    update_job_sunset(chat[1],context)
    current_jobs = context.job_queue.get_jobs_by_name(str(chat[1])+"sunrise")
    print(current_jobs)
    current_jobs = context.job_queue.get_jobs_by_name(str(chat[1])+"sunset")
    print(current_jobs)
    update.message.reply_text("Je suis bien activé")

def longitude_command(update: Update, context: CallbackContext):
    """Updates longitude for a chat"""
    localDatabase = Database()
    content = update.message.text.split(" ")[1]
    try:
        longitude = float(content)
        localDatabase.setLongitude(longitude,update.message.chat.id)
        update.message.reply_text("J'ai ta longitude")
    except:
        update.message.reply_text("envoie moi un float!")
    update_job_sunrise(update.message.chat.id,context)
    update_job_sunset(update.message.chat.id,context)
    

def latitude_command(update: Update, context: CallbackContext):
    """Updates latitude for a chat"""
    localDatabase = Database()
    content = update.message.text.split(" ")[1]
    try:
        latitude = float(content)
        localDatabase.setLatitude(latitude,update.message.chat.id)
        update.message.reply_text("J'ai ta latitude")
    except:
        update.message.reply_text("envoie moi un float!")
    update_job_sunrise(update.message.chat.id,context)
    update_job_sunset(update.message.chat.id,context)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start_command))

    dispatcher.add_handler(CommandHandler("enable", enable_command))

    dispatcher.add_handler(CommandHandler("longitude", longitude_command))
    dispatcher.add_handler(CommandHandler("latitude", latitude_command))

    localDatabase = Database()
    list_chats = localDatabase.get_chats()
    for chat in list_chats:
        print(chat)
        update_job_sunrise(chat[1],context=updater)
        update_job_sunset(chat[1],context=updater)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print("coucou")
    main()
