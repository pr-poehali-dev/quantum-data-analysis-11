import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import psycopg2


def handler(event: dict, context) -> dict:
    """Отправляет заявку с формы на email владельца сайта и сохраняет в БД"""

    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, X-User-Id, X-Auth-Token, X-Session-Id',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }

    raw_body = event.get('body', '') or '{}'
    body = json.loads(raw_body)
    contact = body.get('contact', '')

    if not contact:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Контакт не указан'})
        }

    schema = os.environ['MAIN_DB_SCHEMA']
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {schema}.leads (contact) VALUES ('{contact}')")
    conn.commit()
    cur.close()
    conn.close()

    smtp_user = os.environ['SMTP_USER']
    smtp_password = os.environ['SMTP_PASSWORD']
    recipient = 'maryasckockova@mail.ru'

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = recipient
    msg['Subject'] = 'Новая заявка с сайта'

    body_text = f"""
Новая заявка с сайта "Речь и развитие"

Контакт клиента: {contact}

Свяжитесь с клиентом в ближайшее время.
"""
    msg.attach(MIMEText(body_text, 'plain', 'utf-8'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({'success': True})
    }
