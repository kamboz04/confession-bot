notttelegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram import Update,ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes,MessageHandler,filters
from app.services import user_exists,addUser,incCount,check

import os
from dotenv import load_dotenv

load_dotenv()

#handler for start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    userId = str(update.effective_user.id)

    #if user alrady exists just say i am alive else first add him to database
    if user_exists(userId):

        await update.message.reply_text("🕵️ Anonymous Confession Bot\n\nHey, I receive anonymous confessions, review them, and publish selected ones to a channel—without revealing your identity.\n\nTo send your confession, use the command: /confess\nThen type your message and send. \n\nIt can be anything\n\nany incident \nlove story \nbreakup story \nOr anything you wanna say but can't say openly\n\n—just make sure it follows basic rules (no spam, hate, or illegal content).Once submitted, your confession will be reviewed before being posted.\n\nConfessions will be posted here @CricMemez\n\nMake sure you join so you can see other's opinions on your confessions.\n\nNote : Your indentity will be anonymous, so don't share any name etc")
    else:
        addUser(userId)
        await update.message.reply_text("🕵️ Anonymous Confession Bot\n\nHey, I receive anonymous confessions, review them, and publish selected ones to a channel—without revealing your identity.\n\nTo send your confession, use the command: /confess\nThen type your message and send. \n\nIt can be anything\n\nany incident \nlove story \nbreakup story \nOr anything you wanna say but can't say openly\n\n—just make sure it follows basic rules (no spam, hate, or illegal content).Once submitted, your confession will be reviewed before being posted.\n\nConfessions will be posted here @CricMemez\n\nMake sure you join so you can see other's opinions on your confessions.\n\nNote : Your indentity will be anonymous, so don't share any name etc")

#a dictionary to store the confessions temprarly
confessions = {}
confession_id = 0

#handler for confess command
async def confess(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # fethch count from databse
    user_id = update.message.from_user.id
    row = check(user_id)

    currCnt = row[0]

    # if count >=5 daily limit exceeds
    # else ask for confession msg 
    if currCnt >= 5:
        print("op.")
        await update.message.reply_text("You have exhausted daily limit of 5 :(")
        return
    else:
        await update.message.reply_text("send your msg....😎")
        context.user_data["newConfession"] = True

# handler for accept/reject buttons
async def buttonhandle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    action, cid = query.data.split("|")
    cid = int(cid)

    msg = confessions.get(cid)

    if not msg:
        await query.edit_message_text("⚠️ Confession not found.")
        return

    # if approved, send confesssion to channel
    if action == "approve":
        await context.bot.send_message(
            chat_id=os.getenv("CHANNEL_ID"),
            text=f"🕵️ Anonymous Confession:\n\n{msg}"
        )

        # Update admin message
        await query.edit_message_text("✅ Approved and posted")

    elif action == "reject":
        await query.edit_message_text("❌ Rejected")

# handler for incoming confession  msg 
async def unified_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # send confession msg with accept/reject  buttons to admin
    if context.user_data.get("newConfession"):

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
            chat_id = os.getenv("ADMIN_ID"),
            text=f"📩 New Confession:\n\n{user_msg}\n\n👤 User ID: {user_id}",
            reply_markup=replyMarkup
            
        )

        incCount(user_id)

        # Reply to user
        await update.message.reply_text("Your confession has been sent for review and will be posted here @CricMemez 😽")

        context.user_data.pop("newConfession")

    else:
        return
    
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("📜 Rules:\n\nNo spam or repeated messages\nNo hate speech or abusive language\n No personal attacks or targeting individuals\nNo illegal or harmful content\nNo promotions, ads, or links\n\n⚠️ Follow the rules or you may be banned.\n\n✅Keep it real, respectful, and meaningful.")
