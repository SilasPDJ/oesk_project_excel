from default.sets.init_email import EmailExecutor
from default.sets import InitialSetting


class SendDividas(EmailExecutor, InitialSetting):
    def __init__(self, *args, email, compt):
        __razao_social, __cnpj = args
        now_email = email
        self.compt = compt

        print(now_email)
        # print(f'VALOR: {VALOR}')
        print(f'_cliente: {__razao_social}')
        # input(self.set_compt_only(-11, 1, past_only=False))
        # FUNCIONA PRA CONTAR PRO MES Q VEM VALIDADO COM ANO
        self.client_path = self.files_pathit(
            "Dívidas_Simples_" + __razao_social, compt)

        dividas_pdf_files = self.files_get_anexos_v4(
            self.client_path, file_type='pdf',  upload=False)
        qtd_arquivos = len(dividas_pdf_files)
        # mail_header = f"com vencimento previsto para o dia: {self.venc_boletos().replace('-', '/')}"
        mail_header = f"com vencimento previsto para o dia: 30/10"
        mail_header = mail_header.replace('30', '31')

        mail_header = f"Parcelamentos, {'boleto' if qtd_arquivos == 1 else 'boletos'} {mail_header}"
        print('titulo: ', mail_header)

        message = self.mail_dividas_msg(
            __razao_social, __cnpj, len(dividas_pdf_files))
        # print(message)

        das_message = self.write_message(message)

        # # 'silsilinhas@gmail.com'
        self.main_send_email(now_email, mail_header,
                             das_message, dividas_pdf_files)
        # ###########################
        # Vou registrar o each_dict no b
        # ###########################

        """a partir do terceiro argumento, só há mensagens attachedas"""

    def mail_dividas_msg(self, client, cnpj, main_anx_len=0):

        colours = self.zlist_colours_emails()
        red, blue, money, parc_style = \
            self.wcor(colours[114]), self.wcor('blue'), ' style="background-color:yellow; color:green"', \
            'style="background-color:yellow; color:red"'
        ntt = self.tag_text
        inso = self.inside_me_others
        # posso inso dentro de inso sem problema
        full_mensagem = f"""
{ntt('h1', f'{self.hora_mensagem()}, {client}!')}

{inso(ntt('h2', 'Seguem anexados:'), inso(ntt('p', '->'),ntt('span '+parc_style, f' {main_anx_len} Parcelamentos pendentes'), 
                                          ntt('h2', '-> A data de vencimento é igual para todos os boletos anexados')))
        if main_anx_len > 1 else inso(ntt('h2', 'Segue anexado:'), inso(ntt('p', '-> '),ntt('span'+red, 'Parcelamento pendente'))) 
        if main_anx_len > 0 else ntt('h3'+money, 'NÃO HÁ PARCELAMENTOS PENDENTES OU ANEXADOS')}


<div>
Este e-mail é automático. Por gentileza, cheque o nome e o CNPJ ({ntt('span'+red, cnpj)}) antes de pagar o documento.
<h4>Caso haja qualquer conflito, responda sem hesitar esta mensagem neste e-mail.</h4>
<h4>Todas as declarações são e continuarão sendo feitas minuciosamente.</h4>
</div>
{ntt('h2'+blue,'ATT, Oesk Contábil')}
        """
        return full_mensagem

    def get_dividas_vencimento(self, compt_setted=None):
        """
        :param compt_setted: from dividas, compt setted

        :return: data vencimento formato dia-mes-ano
        """

        mes, ano = compt_setted.split('-')
        mes, ano = int(mes), int(ano)
        # caso precise da compt setted
        venc_dividas_day = self.get_last_business_day_of_month()
        # é possível data

        venc = f'{venc_dividas_day:02d}-{self.m():02d}'
        return venc

    def dividas_mime_img(self, dividas_png_files: list):
        from email.mime.image import MIMEImage
        imgsimgs = []
        for png in dividas_png_files:
            print(png)
            with open(png, 'rb') as pf:
                img = MIMEImage(pf.read())
                imgsimgs.append(img)
        return imgsimgs

    def venc_boletos(self):
        from datetime import date
        from dateutil.relativedelta import relativedelta as reldel
        compt = self.compt
        m, y = compt.split('-')
        m, y = int(m), int(y)
        the_venc = date(m, y, 1) + reldel(months=1) - reldel(days=1)
        return the_venc
