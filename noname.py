# importing the important and useful modules etc

from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes,MessageHandler,filters,CallbackQueryHandler

# initailise the bot token 

TOKEN = "8461662181:AAEbn2aIcF6o4rleIObzpLvN8G2XyaYEQx8"


confessions = {}
confession_id = 0

# define your fxns etc 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ HEY KESHAV04 your, Your bot is alive (v20.6).")


async def confess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("send your msg....")


 # replace with your ID

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global confession_id

    user_msg = update.message.text
    user_id = update.message.from_user.id

    confession_id += 1
    confessions[confession_id] = user_msg

    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve|{confession_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject|{confession_id}")
     ]
]
    replyMarkup = InlineKeyboardMarkup(keyboard)


    # Send confession to admin (you)
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📩 New Confession:\n\n{user_msg}\n\n👤 User ID: {user_id}",
        reply_markup=replyMarkup
        
    )

    # Reply to user
    await update.message.reply_text("Your confession has been sent for review.")

async def buttonhandle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    CHANNEL_ID = -1003810548229
    query = update.callback_query

    await query.answer()

    action, cid = query.data.split("|")
    cid = int(cid)

    msg = confessions.get(cid)

    if not msg:
        await query.edit_message_text("⚠️ Confession not found.")
        return

    if action == "approve":
        # (Later you can send to channel here)
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"🕵️ Anonymous Confession:\n\n{msg}"
        )

        # Update admin message
        await query.edit_message_text("✅ Approved and posted")

    elif action == "reject":
        await query.edit_message_text("❌ Rejected")



# define main fxn 

def main():
    app = Application.builder().token(TOKEN).build() # make instance of bot
    app.add_handler(CommandHandler("start", start))  # adding handler
    app.add_handler(CommandHandler("confess",confess)) 
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(buttonhandle))
    
    print("🤖 Bot is running... (v20.6)")
    app.run_polling()  #start polling

# basic boilerplate for main fxn 

if __name__ == "__main__":
    main()
