from win32com import client


class A:
    outlook_app = client.Dispatch('outlook.application')
    outlook_app.Session.Accounts.Item(1)  # set email sender

    def main_send_email(self, to, header, attached_msg, pdf_files=None):
        # return super().main_send_email(to, header, attached_msg, pdf_files)
        mail = self.outlook_app.CreateItem(0)
        oesk_dadmail = self.outlook_app.Session.Accounts.Item(1)
        mail.To = to
        # mail.To = 'silsilinhas@gmail.com'
        mail.Subject = header
        mail.HTMLBody = attached_msg
        if pdf_files is not None:
            for pdf in pdf_files:
                mail.Attachments.Add(pdf)
        mail.Send()


A().main_send_email("silsilinhas@gmail.com", "Apenas um teste", "<h1 style='background-color: red'>TESTE</h1>",
                    [r"O:\OneDrive\_FISCAL-2021\2022\04-2022\Vensol Multi Servicos LTDA\Registro_ISS-21776608000182.pdf"])
