# constants declaration

NAME = 'pythogram'
VERSION = '0.1'
DESCRIPTION = 'Signal analyzer'

import numpy
import scipy
import shutil
import os
import os.path
import platform
from cx_Freeze import setup,Executable

def list_all_files(path):
  entrylist = os.listdir(path)
  flist = []
  for entry in entrylist:
    fentry = os.path.join(path, entry)
    if os.path.isdir(fentry):
      nflist = list_all_files(fentry)
      flist = flist + nflist
    else:
      flist.append(fentry)
  return flist

setup(
  name = NAME,
  version = VERSION,
  description = DESCRIPTION,
  options = {
    'build_exe' : {
                    'excludes': [
                                 'collections.abc',
                                 'email',
                                 'numpy',
                                 'scipy',
                                 'unittest'
                                ],
                    'include_files': [
                                      os.path.dirname(numpy.__file__),
                                      os.path.dirname(scipy.__file__)
                                     ],
                    'includes': [
                                 'ast',
                                 'multiprocessing',
                                 'timeit',
                                 'urllib2'
                                ]
                  }
  },
  executables = [
    Executable(
      'pythogram.py',
      base=(None if platform.system() != 'Windows' else 'Win32GUI')
    )
  ]
)

me = os.path.dirname(os.path.abspath(__file__))

build_dir = os.path.join(me, 'build', os.listdir(os.path.join(me, 'build'))[0])

if platform.system()=='Windows':
  import zipfile
  zip=zipfile.ZipFile(os.path.join(me, '%s-%s.zip'%(NAME, VERSION)), "w")
  for file in list_all_files(build_dir):
    zip.write(file,'%s-%s\\%s'%(NAME, VERSION, os.path.relpath(file,build_dir)), zipfile.ZIP_DEFLATED)
  zip.close()
else:
  import tarfile
  tar=tarfile.open('%s-%s.tar.gz'%(NAME, VERSION),'w:gz')
  tar.add(build_dir, '%s-%s'%(NAME, VERSION))
  tar.close()
shutil.rmtree(build_dir)
