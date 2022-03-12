import os
import jwt
import datetime
import smtplib
import random

from flask import request
from api import db, app, PORTAL_NAME

from api.service.users import VerifyCredentials, ById, ByUsernameOrEmail, UpdatePassword

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from api.util.errors import ForbiddenError, MessagedError


# TODO: padronizar respostas dos endpoints?
def Authenticate(handle, password):
    return VerifyCredentials(handle, password)


def RecoverPassword(username, email):
    user = ByUsernameOrEmail(username, email)

    # só pra não correr o risco
    if user.id == 0:
        raise ForbiddenError(f"Não é possível recuperar a senha do Administrador.")

    # Gera uma hash que servirá como senha temporaria
    new_password = str(random.getrandbits(128))[:11]

    try:
        # Conecta e inicia o serviço de email
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        res = smtp.starttls()

        # https://stackoverflow.com/questions/54657006/smtpauthenticationerror-5-7-14-please-log-n5-7-14-in-via-your-web-browser/56809076#56809076
        smtp.login('codelabtesteesquecisenha@gmail.com', '44D6DDAAC9C660F72D6490D7CC44731BEA7C236A9241B387D3E9AF0C66B30D49')

        # enviar email
        msg = MIMEMultipart()
        msg['Subject'] = f'Recuperação de Senha {PORTAL_NAME}'
        msg['From'] = f'{PORTAL_NAME}-Senha'
        msg['To'] = user.email
        body = MIMEText(f"A sua nova senha é {new_password}")
        msg.attach(body)
        smtp.sendmail('codelabtesteesquecisenha@gmail.com', email, msg.as_string())
    except:
        raise MessagedError(f"Não foi possível enviar um email para o usuario {user.name} ({user.email}), então a senha não foi alterada.")

    UpdatePassword(user, new_password)


def AuthorizedUser(id, include_data=False):
    user = ById(id, include_data=include_data)
    return user
