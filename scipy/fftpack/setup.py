#!/usr/bin/env python
# Created by Pearu Peterson, August 2002

from os.path import join

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration('fftpack',parent_package, top_path)

    config.add_data_dir('tests')
    config.add_data_dir('benchmarks')

    config.add_library('dfftpack',
                       sources=[join('dfftpack','*.f')])

    sources = ['fftpack.pyf','src/zfft.c','src/drfft.c','src/zrfft.c',
               'src/zfftnd.c']

    config.add_extension('_fftpack',
        sources=sources,
        libraries=['dfftpack'],
        depends=['src/zfft_djbfft.c', 'src/zfft_fftpack.c', 'src/zfft_fftw.c',
            'src/zfft_fftw3.c', 'src/zfft_mkl.c',
            'src/drfft_djbfft.c', 'src/drfft_fftpack.c',
            'src/drfft_fftw3.c', 'src/drfft_fftw.c',
            'src/zfftnd_fftpack.c', 'src/zfftnd_fftw.c',
            'src/zfftnd_fftw3.c', 'src/zfftnd_mkl.c',
            ],
    )

    config.add_extension('convolve',
        sources=['convolve.pyf','src/convolve.c'],
        libraries=['dfftpack'],
    )
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    from fftpack_version import fftpack_version
    setup(version=fftpack_version,
          description='fftpack - Discrete Fourier Transform package',
          author='Pearu Peterson',
          author_email = 'pearu@cens.ioc.ee',
          maintainer_email = 'scipy-dev@scipy.org',
          license = 'SciPy License (BSD Style)',
          **configuration(top_path='').todict())
