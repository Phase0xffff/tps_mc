# thomson_mc/projector.pyx
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True
import numpy as np
cimport numpy as np
from libc.math cimport sin, asin, cos, atan, sqrt

ctypedef np.float64_t DTYPE_t
DTYPE = np.float64

cdef class Projector:
    cdef double Ey, B, L_e, d_e, L_b, d_b, L

    def __cinit__(
        self, double Ey, double B,
        double L_e, double d_e, double L_b, double d_b, double L
    ):
        self.Ey = Ey
        self.B = B
        self.L_e = L_e
        self.d_e = d_e
        self.L_b = L_b
        self.d_b = d_b
        self.L = L
        if L < (L_e + d_e) or L < (L_b + d_b):
            raise ValueError(
                "Total length L must be >= L_e + d_e and >=  L_b + d_b"
            )
        if d_b < L_e + d_e:
            raise ValueError("d_b must be >= L_e + d_e")

    cpdef np.ndarray project(
        self, np.ndarray velocities, double charge_mass_ratio
    ):
        if not isinstance(velocities, np.ndarray):
            raise TypeError("velocities must be a numpy.ndarray")
        if velocities.dtype != DTYPE:
            velocities = velocities.astype(DTYPE)
        velocities = np.ascontiguousarray(velocities, dtype=DTYPE)

        cdef Py_ssize_t n = velocities.shape[0]
        coords = np.empty((n,2), dtype=DTYPE)
        cdef DTYPE_t[:, :] v = velocities
        cdef DTYPE_t[:, :] c = coords

        cdef double Ey = self.Ey
        cdef double B = self.B
        cdef double L_e = self.L_e
        cdef double d_e = self.d_e
        cdef double L_b = self.L_b
        cdef double d_b = self.d_b
        cdef double L = self.L

        cdef int i = 0
        cdef double vx, vy, vz, x, y, eps
        cdef double t1, sin1, cos1, tan1, theta1, r, v_xz
        cdef double t2, sin2, cos2, theta2
        cdef double t3, dvy

        eps = 1e-12

        with nogil:
            for i in range(n):
                vx = v[i,0]
                vy = v[i,1]
                vz = v[i,2] if v[i,2]>=eps else eps

                # free flight to magnetic field
                t1 = (L - L_b - d_b) / vz
                x = vx * t1
                y = vy * t1

                # magnetic field region
                tan1 = vx / vz
                theta1 = atan(tan1)
                cos1 = sqrt(1 + tan1 * tan1)
                sin1 = tan1 * cos1
                v_xz = vz / cos1
                r = v_xz / (charge_mass_ratio * B)
                if r * (1 - sin1) <= L_b:
                    c[i,0] = 0.0
                    c[i,1] = 0.0
                    continue

                sin2 = sin1 + L_b/r
                theta2 = asin(sin2)
                t2 = (theta2 - theta1) / (B * charge_mass_ratio)
                cos2 = sqrt(1 - sin2 * sin2)
                x += r*(cos1 - cos2)
                vx = v_xz * sin2
                vz = v_xz * cos2
                y += vy * t2

                # before electric field
                x += vx * d_b / vz
                y += vy * (d_b - L_e - d_e)/vz

                # electric field
                t3 = L_e / vz
                dvy = charge_mass_ratio * Ey * t3
                y += (vy + dvy / 2.0) * t3
                vy += dvy
                y += vy * d_e / vz

                c[i,0] = x
                c[i,1] = y

        return coords
