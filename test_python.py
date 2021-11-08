with open('pgdas_fiscal_oesk/img_scrap.txt') as f:
    content = f.read()
    c_up = content.upper()
    c_low = content.lower()
# print(content)


def get_scrap(*vals):
    for val in vals:
        if val.islower():
            yield c_low.find(val)
        elif val.isupper():
            yield c_up.rfind(val)


searched = '26', '4p', '7j'
lowsrc = (s.upper() for s in searched)
uppsrc = (s.lower() for s in searched)


p1, p2, p3, P1, P2, P3 = get_scrap(*lowsrc, *uppsrc)
print(p1, p2, p3)


print(P1, P2, P3)
print(content[p2: p2 + 2])
# 7782 8089 8159
# 415 1824 188
# ------------------
# 4508 7669 7021
# 188 200 140
# ------------------
# 7618 7116 7565
# 575 3531 761
