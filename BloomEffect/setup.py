"""
Setup.py file

Configure the project, build the package and upload the package to PYPI
"""
import setuptools
from Cython.Build import cythonize
from setuptools import Extension

# NUMPY IS REQUIRED
try:
    import numpy
except ImportError:
    raise ImportError("\n<numpy> library is missing on your system."
                      "\nTry: \n   C:\\pip install numpy on a window command prompt.")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BloomEffect",
    version="1.0.2",
    author="Yoann Berenguer",
    author_email="yoyoberenguer@hotmail.com",
    description="Pygame bloom effect (shader effect)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yoyoberenguer/BloomEffect",
    # packages=setuptools.find_packages(),
    packages=['BloomEffect'],
    ext_modules=cythonize([
        Extension("BloomEffect.bloom", ["BloomEffect/bloom.pyx"],
                  extra_compile_args=["-DPLATFORM=linux", "-march=x86-64", "-m64", "-O3", "-ffast-math", "-Wall", "-static", "-fPIC", "-shared",
	     "--param=max-vartrack-size=1500000"], extra_link_args=['-lm', '-fopenmp'] ,language="c")]),
    include_dirs=[numpy.get_include()],
    define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    license='MIT',

    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Cython',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        # 'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    install_requires=[
        'setuptools>=49.2.1',
        'Cython>=0.28',
        'numpy>=1.18',
        'pygame>=2.0'
    ],
    python_requires='>=3.6',
    platforms=['any'],
    include_package_data=True,
    data_files=[
        ('./lib/site-packages/BloomEffect',
         ['LICENSE',
          'MANIFEST.in',
          'pyproject.toml',
          'README.md',
          'requirements.txt',
          'BloomEffect/__init__.py',
          'BloomEffect/__init__.pxd',
          'BloomEffect/bloom.pyx',
          'BloomEffect/bloom.pxd',
          'BloomEffect/deprecated.pyx',
          'BloomEffect/setup_bloom.py',
          ]),
    ],

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/yoyoberenguer/BloomEffect/issues',
        'Source': 'https://github.com/yoyoberenguer/BloomEffect',
    },
)

