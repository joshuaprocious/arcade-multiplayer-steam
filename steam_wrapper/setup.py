import os
from setuptools import setup, Extension
from Cython.Build import cythonize

# Path to Steamworks SDK (relative to this file's directory)
this_dir = os.path.dirname(__file__)
sdk_root = os.path.abspath(os.path.join(this_dir, "..", "steamworks_sdk_155"))

ext = Extension(
    name="steam_wrapper",
    sources=["steam_wrapper.pyx"],
    language="c++",
    include_dirs=[os.path.join(sdk_root, "public")],
    library_dirs=[os.path.join(sdk_root, "redistributable_bin", "win64")],
    libraries=["steam_api64"],
    extra_compile_args=["/std:c++17"],
)

setup(
    name="steam_wrapper",
    ext_modules=cythonize([ext], compiler_directives={'language_level': "3"}),
)
