from .models import Payment
import settings
import requests
import logging
from datetime import datetime

logger = logging.getLogger('django', )


def print_log(text):
    logger.info('--------------------------------------------')
    logger.info(f'{datetime.now()} | {text}')
    logger.info('---------------------------------------------')


def check_qiwi(payment_uuid):
    payment=None
    try:
        payment = Payment.objects.get(payment_id=payment_uuid)
    except:
        print_log('Payment UUID not found')
        return False
    if payment and not payment.status:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            "Authorization": f'Bearer {settings.QIWI_SECRET}'
        }
        request = requests.get(f'https://api.qiwi.com/partner/bill/v1/bills/{payment.id}', headers=headers)
        respond = request.json()
        if respond['status']['value'] == 'PAID':
            payment.status = True
            payment.save()
            print_log(f'Payment ID {payment.id} complete')
            return True
        else:
            return False



