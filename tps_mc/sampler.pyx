# thomson_mc/sampler.pyx
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True
import numpy as np
cimport numpy as np
from libc.math cimport sqrt, log, cos, sin, acos, fabs, M_PI
from libc.stdlib cimport rand, RAND_MAX

ctypedef np.float64_t DTYPE_t
DTYPE = np.float64

cdef inline double rand_uniform() nogil:
    # rand() 返回 0..RAND_MAX，避免 0 导致 log(0)
    cdef double r = (rand() + 1.0) / (RAND_MAX + 1.0)
    return r

cpdef np.ndarray sample(
    int n_particles,
    double cone_angle,
    double mass,
    double mean_energy,
    double energy_threshold=0.0,
    str direction_mode="uniform"
):
    """
    Sample particle velocities:
      - Energy E sampled from exponential p(E) = (1/<E>) exp(-E/<E>)
      - Speed v = sqrt(2 E / m)
      - Direction sampled within cone angle `cone_angle` (radians)
          direction_mode: "uniform"    -> uniform over cone
                          "gaussian"   -> gaussian about axis, truncated to cone

    Returns:
        velocities: ndarray shape (n_particles, 3), dtype float64
    """
    if mean_energy <= 0.0:
        raise ValueError("mean_energy must be positive")

    cdef np.ndarray[DTYPE_t, ndim=2] velocities = np.empty(
        (n_particles,3), dtype=DTYPE
    )
    cdef DTYPE_t[:, :] v = velocities

    cdef int i
    cdef double u, u2, E, vmag, theta, phi
    cdef double sigma_theta = cone_angle * 0.5
    cdef double x, y, z
    cdef double cos_tmax, cos_theta, r_val, z0
    cos_tmax = cos(cone_angle)

    with nogil:
        for i in range(n_particles):
            # ---------- 1) Exponential energy ----------
            u = rand_uniform()
            # 注意：平均能量是截断前的能量分布的平均值！！！
            E = energy_threshold - mean_energy * log(u)
            vmag = sqrt(2.0 * E / mass)

            # ---------- 2) Direction sampling ----------
            if direction_mode == "uniform":
                u2 = rand_uniform()
                cos_theta = 1.0 - u2 * (1.0 - cos_tmax)
                theta = acos(cos_theta)
                phi = 2.0 * M_PI * rand_uniform()
            else:
                while True:
                    u = rand_uniform()
                    u2 = rand_uniform()
                    r_val = sqrt(-2.0*log(u))
                    z0 = r_val * cos(2.0*M_PI*u2)
                    theta = fabs(z0) * sigma_theta
                    if theta <= cone_angle:
                        break
                phi = 2.0 * M_PI * rand_uniform()

            # ---------- 3) Construct velocity ----------
            x = vmag * sin(theta) * cos(phi)
            y = vmag * sin(theta) * sin(phi)
            z = vmag * cos(theta)

            v[i,0] = x
            v[i,1] = y
            v[i,2] = z

    return velocities
