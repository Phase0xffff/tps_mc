# tps_mc/controller.py
from typing import List, Literal

from .particles import ParticleSpec
from .sampler import sample
from .projector import Projector
from .visualize import plot_coords


class ThomsonSimulator:
    def __init__(self, e_field, b_field, L_e, d_e, L_b, d_b, L):
        """
        e_field, b_field: 电场/磁场强度
        l_e, d_e: 电场区间长度 & 电场区到探测面距离
        l_b, d_b: 磁场区间长度 & 磁场区到探测面距离
        l: 入射孔到探测面的总长度
        """
        self.projector = Projector(e_field, b_field, L_e, d_e, L_b, d_b, L)
        self.species: List[ParticleSpec] = []

    def add_species(self, species: ParticleSpec):
        """添加一个粒子种类"""
        self.species.append(species)

    def run(
        self,
        cone_angle: float,
        direction_mode: Literal["uniform", "gaussian"] = "uniform",
        plot: bool = True,
        mode: Literal["scatter", "heatmap", "both"] = "scatter"
    ):
        """
        n_particles: 每个物种采样的粒子数
        cone_angle: 方向锥角（弧度）
        """
        all_coords = []
        all_labels = []

        for sp in self.species:
            velocities = sample(
                n_particles=sp.n_particles,
                cone_angle=cone_angle,
                mass=sp.mass,
                mean_energy=sp.mean_energy,
                energy_threshold=sp.energy_threshold,
                direction_mode=direction_mode
            )
            coords = self.projector.project(
                velocities, sp.charge / sp.mass
            )
            all_coords.append(coords)
            all_labels.append(sp.name)

        if plot:
            plot_coords(all_coords, labels=all_labels, mode=mode)

        return all_coords
