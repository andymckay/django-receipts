from datetime import datetime
import logging

from receipts.receipts import Receipt
from django_receipts import constants

log = logging.getLogger(__name__)


def check(model, data):
    """
    Checks the validity of the receipt against the verification service.

    `model`: the mode, of the receipt object to update with the results
    `data`: the actual receipt string sent from the client
    """
    model.checked = datetime.now()
    receipt = Receipt(data)
    log.info('Checking receipt: %s' % model.pk)
    try:
        result = receipt.verify_server()['status']
    except:
        log.error('There was an error with the verification.', exc_info=True)
        result = 'error'

    status = constants.VALID_LOOKUP[result]
    model.valid = status
    model.save()
    return constants.VALID_INVERTED[status]
