# tps_mc/__init__.py
"""
tps_mc 包初始化文件

统一暴露包的主要接口，方便外部导入：
    from tps_mc import ThomsonSimulator, ParticleSpec
"""

from .controller import ThomsonSimulator
from .particles import ParticleSpec

# 可控 from tps_mc import * 时导出的符号
__all__ = ["ThomsonSimulator", "ParticleSpec"]
