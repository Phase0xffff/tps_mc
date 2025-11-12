# TPS-MC: Thomson Spectrometer Monte Carlo Simulation

**TPS-MC** 是一个用于模拟 **Thomson Parabola Spectrometer（汤姆逊谱仪）** 中带电粒子轨迹的 Python 包，采用 **Cython 加速** 和 **JSON 配置驱动**，支持多粒子种类、能量分布采样、电磁场偏转以及结果可视化。

## 项目特点

+ 完全基于物理模型的汤姆逊轨迹模拟
+ 多离子种类支持与个性化参数设置
+ Cython 加速计算（采样与偏转）
+ 可视化模块支持散点图与热图
+ JSON 配置驱动，命令行一键运行
+ 可在 VSCode 中直接调试与扩展

## 安装

建议使用 Conda 创建隔离环境：

```bash
# 克隆仓库
git clone https://github.com/Phase0xffff/tps_mc.git
cd tps_mc

# 使用 environment.yml 创建环境
conda env create -f environment.yml

# 激活环境
conda activate tps_mc_env

# 安装本地包
pip install -e .
```

这会：

+ 从github下载最新版本的源代码

+ 自动编译 Cython 扩展 (`sampler.pyx`, `projector.pyx`)；

+ 注册命令行脚本 `tps-mc`；

+ 在当前环境中以“开发模式”安装包。

安装完成后，你可以在任何路径下直接运行：

```bash
tps-mc config.json
```

## 程序结构

```bash
tps_mc/
├── __init__.py               # 暴露主要类接口
├── cli.py                    # 命令行入口
├── controller.py              # 主控类 ThomsonSimulator
├── particles.py               # 粒子定义 ParticleSpec
├── sampler.pyx                # 能量与方向采样（Cython 加速）
├── projector.pyx              # 电磁场偏转计算（Cython 加速）
├── visualize.py               # 可视化模块
example/
├── config.json               # 示例配置文件
pyproject.toml
setup.py
README.md
LICENSE
MANIFEST.in
```

## JSON 配置文件格式

程序完全由配置文件驱动，示例如下（可参考`example/config.json`）：

```json
{
    "tps_params": {
        "e_field": 1.7e6,
        "b_field": 1.0,
        "L_e": 0.15,
        "d_e": 0.259,
        "L_b": 0.06,
        "d_b": 0.44,
        "L": 1.0
    },
    "particles": [
    {
        "name": "Proton",
        "mass": "m_p",
        "charge": "e",
        "mean_energy": "1MeV",
        "energy_threshold": "1MeV",
        "n_particles": 10000
    },
    {
        "name": "Alpha",
        "mass": "4m_p",
        "charge": "2e",
        "mean_energy": "5MeV",
        "energy_threshold": "1MeV",
        "n_particles": 5000
    }
    ],
    "cone_angle": 0.1,
    "direction_mode": "uniform",
    "plot": true,
    "plot_mode": "scatter"
}
```

字段说明：

|字段   |说明   |
|-------|------|
|tps_params|汤姆逊谱仪几何和场参数|
|particles|各离子种类定义（可多个）|
|mean_energy|指定能量分布的平均能量（支持单位 eV/keV/MeV）|
|energy_threshold|能量分布采样的下限阈值|
|n_particles|每个粒子种类采样的数目|
|cone_angle|方向锥角（单位：度）|
|direction_mode|"uniform" 或 "gaussian"|
|plot|是否绘图|
|plot_mode|"scatter", "heatmap", "both"|

## 运行示例

在任意路径下准备一个配置文件，例如：

```bash
config.json
```

内容如上示例，然后运行：

``` bash
tps-mc config.json
```

程序将自动：

1. 读取配置；

1. 构建电磁场模型；

1. 为每种粒子进行能量与方向采样；

1. 计算到达探测面的坐标；

1. 生成散点图或热图。

## 调试与开发（仅供参考）

### 在 VSCode 中调试

1. 打开项目根目录；

2. 创建 .vscode/launch.json（只影响此项目）：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run TPS-MC",
      "type": "python",
      "request": "launch",
      "module": "tps_mc.cli",
      "args": ["config.json"],
      "cwd": "${workspaceFolder}",
      "console": "integratedTerminal"
    }
  ]
}
```

3. 在 cli.py 或 controller.py 中设置断点；

1. 按 F5 启动调试。

## License

MIT License © 2025 Yijie Zhao
