from datetime import datetime, timezone, timedelta

from main import db


class Notification(db.Model):
    """Simple database model to track notifications."""

    FREQUENCY_MAPPING = {1: 'daily', 7: 'weekly'}

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    frequency = db.Column(db.SmallInteger)
    delivery_date = db.Column(db.DateTime)

    def set_or_update_delivery_date(self):
        """Calculate the delivery date based on the instance's frequency."""
        if self.delivery_date is None:
            self.delivery_date = datetime.now(timezone.utc) + timedelta(days=self.frequency)
        else:
            self.delivery_date += timedelta(days=self.frequency)

    @property
    def verbose_frequency(self):
        return self.FREQUENCY_MAPPING.get(self.frequency)
