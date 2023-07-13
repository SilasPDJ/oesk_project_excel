import smtplib
import json
import os
from email import policy
from email.parser import Parser
# from smtp_project import *


class EmailExecutor:
    def create_my_gmail_login_file(self):
        my_email, my_pass = '', ''
        thispath = os.path.dirname(__file__)
        thispath = os.path.join(thispath,
                                '..\\..', 'pgdas_fiscal_oesk\\data_clients_files')
        flpsnm = f'{thispath}\\serverMailLogin.txt'
        try:
            with open(flpsnm) as f:
                datas = f.read().split()
                my_email, my_pass = datas[0], datas[1]

        except FileNotFoundError:
            print('You need to add an email, I recommend you use a dedicated one')
            my_email = input('\033[1;31m INPUT YOUR TEST EMAIL: ')
            my_pass = input('\033[1;31m INPUT YOUR TEST PASSWORD: \033[m')
            os.makedirs(os.path.dirname(flpsnm))
            with open(flpsnm, 'w') as f:
                f.write(f'{my_email}\n{my_pass}')
        finally:
            return my_email, my_pass

    def main_send_email(self, to, header, attached_msg, pdf_files=None):
        """
        :param to: Envia a quem?
        :param header: subject, título
        :param attached_msg: ALL que já foi attached
        :param pdf_files: optional, email com PDF

        :return:
        """
        from email.mime.multipart import MIMEMultipart
        from email.header import Header

        sm, sp = self.create_my_gmail_login_file()
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(sm, sp)
            envia_mail = MIMEMultipart('mixed')
            envia_mail['Subject'] = Header(header, 'utf-8')
            envia_mail['To'] = to

            envia_mail.attach(attached_msg)
            if pdf_files is not None:
                for pdf in pdf_files:
                    envia_mail.attach(pdf)

                # "anexa" mensagens, anexos, etc

            server.sendmail(sm, to, envia_mail.as_string())

        # mimemultipart mixed or alternative

    def write_message(self, text="test", html_plain="html"):
        """
        :param text:
        :param html_plain: html or plain?
        :return:
        """

        from email.mime.text import MIMEText
        from email.header import Header
        from email import encoders
        """
        :param w: Write
        :return: return written
        """
        if 'plain' != html_plain.lower().strip() != 'html':
            raise AttributeError

        text = MIMEText(text, html_plain, 'utf-8')
        return text

    def tag_text(self, tag, text):
        # attributes inside text
        fecha = tag.split('style')[0].strip()
        new_text = f'<{tag}>{text}</{fecha}>'
        return new_text

    def zlist_colours_emails(self):
        path_colours = os.path.dirname(__file__)
        with open(path_colours+'\\zlist_colours.json') as fcol:
            colours = json.load(fcol)
            return colours

    def inside_me_others(self, inside_me, *others):
        """
        :param str inside_me:
        :param str others:
        :return:

        Cria tags (*others) dentro da inside_me
        """
        # pega o final e separa para colocar no meio
        ff = inside_me.index('</')

        final = inside_me[ff:]
        returned = inside_me[:ff]

        for other in others:
            returned += other
            # input(returned)
        returned += final
        return returned

    def wcor(self, cor):
        r = f' style=color:{cor}'
        return r

    def hora_mensagem(self):
        from datetime import datetime as dt
        hora = dt.now().time().hour
        if 18 > hora >= 12:
            return 'Boa tarde'
        elif 12 > hora > 7:
            return 'Bom dia'
        elif hora >= 18:
            # return 'Boa noite'
            return 'Por gentileza'
        else:
            return 'Por gentileza'
