#daily jobs

from app.services import reset_count

async def daily_job(context):
    reset_count()
