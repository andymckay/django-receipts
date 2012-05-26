from datetime import datetime
import logging

from jwt import DecodeError
from receipts.receipts import Receipt, VerificationError
from django_receipts import constants
from django_receipts.models import Receipt as ReceiptModel

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
    except (VerificationError, TypeError, DecodeError):
        log.error('There was an error with the verification.', exc_info=True)
        status = constants.VALID_LOOKUP['error']
    else:
        status = constants.VALID_LOOKUP.get(result)

    model.valid = status
    model.save()
    return status
