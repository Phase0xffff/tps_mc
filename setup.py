from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

# 自动查找 numpy include
include_dirs = [np.get_include()]

# 声明 Cython 扩展
extensions = [
    Extension(
        "tps_mc.sampler", ["tps_mc/sampler.pyx"], include_dirs=include_dirs
    ),
    Extension(
        "tps_mc.projector", ["tps_mc/projector.pyx"], include_dirs=include_dirs
    ),
]

setup(
    name="tps_mc",
    version="0.1.0",
    ext_modules=cythonize(
        extensions,
        language_level=3,
        annotate=True,      # 可选，生成 HTML 注释
        compiler_directives={
            "boundscheck": True, "wraparound": True,    # 调试阶段打开
            "cdivision": True,
            "linetrace": True, "binding": True          # 用于调试跟踪
        }
    ),
    packages=["tps_mc"],
    zip_safe=False
)
