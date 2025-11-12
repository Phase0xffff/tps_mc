# tps_mc/cli.py
import argparse
import json
import numpy as np
from tps_mc import ThomsonSimulator, ParticleSpec


def main():
    parser = argparse.ArgumentParser(
        description="Run Thomson spectrometer simulation from JSON config"
    )
    parser.add_argument(
        "config",
        type=str,
        help="Path to JSON configuration file"
    )
    args = parser.parse_args()

    # --- 1) 读取配置 ---
    with open(args.config, "r") as f:
        cfg = json.load(f)

    # --- 2) 初始化模拟器 ---
    sim = ThomsonSimulator(
        e_field=cfg["tps_params"]["e_field"],
        b_field=cfg["tps_params"]["b_field"],
        L_e=cfg["tps_params"]["L_e"],
        d_e=cfg["tps_params"]["d_e"],
        L_b=cfg["tps_params"]["L_b"],
        d_b=cfg["tps_params"]["d_b"],
        L=cfg["tps_params"]["L"],
    )

    # --- 3) 添加粒子 ---
    for sp_cfg in cfg["particles"]:
        sp = ParticleSpec(
            name=sp_cfg["name"],
            mass=sp_cfg["mass"],
            charge=sp_cfg["charge"],
            mean_energy=sp_cfg["mean_energy"],
            energy_threshold=sp_cfg['energy_threshold'],
            n_particles=sp_cfg.get("n_particles", 1000)
        )
        sim.add_species(sp)

    # --- 4) 运行模拟 ---
    sim.run(
        cone_angle=np.radians(cfg.get("cone_angle", 10)),
        direction_mode=cfg.get("direction_mode", "uniform"),
        plot=cfg.get("plot", True),
        mode=cfg.get("plot_mode", "scatter"),
    )
