import random
import math
from Utility import Point

class Sampler:
    def __init__(self, num_samples, num_sets):
        self.num_samples = num_samples
        self.num_sets    = num_sets
        self.count       = 0
        self.jump        = 0
        self.samples     = []
        self.hemisphere_samples = []
        self.generate_samples()
    
    def setup_shuffled_indices(self):
        pass

    def map_samples_to_hemisphere(self, exp):
        PI = math.pi
        for sample in self.samples:
            cos_phi = math.cos(2.0 * PI * sample.x)
            sin_phi = math.sin(2.0 * PI * sample.x)
            cos_theta = pow((1.0 - sample.y), 1.0 / (exp + 1.0))
            sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)
            pu = sin_theta * cos_phi
            pv = sin_theta * sin_phi
            pw = cos_theta
            self.hemisphere_samples.append(Point(pu, pv, pw))

    def sample_unit_square(self):
        if self.count % self.num_samples == 0:
            self.jump = (random.randint(1, self.num_sets) % self.num_sets) * self.num_samples
        index = self.jump + self.count % self.num_samples
        sample = self.samples[index]
        self.count += 1
        return sample

    def sample_hemisphere(self):
        if self.count % self.num_samples == 0:
            self.jump = (random.randint(1, self.num_sets) % self.num_sets) * self.num_samples
        index = self.jump + self.count % self.num_samples
        sample = self.hemisphere_samples[index]
        self.count += 1
        return sample
        

class Regular(Sampler):        
    def generate_samples(self):
        n = int(math.sqrt(self.num_samples))
        for i in range(self.num_sets):
            for j in range(n):
                for k in range(n):
                    self.samples.append(Point((k + 0.5) / n, (j + 0.5) / n, 0.0))


class MultiJittered(Sampler):        
    def generate_samples(self):
        n = int(math.sqrt(self.num_samples))
        subcell_width = 1.0 / self.num_samples

        # fill the samples array
        for k in range(self.num_samples * self.num_sets):
            self.samples.append(Point(0.0, 0.0, 0.0))

        # initial patterns
        for p in range(self.num_sets):
            for i in range(n):
                for j in range(n):
                    self.samples[i * n + j + p * self.num_samples].x = (i * n + j) * subcell_width + random.uniform(0, subcell_width)
                    self.samples[i * n + j + p * self.num_samples].y = (j * n + i) * subcell_width + random.uniform(0, subcell_width)
                   
        # shuffle x coordinates
        for p in range(self.num_sets):
            for i in range(n):
                for j in range(n):
                    k = random.randint(j, n - 1)
                    t                                                = self.samples[i * n + j + p * self.num_samples].x
                    self.samples[i * n + j + p * self.num_samples].x = self.samples[i * n + k + p * self.num_samples].x
                    self.samples[i * n + k + p * self.num_samples].x = t

        # shuffle y coordinates
        for p in range(self.num_sets):
            for i in range(n):
                for j in range(n):
                    k = random.randint(j, n - 1)
                    t                                                = self.samples[i * n + j + p * self.num_samples].y
                    self.samples[i * n + j + p * self.num_samples].y = self.samples[i * n + k + p * self.num_samples].y
                    self.samples[i * n + k + p * self.num_samples].y = t
