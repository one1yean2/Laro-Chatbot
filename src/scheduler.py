from flask_apscheduler import APScheduler

scheduler = APScheduler()

def create_jobs(app):
    job = scheduler.add_job(id='Scheduled Task', func=scheduled_task, trigger='cron', hour=18, minute=4, second=50)
    

def scheduled_task():
    from .steamdata import get_games_steamweb
    get_games_steamweb()
