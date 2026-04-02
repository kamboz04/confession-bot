#main code

from telegram.ext import Application, CommandHandler,MessageHandler,filters,CallbackQueryHandler
from datetime import time

from app.config import BOT_TOKEN
from app.db.schema import init_db
from app.handlers import start,confess,buttonhandle,unified_text_handler,rules
from app.jobs import daily_job


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    init_db()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("confess",confess)) 
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,unified_text_handler))

    app.add_handler(CallbackQueryHandler(buttonhandle))
    app.add_handler(CommandHandler("rules", rules))

    #running daily job
    app.job_queue.run_daily(
        daily_job,
        time=time(hour=0, minute=0)
    )

    print("Runing...........")
    app.run_polling()

if __name__ == "__main__":
    main()
