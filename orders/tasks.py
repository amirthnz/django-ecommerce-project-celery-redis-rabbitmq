from celery import shared_task
from django.core.mail import send_mail
from ippanel import Client
import requests
from .models import Order
Client.send_pattern
@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
    f'You have successfully placed an order.' \
    f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,
    message,
    'admin@myshop.com',
    [order.email])
    return mail_sent


@shared_task
def send_sms():
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\n' \
    f'You have successfully placed an order.' \
    f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,
    message,
    'admin@myshop.com',
    [order.email])


    api_key = "Xai3MZu00HMZrzvFdl84O--ZUXdHLR2XonaghfWd8SI="
    api_endpoint = "https://api2.ippanel.com/api/v1/sms/send/webservice/single"

    headers = {
        "apikey": api_key,
    }

    response = requests.get(api_endpoint, headers=headers)

    # # check if the request was successful
    if response.status_code == 200:
        print(f"THE STATUS IS {response.content}")
    else:
        print("ERROR")

    # create client instance
    sms = Client(api_key)
    message_id = sms.send(
        "+983000505",          # originator
        ["989386274038"],    # recipients
        "Success", # message
        "description"        # is logged
    )

    return message_id

    # return mail_sent

