'''
    Distributions
'''

import numpy as np
from matplotlib import pyplot as plt

# Seeding for reproducibility
np.random.seed(42)

# sampling from each of the six distributions
beta_samples    = np.random.beta(a=4, b=20, size=1000000) * 100
exp_samples     = np.random.exponential(scale=0.1, size=1000000) * 100
gamma_samples   = np.random.gamma(shape=2, scale=0.1, size=1000000) * 100
laplace_samples = np.random.laplace(loc=0, scale=0.5, size=1000000) * 100
normal_samples  = np.random.normal(loc=0, scale=3, size=1000000)
poisson_samples = np.random.poisson(lam=3, size=1000000)

# plotting histograms for each of the distributions
plt.subplot(3, 2, 1)
plt.hist(beta_samples, bins=np.arange(-5, 51, 1), color='red')
plt.title('Beta')

plt.subplot(3, 2, 2)
plt.hist(exp_samples, bins=np.arange(-1, 51, 1), color='green', alpha=0.5)
plt.title('Exponential')

plt.subplot(3, 2, 3)
plt.hist(gamma_samples, bins=np.arange(-1, 51, 1), color='black', alpha=0.8, orientation='horizontal')
plt.title('Gamma')

plt.subplot(3, 2, 4)
plt.hist(laplace_samples, bins=np.arange(-1, 51, 1), color='orange')
plt.title('Laplace')

plt.subplot(3, 2, 5)
plt.hist(normal_samples, bins=np.arange(-10, 12, 1))
plt.title('Normal')

plt.subplot(3, 2, 6)
plt.hist(poisson_samples, bins=np.arange(-1, 12, 1))
plt.title('Poisson')

# adjust the sub-plots to fit the titles and labels
plt.tight_layout()
# save the plot as plot.png
plt.savefig('plot.png')
