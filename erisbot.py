import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("TOKEN")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy ErisBot. Usa /ayuda para ver los comandos disponibles.")

# /info
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        f"Nombre: {user.full_name}\nUsername: @{user.username}\nID: {user.id}"
    )

# /ban
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user.id
        await context.bot.ban_chat_member(chat_id=update.message.chat_id, user_id=target_user)
        await update.message.reply_text("Usuario baneado.")
    else:
        await update.message.reply_text("Debes responder al mensaje del usuario que quieres banear.")

# /ayuda
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Iniciar el bot\n"
        "/info - Mostrar información del usuario\n"
        "/ban - Banear al usuario (respondiendo a su mensaje)\n"
        "/ayuda - Ver este menú"
    )

# Bienvenida automática
async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for nuevo in update.message.new_chat_members:
        nombre = nuevo.full_name
        await update.message.reply_text(
            f"¡Bienvenido/a {nombre} a *Jise Shop*! 🌆\nPor favor, lee las reglas y disfruta del grupo.",
            parse_mode='Markdown'
        )

# Iniciar aplicación
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("info", info))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("ayuda", ayuda))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bienvenida))

print("ErisBot funcionando...")
app.run_polling()