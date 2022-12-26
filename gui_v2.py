from default.sets.pathmanager import HasJson
path = r"O:\OneDrive\_FISCAL-2021\2022\11-2022\S. J. da Silva Dedetizadora\DAS_EM_ABERTO.json"

das_json = HasJson.load_json(path)
pend_compts = []
for lspart in das_json:
    pend_compts.append(list(lspart.keys())[0])
print(pend_compts)

for lspart, compt in zip(das_json, pend_compts):
    s = lspart[compt]
    print(s)

for e, lspart in enumerate(das_json):
    n_parc = lspart[pend_compts[e]]
    print(n_parc)
# a = list(lcompt.keys())[0]
# print(a)
# # for k, v in j.items():
# # print(k, v)
