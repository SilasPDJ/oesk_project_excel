# from default import NewSetPaths, ExcelToData
from default.sets.init_email import EmailExecutor
from default.sets import InitialSetting
from win32com import client


class PgDasmailSender(EmailExecutor, InitialSetting):

    def __init__(self, *args, email, compt, venc_das, all_valores=None):
        a = __r_social, __cnpj, __cpf, __declarado, __valor_competencia, imposto_a_calcular, __envio = args

        self.__venc_das = venc_das
        self.compt = compt
        self.client_path = self.files_pathit(__r_social.strip(), self.compt)

        mail_header = f"{compt.replace('-', '/')} - Relatórios e fechamento da competência. Simples Nacional."
        print('titulo: ', mail_header)
        _valor = self.trata_money_excel(__valor_competencia)
        print(_valor)
        print(__valor_competencia)
        print(__valor_competencia)
        print(a)

        now_email = email
        # now_email = 'silsilinhas@gmail.com'
        if now_email == '':
            print('wtf')
        elif imposto_a_calcular.upper() not in ["LP", "SEM_MOV"]:
            print(now_email)
            print(f'VALOR: {_valor}')
            print(f'CLIENTE: {__r_social}')
            self.message = self.mail_pgdas_msg(
                __r_social, __cnpj, imposto_a_calcular, _valor)
            # input(message)
            das_message = self.write_message(self.message)

            das_anx_files = self.files_get_anexos_v4(
                self.client_path, file_type='pdf')
            # if gmail upload is Fals
            #
            # e
            if _valor != 'SEM VALOR A PAGAR' and __valor_competencia != 'das_pend':
                if len(das_anx_files) < 4:
                    print(
                        f'\033[1;31mAlgo está errado com {__r_social}\033[m')
                    print('Vou passar...')
                else:
                    print('td certo')
                    self.main_send_email(
                        now_email, mail_header, das_message, das_anx_files)
            else:
                if len(das_anx_files) < 2:
                    print(
                        f'\033[1;31mAlgo está errado com {__r_social}\033[m')
                    print('Vou passar...')
                else:
                    self.main_send_email(
                        now_email, mail_header, das_message, das_anx_files)

            # input('security, silsilinhas')

            print(f'Enviado... p/ {now_email}')
            # input('teste')

        else:
            print('\033[1;31m', f'ainda não declarado, {__r_social}', '\033[m')

    def main_send_email(self, to, header, attached_msg, pdf_files=None):
        import pythoncom
        # return super().main_send_email(to, header, attached_msg, pdf_files)
        self.outlook_app = client.Dispatch(
            'outlook.application', pythoncom.CoInitialize())
        mail = self.outlook_app.CreateItem(0)

        # set the account
        account = None
        for acc in mail.Session.Accounts:
            if "39" in acc.DisplayName:
                account = acc
        mail._oleobj_.Invoke(*(64209, 0, 8, 0, account))
        # mail.SendUsingAccount = self.outlook_app.Session.Accounts.Item(1)
        # set email sender
        # mail.To = 'silsilinhas@gmail.com'
        mail.To = to
        mail.Subject = header
        mail.HTMLBody = attached_msg
        if pdf_files is not None:
            for pdf in pdf_files:
                mail.Attachments.Add(pdf)
        try:
            mail.Send()
            # mail.Save()
        except Exception as e:
            mail.Display(True)

    def write_message(self, text="test", html_plain="html"):
        """
        :param text:
        :param html_plain: html or plain?
        :return:
        """
        # return super().write_message(text, html_plain)
        return text

    def mail_pgdas_msg(self, client, cnpj, tipo_das, valor):
        colours = self.zlist_colours_emails()

        red, blue, money = self.wcor(colours[114]), self.wcor(
            'blue'), 'style="background-color:yellow; color:green"'
        ntt = self.tag_text
        inso = self.inside_me_others
        inside_me = ntt(f'strong'+blue, 'inside meeeeeeeee')
        # {inso(ntt('h2'+blue, f"{self.hora_mensagem()}, "), ntt("span"+blue,f"{client}!"))}
        # {inso(ntt('h3' + blue, f'CNPJ: '), ntt('span' + red, cnpj))}
        # {ntt('h3', f'CNPJ: {cnpj}')}
        full_mensagem = f"""
{ntt('h2', f'{self.hora_mensagem()}, {client}!')}
{ntt('h3', 'Seguem anexados:')}
<h3> 
-> DAS {f"({ntt('span'+blue,tipo_das)})" if valor != 'SEM VALOR A PAGAR' else ''}
sobre faturamento de {ntt('span style="background-color:yellow; color:green"', 'R$ '+valor)}
</h3>

<h3> 
    -> Protocolos e demonstrativos respectivos
            {
    f'''
    <h3>
        -> A previsão da data de vencimento do boleto é: {ntt('span' + red, self.__venc_das)}
    </h3>
    <h4> 
        -> O arquivo do boleto contém as iniciais "{ntt('span'+red,'PGDASD-DAS')}"
    </h4>
    '''
            if valor != 'SEM VALOR A PAGAR' else f"<h3>{ntt('span'+red,'NÃO')} há boleto a pagar.</h3>"
            }
<hr>
</h3> 
<div>
Este e-mail é automático. Considerar sempre o e-mail mais atual.<br>
Por gentileza, cheque o nome e o CNPJ ({ntt('span'+red, cnpj)}) {"antes de pagar o documento." if valor != 'SEM VALOR A PAGAR' else ''}
<h4>Caso haja qualquer conflito, responda sem hesitar esta mensagem neste e-mail.</h4>
<h4>Todas as declarações são e continuarão sendo feitas minuciosamente.</h4>
</div>
{ntt('h2'+blue,'ATT, Oesk Contábil')}

        """
        return full_mensagem
