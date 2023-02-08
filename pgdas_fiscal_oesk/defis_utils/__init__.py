import os
import glob
from subprocess import Popen, call
# Popen doesn't block, call blocks

"""
Legenda:
-> dp = dirpath
-> dn = dirnames
-> fn = fnames
"""


path = r'I:\OESK_CONTABIL'

ano_dirf = 2021
ano_dirf = str(ano_dirf)


def get_cliente(val):
    val = val.replace('/', '\\')
    val = val.split('\\')
    new_val = val.index(ano_dirf)
    returned = val[new_val-1]
    return returned

clientes_path = {}

for (dirpath, dirnames, filenames) in os.walk(path):

    if ano_dirf in dirnames:
        # input(dirpath)
        for (dp2, dn2, fn2) in os.walk(dirpath):
            if ano_dirf in dp2:
                for dp3, dn3, fn3 in os.walk(dp2):
                    if 'DIRF' in dp3:
                        dirf_path = dp3
                        now_command = f'explorer {dp3}'

                        the_client = get_cliente(dp3)
                        # input(the_client)
                        # print(the_client)
                        clientes_path[the_client] = dirf_path
                        # call(now_command)
for k, v in clientes_path.items():
    print(f'{k}')
