from datetime import datetime, timezone

from celery import Celery
from celery.schedules import crontab
from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from future.backports.datetime import timedelta

app = Flask(__name__)

# DB config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://notif:notif@db:5432/notif'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Celery config
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'

celery_app = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], include=['tasks'])
celery_app.conf.update(app.config)

celery_app.conf.beat_schedule['send_notifications'] = {
    'task': 'tasks.send_notifications',
    'schedule': crontab(minute='*'),
}


@app.route('/', methods=['GET', 'POST'])
def service_notifications_view():
    from models import Notification

    if request.method == 'POST':

        frequency = int(request.form.get('frequency', 1))
        if frequency not in Notification.FREQUENCY_MAPPING:
            frequency = 1

        notification = Notification(
            message=request.form.get('message'),
            frequency=frequency,
        )
        notification.set_or_update_delivery_date()
        db.session.add(notification)
        db.session.commit()

    context = {
        'notifications': Notification.query.order_by(Notification.delivery_date)[:10],
        'frequencies': Notification.FREQUENCY_MAPPING.items(),
    }

    return render_template('index.html', **context)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
