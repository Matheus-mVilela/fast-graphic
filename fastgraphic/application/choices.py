STATUS_OPEN = 'open'
STATUS_FINISHED = 'finished'

STATUS_CHOICES = (
    (STATUS_OPEN, 'Open'),
    (STATUS_FINISHED, 'Finished'),
)

CREDIT_CARD = 'credit-card'
DEBIT_CARD = 'debit-card'
MONEY = 'money'

PAYMENT_METHOD_CHOICES = (
    (MONEY, 'Dinheiro'),
    (CREDIT_CARD, 'Cartão de Crédito'),
    (DEBIT_CARD, 'Cartão de Débito'),
)
