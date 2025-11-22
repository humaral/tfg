# Autor: Hugo Martín Alonso
# Fecha: 22/11/2025
# Descripción: utilidades para el envío de correos electrónicos.

from flask_mail import Message
from flask import current_app
from app import mail

def enviar_mail(subject, sender=None, recipients=None, cc=None, body=''):

    if recipients is None:
        recipients = []
    if cc is None:
        cc = []

    msg = Message(
        subject=subject,
        sender=sender if sender else current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=recipients,
        cc=cc,
        body=body
    )
    
    mail.send(msg)