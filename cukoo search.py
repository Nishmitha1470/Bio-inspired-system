import numpy as np

P = 1000
L = 2
E = 200e9
rho = 7850
stress_max = 150e6
deflection_max = 0.005

def objective(x):
    b, h = x

    weight = rho * L * b * h
    stress = (6 * P * L) / (b * h**2)
    deflection = (4 * P * L**3) / (E * b * h**3)

    penalty = 0

    if stress > stress_max:
        penalty += 1000 * (stress / stress_max - 1)**2

    if deflection > deflection_max:
        penalty += 1000 * (deflection / deflection_max - 1)**2

    return weight + penalty


n = 20
iterations = 100
pa = 0.25

lower = np.array([0.01, 0.01])
upper = np.array([0.1, 0.2])

nests = np.random.uniform(lower, upper, (n, 2))
fitness = np.array([objective(x) for x in nests])

best = nests[np.argmin(fitness)].copy()

for t in range(iterations):

    for i in range(n):

        step = np.random.normal(0, 0.1, 2)
        new = nests[i] + step * (nests[i] - best)
        new = np.clip(new, lower, upper)

        if objective(new) < fitness[i]:
            nests[i] = new
            fitness[i] = objective(new)

    for i in range(n):

        if np.random.rand() < pa:

            new = np.random.uniform(lower, upper)

            if objective(new) < fitness[i]:
                nests[i] = new
                fitness[i] = objective(new)

    best = nests[np.argmin(fitness)].copy()

b, h = best

print("Optimal Beam Design")
print("Width:", round(b, 5), "m")
print("Height:", round(h, 5), "m")
print("Minimum Weight:", round(rho * L * b * h, 4), "kg")
print("Stress:", round((6*P*L)/(b*h**2) / 1e6, 2), "MPa")
print("Deflection:", round((4*P*L**3)/(E*b*h**3), 6), "m")
