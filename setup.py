from setuptools import setup, Extension, find_packages
from pathlib import Path
import subprocess as sp

import platform

uname = platform.uname()

BSEC = True
bsec_lib_name = 'algobsec'

if BSEC:
    ext_comp_args = ['-D BSEC']
    libs = ['pthread', 'm', 'rt', bsec_lib_name]
    lib_dirs = ['/usr/local/lib', 'bsec']
    if uname.machine.find('64') != -1:
        bsec_lib_dir = 'bsec/m64'
    else:
        bsec_lib_dir = 'bsec/m32'
    lib_dirs.extend([bsec_lib_dir])
else:
    ext_comp_args = []
    libs = ['pthread', 'm', 'rt']
    lib_dirs = ['/usr/local/lib']
    bsec_lib_dir = None

LIBDIR = Path(__file__).parent

README = (LIBDIR / "README.md").read_text()

# Run ranlib on the libraries
if bsec_lib_dir:
    sp.run(["ranlib", f"{bsec_lib_dir}/lib{bsec_lib_name}.a"])

bme68x = Extension('bme68x',
                   extra_compile_args=ext_comp_args,
                   include_dirs=['/usr/local/include'],
                   libraries=libs,
                   library_dirs=lib_dirs,
                   depends=['BME68x-Sensor-API/bme68x.h', 'BME68x-Sensor-API/bme68x.c',
                            'BME68x-Sensor-API/bme68x_defs.h', 'internal_functions.h', 'internal_functions.c'],
                   sources=['bme68xmodule.c', 'BME68x-Sensor-API/bme68x.c', 'internal_functions.c'])

setup(name='bme68x',
      version='1.3.0',
      description='Python interface for BME68X sensor and BSEC',
      long_description=README,
      long_description_content_type='text/markdown',
      url='https://github.com/pi3g/bme68x-python-library',
      author='Nathan',
      author_email='nathan@pi3g.com',
      license='MIT',
      classifiers=[
           'Development Status :: 3 - Alpha',
           'Intended Audience :: Developers',
           'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Scientific/Engineering :: Atmospheric Science',
      ],
      keywords='bme68x bme680 bme688 BME68X BME680 BME688 bsec BSEC sensor environment temperature pressure humidity air pollution',
      packages=find_packages(),
      py_modules=['bme68xConstants', 'bsecConstants'],
      package_data={
          'bme68x': ['bsec/2021_04_29_02_51_bsec_h2s_nonh2s_2_0_6_1 .config']
      },
      headers=['BME68x-Sensor-API/bme68x.h',
               'BME68x-Sensor-API/bme68x_defs.h', 'internal_functions.h'],
      ext_modules=[bme68x])
