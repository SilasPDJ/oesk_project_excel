from pgdas_fiscal_oesk.giss_online_pt11 import GissGui

if __name__ == "__main__":
    from default.sets import compt_to_date_obj
    comptencia = compt_to_date_obj('03-2023')
    # __r_social, _giss_cnpj, _logar

    dados = ['DANILO PORPHIRIO VENSOL', 20367544000101, 228854]
    GissGui(dados, '09-2023', comptencia.strftime('%m-%Y'), headless=False)
