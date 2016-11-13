def sv_main(t=0.5, w=1, u=1):

    in_sockets = [
        ['s', 'Animation', t],
        ['s', 'Mode_1', w],
        ['s', 'Mode_2', u]
    ]

    from math import sin, cos, radians, pi, sqrt
    from mathutils import Vector, Euler
    import numpy as np
    import scipy
    from scipy.special import jn, jn_zeros

    def drumhead_height(n, k, distance, angle, t):
        nth_zero = jn_zeros(n, k)
        return cos(t)*cos(n*angle)*jn(n, distance*nth_zero)

    theta = np.r_[0:2*pi:50j]
    radius = np.r_[0:1:50j]

    x = array([r*cos(theta) for r in radius])
    y = array([r*sin(theta) for r in radius])
    z = array([drumhead_height(1, 1, r, theta, 0.5) for r in radius])

    Verts = []
    verts_new = Verts.append

    for i in x:
        verts_new((x[i],y[i],z[i]))

    out_sockets = [
        ['v', 'Verts', [Verts]]
    ]

    return in_sockets, out_sockets