from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

TOKEN = "8587942506:AAEMLlbc-Z_ZOcSfIkOdtv_hrRKw89ivFF0"
ADMIN_ID = 5502861086
GROUP_INVITE_LINK = "https://t.me/Desi_album70"

PAID_USERS = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id in PAID_USERS:
        await update.message.reply_text(
            f"✅ You are already a premium member.\n\n🔗 Join group:\n{GROUP_INVITE_LINK}"
        )
        return

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
    await query.edit_message_text(
        "Choose a Premium Plan:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("UPI Payment", callback_data="upi")]]
    await query.edit_message_text(
        "Choose Payment Method:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def upi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "💳 Pay using UPI:\n"
        "UPI ID: deepanshu-maurya@ptaxis\n\n"
        "📸 After payment, send the screenshot here."
    )


# 📸 USER SENDS PAYMENT SCREENSHOT
async def payment_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    photo = update.message.photo[-1].file_id

    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
        ]
    ]

    caption = (
        "💰 Payment Proof Received\n\n"
        f"👤 User: @{user.username}\n"
        f"🆔 User ID: {user.id}"
    )

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await update.message.reply_text(
        "✅ Screenshot sent to admin.\nPlease wait for approval."
    )


# 👑 ADMIN APPROVE / REJECT
async def admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return

    action, user_id = query.data.split("_")
    user_id = int(user_id)

    if action == "approve":
        PAID_USERS.add(user_id)
        await context.bot.send_message(
            user_id,
            f"🎉 Payment Approved!\n\n🔗 Join your premium group:\n{GROUP_INVITE_LINK}"
        )
        await query.edit_message_caption("✅ Approved and access granted.")

    elif action == "reject":
        await context.bot.send_message(
            user_id,
            "❌ Payment rejected.\nPlease contact admin."
        )
        await query.edit_message_caption("❌ Payment rejected.")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(premium, pattern="^premium$"))
app.add_handler(CallbackQueryHandler(plan, pattern="^plan_"))
app.add_handler(CallbackQueryHandler(upi, pattern="^upi$"))
app.add_handler(CallbackQueryHandler(admin_action, pattern="^(approve|reject)_"))
app.add_handler(MessageHandler(filters.PHOTO, payment_proof))

print("Bot is running...")
app.run_polling()
