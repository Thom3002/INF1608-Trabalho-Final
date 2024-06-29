#include "particle.h"

void apply_force(Particle *p, double fx, double fy, double fz) {
    p->fx += fx;
    p->fy += fy;
    p->fz += fz;
}
void update_particle(Particle *p, double dt) {
    // Método de Verlet para atualizar a posição
    double new_x = 2 * p->x - p->vx + p->fx / p->mass * dt * dt;
    double new_y = 2 * p->y - p->vy + p->fy / p->mass * dt * dt;
    double new_z = 2 * p->z - p->vz + p->fz / p->mass * dt * dt;

    // Atualiza a velocidade
    p->vx = (new_x - p->x) / dt;
    p->vy = (new_y - p->y) / dt;
    p->vz = (new_z - p->z) / dt;

    // Atualiza a posição
    p->x = new_x;
    p->y = new_y;
    p->z = new_z;
}

