import os
# import slugify
import sys

# https://pt.stackoverflow.com/questions/220078/o-que-significa-o-erro-execu%C3%A7%C3%A3o-de-scripts-foi-desabilitada-neste-sistema
package = sys.argv[1]
try:
    os.mkdir(package)
except FileExistsError:
    pass
open(os.path.join(package, '__init__.py'), 'w').close()
