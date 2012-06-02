from datetime import timedelta
import hashlib
import json

from django import http
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now

from django_receipts.models import Receipt
from django_receipts.tasks import check

import logging

log = logging.getLogger(__name__)
CHECK_INTERVAL = getattr(settings, 'RECEIPT_CHECK_INTERVAL', 60 * 60)


@csrf_exempt
def receive(request):
    """
    Receives the receipt from the client and maybe fires off a check of that
    receipt if needed.
    """
    if request.method != 'POST':
        return http.HttpResponseNotAllowed(['POST'])

    receipt = request.raw_post_data
    if not receipt:
        return http.HttpResponseBadRequest()

    hash_ = hashlib.md5(receipt).hexdigest()
    log.info('Receipt received: %s, %s' % (hash_, request.META['REMOTE_ADDR']))

    obj, created = Receipt.objects.get_or_create(hash=hash_)
    expired = (not obj.checked or
               (obj.checked + timedelta(seconds=CHECK_INTERVAL)) < now())

    if obj.allow and expired:
        result = check(obj, receipt)
    else:
        result = obj.get_status()

    response = http.HttpResponse(json.dumps({'status': result}),
                                 content_type='application/json')
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST'
    return response
