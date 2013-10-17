import random
import math
from Utility import Point

class Sampler:
    def __init__(self):
        pass
    
    def setup_shuffled_indices(self):
        pass

    def sample_unit_square(self):
        pass


class Regular(Sampler):
    def __init__(self, num_samples, num_sets):
        self.num_samples = num_samples
        self.num_sets    = num_sets
        self.count       = 0
        self.jump        = 0
        self.samples     = []
        self.generate_samples()
        
    def generate_samples(self):
        n = int(math.sqrt(self.num_samples))
        for i in range(0, self.num_sets):
            for j in range(0, n):
                for k in range(0, n):
                    self.samples.append(Point((k + 0.5) / n, (j + 0.5) / n, 0.0))

    def sample_unit_square(self):
        if self.count % self.num_samples == 0:
            self.jump = (random.randint(1, self.num_sets) % self.num_sets) * self.num_samples
        index = self.jump + self.count % self.num_samples
        sample = self.samples[index]
        self.count += 1
        return sample


class MultiJittered(Sampler):
    def __init__(self, num_samples, num_sets):
        self.num_samples = num_samples
        self.num_sets = num_sets
        self.count = 0 
        self.jump = 0
        self.samples = []
        self.generate_samples()
        
    def generate_samples(self):
        n = int(math.sqrt(self.num_samples))
        subcell_width = 1.0 / self.num_samples

        # fill the samples array
        for k in range(0, self.num_samples * self.num_sets):
            self.samples.append(Point(0.0, 0.0, 0.0))

        # initial patterns
        for p in range(0, self.num_sets):
            for i in range(0, n):
                for j in range(0, n):
                    self.samples[i * n + j + p * self.num_samples].x = (i * n + j) * subcell_width + random.uniform(0, subcell_width)
                    self.samples[i * n + j + p * self.num_samples].y = (j * n + i) * subcell_width + random.uniform(0, subcell_width)
                   
        # shuffle x coordinates
        for p in range(0, self.num_sets):
            for i in range(0, n):
                for j in range(0, n):
                    k = random.randint(j, n - 1)
                    t                                                = self.samples[i * n + j + p * self.num_samples].x
                    self.samples[i * n + j + p * self.num_samples].x = self.samples[i * n + k + p * self.num_samples].x
                    self.samples[i * n + k + p * self.num_samples].x = t

        # shuffle y coordinates
        for p in range(0, self.num_sets):
            for i in range(0, n):
                for j in range(0, n):
                    k = random.randint(j, n - 1)
                    t                                                = self.samples[i * n + j + p * self.num_samples].y
                    self.samples[i * n + j + p * self.num_samples].y = self.samples[i * n + k + p * self.num_samples].y
                    self.samples[i * n + k + p * self.num_samples].y = t

    def sample_unit_square(self):
        if self.count % self.num_samples == 0:
            self.jump = (random.randint(1, self.num_sets) % self.num_sets) * self.num_samples
        index = self.jump + self.count % self.num_samples
        sample = self.samples[index]
        self.count += 1
        return sample

