import unittest
from datetime import timedelta
from unittest.mock import patch

from main import app, db

from app.models import Notification
from app.tasks import send_notifications


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class TestViews(unittest.TestCase):

    def test_get_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_notification(self):
        response = self.client.post('/', data={
            'message': 'Remind me!',
            'frequency': 1,
        })
        self.assertEqual(response.status_code, 302)
        notification = Notification.query.filter_by(message='Remind me!').first()
        self.assertIsNotNone(notification)
        self.assertIsNotNone(notification.delivery_date)


class TestTasks(unittest.TestCase):

    def test_send_due_notification(self):
        overdue_notification = Notification(message='some message', frequency=1)
        overdue_notification.delivery_date -= timedelta(days=30)
        db.session.add(overdue_notification)
        db.session.commit()

        assert overdue_notification in db.session

        with patch('tasks.send_notification') as send_notification:
            send_notifications.delay.assert_called_with(Notification)

        assert send_notification.called_with(overdue_notification.id)


if __name__ == '__main__':
    unittest.main()
