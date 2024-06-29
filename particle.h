typedef struct {
    double x, y, z;  // Posição
    double vx, vy, vz;  // Velocidade
    double fx, fy, fz;  // Força total aplicada
    double mass;  // Massa
} Particle;

void update_particle(Particle *p, double dt);
void apply_force(Particle *p, double fx, double fy, double fz);
