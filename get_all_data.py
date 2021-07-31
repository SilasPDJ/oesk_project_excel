import pandas as pd

from default.sets import InitialSetting

IS = InitialSetting()
MAIN_FILE = r'C:\Users\Silas\OneDrive\_FISCAL-2021\__EXCEL POR COMPETENCIAS__\NOVA_FORMA_DE_DADOS.xlsm'
COMPT_ATUAL = IS.get_compt(m_cont=0)
DADOS_PADRAO = pd.read_excel(MAIN_FILE, sheet_name='DADOS_PADRÃO').to_dict()
# .to_html
DADOS = list(DADOS_PADRAO.values())


def consultar(specific=None):

    cont = 0 if not specific else specific
    while True:
        razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas = [
            list(d.values())[cont] for d in DADOS]

        yield razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas
        if str(razao_social) == 'nan' or specific:
            break
        # print(razao_social)
        cont += 1

    compt_atual = pd.read_excel(MAIN_FILE, sheet_name=COMPT_ATUAL)
    df = compt_atual.to_dict()
    # Dirs()


print(*consultar(2))
