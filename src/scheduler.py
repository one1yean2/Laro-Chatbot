import datetime
from flask_apscheduler import APScheduler


scheduler = APScheduler()

def create_jobs(app):
    game_data_job = scheduler.add_job(id='Game Data Task', func=game_data_task, trigger='cron', hour=1, minute=0, second=0)
    promotion_job = scheduler.add_job(id='Scheduled Promotion', func=scheduled_promotion, trigger='cron', hour=0, minute=0, second=0)
    expired_job = scheduler.add_job(id='Expired Promotion', func=expired_promotion, trigger='cron', hour=0, minute=0, second=0)
def scheduled_promotion():
    with scheduler.app.app_context():
        from src.models import Promotion , db
        from .views import promotion
        today = datetime.datetime.today()
        if today.day == today.month:
            promo = Promotion(
                promotion_name = 'โปร '+str(today.day)+' เดือน '+str(today.month),
                discount_type = 'percent',
                discount_value = '15',
                min_purchase = '0',
                start_date = datetime.datetime.now(),
                end_date = datetime.datetime.now() + datetime.timedelta(minutes=1),
                usage_limit = '2',
            )
            db.session.add(promo)
            db.session.commit()
def expired_promotion():
    with scheduler.app.app_context():
        from src.models import Promotion , db
        today = datetime.datetime.today()
        Promotion.query.filter(Promotion.end_date <= today).delete(synchronize_session=False)
        db.session.commit()
def game_data_task():
    from .steamdata import get_games_steamweb
    get_games_steamweb()
