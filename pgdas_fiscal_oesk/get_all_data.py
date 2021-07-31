import pandas as pd

from default.sets import InitialSetting as __

IS = __
MAIN_FOLDER = r'C:\Users\Silas\OneDrive\_FISCAL-2021'
MAIN_FILE = MAIN_FOLDER+r'\__EXCEL POR COMPETENCIAS__\NOVA_FORMA_DE_DADOS.xlsm'
ATUAL_COMPT = IS.get_compt(m_cont=0)

DADOS_PADRAO = pd.read_excel(MAIN_FILE, sheet_name='DADOS_PADRÃO').to_dict()
# .to_html
DADOS = list(DADOS_PADRAO.values())


def consultar(specific=None):

    cont = 0 if not specific else specific
    while True:
        razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas = [
            list(d.values())[cont] for d in DADOS]

        yield razao_social, IS.treat_documents_values(cnpj), cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas

        if str(razao_social) == 'nan' or specific:
            break
        # print(razao_social)
        cont += 1

    compt_atual = pd.read_excel(MAIN_FILE, sheet_name=ATUAL_COMPT)
    df = compt_atual.to_dict()
    # Dirs()

# razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas = list(*consultar(
#     2))
# print(*consultar(2))
