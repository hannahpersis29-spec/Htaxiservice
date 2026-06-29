import os

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 2072039982

CHOOSING, NAME, PHONE, PICKUP, DESTINATION, DATE, TIME = range(7)

reply_keyboard = [
    ["✈️ Airport Pickup"],
    ["🏙️ Local Trip"],
    ["🛣️ Outstation"],
]

markup = ReplyKeyboardMarkup(
    reply_keyboard,
    resize_keyboard=True,
    one_time_keyboard=True,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(
        "🚖 Welcome to H Taxi Service!\n\n"
        "Please choose your trip type:",
        reply_markup=markup,
    )

    return CHOOSING


async def choose_trip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["trip_type"] = update.message.text

    await update.message.reply_text(
        "Please enter your name:",
        reply_markup=ReplyKeyboardRemove(),
    )

    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text

    await update.message.reply_text("Please enter your phone number:")

    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text

    await update.message.reply_text("Pickup location:")

    return PICKUP


async def get_pickup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["pickup"] = update.message.text

    await update.message.reply_text("Destination:")

    return DESTINATION
async def get_destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["destination"] = update.message.text

    await update.message.reply_text("Travel date (DD/MM/YYYY):")

    return DATE


async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text

    await update.message.reply_text("Travel time (e.g. 10:30 AM):")

    return TIME


async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["time"] = update.message.text

    booking = (
        "🚖 NEW H TAXI BOOKING\n\n"
        f"Trip Type: {context.user_data['trip_type']}\n"
        f"Name: {context.user_data['name']}\n"
        f"Phone: {context.user_data['phone']}\n"
        f"Pickup: {context.user_data['pickup']}\n"
        f"Destination: {context.user_data['destination']}\n"
        f"Date: {context.user_data['date']}\n"
        f"Time: {context.user_data['time']}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=booking,
    )

    await update.message.reply_text(
        "✅ Thank you!\n\n"
        "Your booking has been received.\n"
        "H Taxi Service will contact you shortly."
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Booking cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END
    def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, choose_trip)
            ],
            NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)
            ],
            PHONE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)
            ],
            PICKUP: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_pickup)
            ],
            DESTINATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_destination)
            ],
            DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)
            ],
            TIME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_time)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    print("H Taxi Service Bot is running...")
    application.run_polling()


if __name__ == "__main__":
    main()
