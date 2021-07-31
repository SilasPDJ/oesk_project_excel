from .get_all_data import consultar, ATUAL_COMPT, ATUAL_ANO, MAIN_FOLDER
razao_social, cnpj, cpf, codigo_simples, imposto_a_calcular, email, gissonline, giss_login, ginfess_cod, ginfess_link, dividas_ativas = list(*consultar(
    2))
# print(*consultar(2))
