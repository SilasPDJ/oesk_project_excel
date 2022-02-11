from default.sets.pathmanager import Dirs
self = Dirs
self.client_path = r'O:\OneDrive\_FISCAL-2021\2022\01-2022\Suzana Palacio dos Santos'


self.compt_used = '01-2022'

_already_exist = self.walget_searpath("z".join([n for n in self.compt_used if n.isnumeric()]),
                                      self.client_path, 2)
print(not _already_exist)
