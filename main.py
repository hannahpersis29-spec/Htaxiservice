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
import os
import logging

# ----------------------------
# LOGGING
# ----------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ----------------------------
# BOT SETTINGS
# ----------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 2072039982

# ----------------------------
# CONVERSATION STATES
# ----------------------------
(
    CHOOSING,
    NAME,
    PHONE,
    PICKUP,
    DESTINATION,
    DATE,
    TIME,
) = range(7)

# ----------------------------
# REPLY KEYBOARD
# ----------------------------
reply_keyboard = [
    ["✈️ Airport Pickup"],
    ["🏙️ Local Trip"],
    ["🚖 Outstation Trip"],
]

markup = ReplyKeyboardMarkup(
    reply_keyboard,
    resize_keyboard=True,
)

# ----------------------------
# START COMMAND
# ----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚖 Welcome to H Taxi Service!\n\n"
        "Please choose your trip type.",
        reply_markup=markup,
    )
    return CHOOSING


# ----------------------------
# CHOOSE TRIP
# ----------------------------
async def choose_trip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["trip_type"] = update.message.text

    await update.message.reply_text(
        "Please enter your full name:",
        reply_markup=ReplyKeyboardRemove(),
    )

    return NAME


# ----------------------------
# CUSTOMER NAME
# ----------------------------
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "Please enter your phone number:"
    )

    return PHONE
    # ----------------------------
# PHONE NUMBER
# ----------------------------
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text

    await update.message.reply_text(
        "📍 Enter your pickup location:"
    )

    return PICKUP


# ----------------------------
# PICKUP LOCATION
# ----------------------------
async def get_pickup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["pickup"] = update.message.text

    await update.message.reply_text(
        "📍 Enter your destination:"
    )

    return DESTINATION


# ----------------------------
# DESTINATION
# ----------------------------
async def get_destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["destination"] = update.message.text

    await update.message.reply_text(
        "📅 Enter your travel date\n\nExample: 30/06/2026"
    )

    return DATE


# ----------------------------
# TRAVEL DATE
# ----------------------------
async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text

    await update.message.reply_text(
        "🕒 Enter your pickup time\n\nExample: 08:30 AM"
    )

    return TIME
    # ----------------------------
# TRAVEL TIME
# ----------------------------
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


# ----------------------------
# CANCEL
# ----------------------------
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Booking cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


# ----------------------------
# MAIN
# ----------------------------
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
        fallbacks=[
            CommandHandler("cancel", cancel),
        ],
    )

    application.add_handler(conv_handler)

    print("H Taxi Service Bot is running...")

    application.run_polling()


if __name__ == "__main__":
   async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Booking cancelled.",
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
    
