from datetime import datetime, timezone, timedelta

from main import celery_app, db
from models import Notification


@celery_app.task
def send_notifications():
    """Select the notifications with a due delivery date, and send."""
    due_notifications = Notification.query.filter(Notification.delivery_date <= datetime.now(timezone.utc))
    for notification in due_notifications:
        send_notification.delay(notification.id)


@celery_app.task
def send_notification(notification_id):
    """Send notification and update the delivery date."""
    # Lock until we update the delivery date
    notification = db.session.query(Notification).with_for_update().filter_by(id=notification_id).first()

    # Check if notification was already sent, and skip if yes.
    if notification.delivery_date > datetime.now(timezone.utc):
        db.session.rollback()
        return

    print(f'Delivered notification={notification_id}!')  # Code for sending goes here.

    notification.set_or_update_delivery_date()

    db.session.commit(notification)
