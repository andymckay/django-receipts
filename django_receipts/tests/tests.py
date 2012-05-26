from datetime import timedelta
import json

from django.utils.timezone import now
from django.test import TestCase
from django.core.urlresolvers import reverse

import mock

from django_receipts import constants
from django_receipts.models import Receipt
from django_receipts.tasks import check, VerificationError


class TestView(TestCase):
    hash_ = 'acbd18db4cc2f85cedef654fccc4a4d8'  # hash of foo.

    def setUp(self):
        self.url = reverse('receipts.receive')

    def test_get(self):
        assert self.client.get(self.url).status_code == 405

    def test_post_empty(self):
        assert self.client.post(self.url).status_code == 400

    @mock.patch('django_receipts.views.check')
    def test_post_valid(self, check):
        check.return_value = 'ok'
        res = self.client.post(self.url, {'receipt': 'foo'})
        assert res.status_code == 200
        assert res['Content-Type'] == 'application/json'
        assert json.loads(res.content)['status'] == 'ok'

    @mock.patch('django_receipts.views.check')
    def test_post_invalid(self, check):
        check.return_value = 'invalid'
        res = self.client.post(self.url, {'receipt': 'foo'})
        assert json.loads(res.content)['status'] == 'invalid'

    @mock.patch('django_receipts.views.check')
    def test_post_obj(self, check):
        check.return_value = 'ok'
        self.client.post(self.url, {'receipt': 'foo'})
        receipts = Receipt.objects.all()
        assert receipts.count() == 1
        assert receipts[0].hash == self.hash_

    @mock.patch('django_receipts.views.check')
    def test_check_called(self, check):
        check.return_value = 'ok'
        Receipt.objects.create(hash=self.hash_)
        self.client.post(self.url, {'receipt': 'foo'})
        receipts = Receipt.objects.all()
        assert receipts.count() == 1
        assert check.called

    @mock.patch('django_receipts.views.check')
    def test_check_not_called(self, check):
        check.return_value = 'ok'
        Receipt.objects.create(hash=self.hash_, checked=now())
        self.client.post(self.url, {'receipt': 'foo'})
        assert not check.called

    @mock.patch('django_receipts.views.check')
    def test_check_expired(self, check):
        check.return_value = 'ok'
        Receipt.objects.create(hash=self.hash_, checked=now() - timedelta(days=5))
        self.client.post(self.url, {'receipt': 'foo'})
        assert check.called

    def test_blocked(self):
        Receipt.objects.create(hash=self.hash_, checked=now(), allow=False,
                               valid=constants.OK)
        res = self.client.post(self.url, {'receipt': 'foo'})
        assert json.loads(res.content)['status'] == 'invalid'


@mock.patch('django_receipts.tasks.Receipt.verify_server')
class TestTask(TestCase):

    def setUp(self):
        self.receipt = Receipt.objects.create(hash='abc')

    def test_ok(self, verify):
        verify.return_value = {'status': 'ok'}
        check(self.receipt, 'abc')
        assert self.receipt.get_status() == 'ok'

    def test_error(self, verify):
        verify.side_effect = VerificationError
        check(self.receipt, 'abc')
        assert self.receipt.get_status() == 'error'

    def test_data_error(self, verify):
        verify.side_effect = {'?': '?'}
        check(self.receipt, 'abc')
        assert self.receipt.get_status() == 'error'

