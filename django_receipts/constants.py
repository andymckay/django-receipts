UNCHECKED = 0
OK = 1
REFUNDED = 2
EXPIRED = 3
PENDING = 4
ERROR = 5

VALID = (
    (UNCHECKED, 'unchecked'),
    (OK, 'ok'),
    (REFUNDED, 'refunded'),
    (EXPIRED, 'expired'),
    (PENDING, 'pending'),
    (ERROR, 'error')
)

VALID_LOOKUP = {
    'ok': OK,
    'refunded':  REFUNDED,
    'pending': PENDING,
    'expired': EXPIRED,
    'error': ERROR
}

VALID_INVERTED = {
    UNCHECKED: 'unchecked',
    OK: 'ok',
    REFUNDED: 'refunded',
    PENDING: 'pending',
    EXPIRED: 'expired',
    ERROR: 'error',
}
