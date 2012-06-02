UNCHECKED = 0
OK = 1
REFUNDED = 2
EXPIRED = 3
PENDING = 4
ERROR = 5
INVALID = 6

VALID_LOOKUP = {
    'unchecked': UNCHECKED,
    'ok': OK,
    'refunded':  REFUNDED,
    'pending': PENDING,
    'expired': EXPIRED,
    'error': ERROR,
    'invalid': INVALID
}

VALID_INVERTED = dict([(v, k) for k, v in VALID_LOOKUP.iteritems()])
