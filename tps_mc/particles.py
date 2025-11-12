# thomson_mc/particles.py
import re

# --- 物理常数 ---
ELEM_CHARGE = 1.602176634e-19  # C
MASS_E = 9.10938356e-31        # kg
MASS_P = 1.6726219e-27         # kg
KB = 1.380649e-23              # J/K


class ParticleSpec:
    """
    粒子规格：名称、质量、电荷、平均能量
    支持多种输入形式：
      - mass: "m_e", "m_p", "4m_p", "2.5m_e"
      - charge: "e", "-e", "2e"
      - mean_energy:
          * "10eV"  -> 自动转为 J
          * "1.5keV" -> 自动转为 J
          * 数值(float) -> 直接视为 J
    """

    def __init__(
        self, name: str, mass, charge, mean_energy, energy_threshold,
        n_particles: int
    ):
        self.name = name
        self.mass = self._resolve_mass(mass)
        self.charge = self._resolve_charge(charge)
        self.mean_energy = self._resolve_energy(mean_energy)
        self.energy_threshold = self._resolve_energy(energy_threshold)
        self.n_particles = n_particles

    def _resolve_mass(self, mass):
        if isinstance(mass, str):
            # 支持 4m_p 或 2.5m_e 这种写法
            match = re.match(r"^([\d.]+)?\s*(m_e|m_p)$", mass.strip())
            if match:
                factor = float(match.group(1)) if match.group(1) else 1.0
                base = match.group(2)
                return factor * (MASS_E if base == "m_e" else MASS_P)
            raise ValueError(f"Unknown mass format: {mass}")
        elif isinstance(mass, (float, int)):
            return float(mass)
        else:
            raise TypeError("mass must be str or float")

    def _resolve_charge(self, charge):
        if isinstance(charge, str):
            # 支持 "e", "-e", "2e", "-3e"
            match = re.match(r"^(-?\d*\.?\d*)?\s*e$", charge.strip())
            if match:
                factor = match.group(1)
                factor = float(factor) if factor not in ("", None) else 1.0
                return factor * ELEM_CHARGE
            raise ValueError(f"Unknown charge format: {charge}")
        elif isinstance(charge, (float, int)):
            return float(charge)
        else:
            raise TypeError("charge must be str or float")

    def _resolve_energy(self, energy):
        if isinstance(energy, str):
            # 支持 10eV, 5keV, 2.5MeV
            match = re.match(
                r"^\s*([\d.]+)\s*(eV|keV|MeV)\s*$", energy, re.IGNORECASE
            )
            if not match:
                raise ValueError(f"Unknown energy format: {energy}")
            value, unit = float(match.group(1)), match.group(2).lower()
            factor = {"ev": 1.0, "kev": 1e3, "mev": 1e6}[unit]
            return value * factor * ELEM_CHARGE  # 转换为 J
        elif isinstance(energy, (float, int)):
            return float(energy)  # 直接视为 J
        else:
            raise TypeError("mean_energy must be str or float")
