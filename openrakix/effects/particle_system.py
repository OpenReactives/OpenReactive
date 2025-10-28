import numpy as np
import random


class Particle:
    def __init__(self, position, velocity, life_time, color):
        self.position = np.array(position, dtype=np.float32)
        self.velocity = np.array(velocity, dtype=np.float32)
        self.life_time = life_time
        self.age = 0
        self.color = np.array(color, dtype=np.float32)
        self.size = 1.0
        self.alive = True

    def update(self, delta_time, gravity=None):
        if not self.alive:
            return

        self.age += delta_time

        if self.age >= self.life_time:
            self.alive = False
            return

        self.position += self.velocity * delta_time

        if gravity is not None:
            self.velocity += np.array(gravity) * delta_time


class ParticleSystem:
    def __init__(self, max_particles=1000):
        self.max_particles = max_particles
        self.particles = []
        self.emission_rate = 10
        self.emission_timer = 0
        self.gravity = np.array([0, -9.8, 0])
        self.spawn_position = np.array([0, 0, 0])
        self.spawn_radius = 0.5
        self.velocity_range = ([-1, 1, -1], [1, 3, 1])
        self.life_time_range = (1.0, 3.0)
        self.color_start = np.array([1, 1, 1, 1])
        self.color_end = np.array([1, 1, 1, 0])
        self.size_start = 1.0
        self.size_end = 0.1
        self.enabled = True

    def emit(self, count=1):
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                break

            offset = np.array([
                random.uniform(-self.spawn_radius, self.spawn_radius),
                random.uniform(-self.spawn_radius, self.spawn_radius),
                random.uniform(-self.spawn_radius, self.spawn_radius)
            ])

            position = self.spawn_position + offset

            velocity = np.array([
                random.uniform(self.velocity_range[0][0], self.velocity_range[1][0]),
                random.uniform(self.velocity_range[0][1], self.velocity_range[1][1]),
                random.uniform(self.velocity_range[0][2], self.velocity_range[1][2])
            ])

            life_time = random.uniform(self.life_time_range[0], self.life_time_range[1])

            particle = Particle(position, velocity, life_time, self.color_start)
            self.particles.append(particle)

    def update(self, delta_time):
        if not self.enabled:
            return

        self.emission_timer += delta_time
        emissions_this_frame = int(self.emission_timer * self.emission_rate)

        if emissions_this_frame > 0:
            self.emit(emissions_this_frame)
            self.emission_timer = 0

        for particle in self.particles:
            particle.update(delta_time, self.gravity)

            if particle.alive:
                life_progress = particle.age / particle.life_time
                particle.color = self.color_start * (1 - life_progress) + self.color_end * life_progress
                particle.size = self.size_start * (1 - life_progress) + self.size_end * life_progress

        self.particles = [p for p in self.particles if p.alive]

    def clear(self):
        self.particles = []

    def get_particle_count(self):
        return len(self.particles)

    def set_spawn_position(self, x, y, z):
        self.spawn_position = np.array([x, y, z])

    def set_gravity(self, x, y, z):
        self.gravity = np.array([x, y, z])

    def set_emission_rate(self, rate):
        self.emission_rate = rate

    def set_velocity_range(self, min_vel, max_vel):
        self.velocity_range = (min_vel, max_vel)

    def set_life_time_range(self, min_life, max_life):
        self.life_time_range = (min_life, max_life)

    def set_color_gradient(self, start_color, end_color):
        self.color_start = np.array(start_color)
        self.color_end = np.array(end_color)

    def set_size_range(self, start_size, end_size):
        self.size_start = start_size
        self.size_end = end_size
