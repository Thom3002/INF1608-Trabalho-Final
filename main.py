import ctypes
from ctypes import Structure, c_double, CDLL, POINTER
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Particle(Structure):
    _fields_ = [("x", c_double), ("y", c_double), ("z", c_double),
                ("vx", c_double), ("vy", c_double), ("vz", c_double),
                ("fx", c_double), ("fy", c_double), ("fz", c_double),
                ("mass", c_double)]

# Carrega a biblioteca em C
lib = CDLL('./libparticle.so')

# Definição dos tipos de argumentos para as funções
lib.update_particle.argtypes = [POINTER(Particle), c_double]
lib.apply_force.argtypes = [POINTER(Particle), c_double, c_double, c_double]
lib.update_particle.restype = None
lib.apply_force.restype = None

# Função para atualizar a posição de uma partícula
def update_particle(particle, dt):
    lib.update_particle(ctypes.byref(particle), dt)

# Função para aplicar força às partículas
def apply_force(particle, fx, fy, fz):
    lib.apply_force(ctypes.byref(particle), fx, fy, fz)

# Função para plotar as partículas
def plot_particles(particles):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Coleta as posições das partículas para plotagem
    xs = [p.x for p in particles]
    ys = [p.y for p in particles]
    zs = [p.z for p in particles]
    
    ax.scatter(xs, ys, zs, color='b')  # Plota as partículas
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_zlabel('Z Position')
    plt.show()

# Exemplo de uso com múltiplas partículas
particles = [Particle(x=i, y=0, z=0, vx=0, vy=0, vz=0, fx=0, fy=0, fz=0, mass=1.0) for i in range(10)]

# Simulação de um passo
for p in particles:
    apply_force(p, 0, -9.8 * p.mass, 0)  # Aplica gravidade
    update_particle(p, 0.01)

plot_particles(particles)
