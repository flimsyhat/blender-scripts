import numpy as np
from scipy.special import sph_harm
import scipy.misc

def sv_main(m=1, n=1, steps=50):

    # Sockets in

    in_sockets = [
    ['s', 'n',  n],
    ['s', 'm',  m],
    ['s', '# of steps',  steps],
    ]

    # Parametrized spherical coordinates
    r = 1
    pi = np.pi
    cos = np.cos
    sin = np.sin
    theta = np.r_[0:2*pi:complex(0,steps)]
    phi = np.r_[0:2*pi:complex(0,steps)]

    # Initialize array
    Verts = []
    verts_new = Verts.append

    # Fill array with vertices

    for i in range(len(theta)-1):
        for j in range(len(phi)-1):

            t = theta[i]
            p = phi[j]

            r = sph_harm(m, n, t, p).real

            x = r * sin(p) * cos(t)
            y = r * sin(p) * sin(t)
            z = r * cos(p)

            verts_new((x,y,z))

    # Sockets out

    out_sockets = [
          ['v', 'Vertices', [Verts]],
      ]

    return in_sockets, out_sockets
