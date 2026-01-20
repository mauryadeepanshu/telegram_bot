from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("⭐ Get Premium", callback_data="premium")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to Paid group 🎉\n\nClick below to see premium options.",
        reply_markup=reply_markup
    )

async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("7 Days - ₹49", callback_data="plan_7")],
        [InlineKeyboardButton("15 Days - ₹89", callback_data="plan_15")],
        [InlineKeyboardButton("30 Days - ₹169", callback_data="plan_30")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Choose a Premium Plan:", reply_markup=reply_markup)

async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("UPI Payment", callback_data="upi")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Choose Payment Method:", reply_markup=reply_markup)

async def upi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "Pay using UPI:\nUPI ID: deepanshu-maurya@ptaxis\n\nAfter payment, send screenshot."
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(premium, pattern="^premium$"))
app.add_handler(CallbackQueryHandler(plan, pattern="^plan_"))
app.add_handler(CallbackQueryHandler(upi, pattern="^upi$"))

print("Bot is running...")
app.run_polling()
