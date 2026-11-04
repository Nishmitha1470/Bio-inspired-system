import random
import math
import matplotlib.pyplot as plt

random.seed(42)

cities = [
    (2, 3), (5, 4), (1, 8), (8, 8),
    (7, 2), (4, 7), (9, 5), (3, 1)
]

n = len(cities)

distance = [[0] * n for _ in range(n)]

for i in range(n):
    for j in range(n):
        distance[i][j] = math.sqrt(
            (cities[i][0] - cities[j][0]) ** 2 +
            (cities[i][1] - cities[j][1]) ** 2
        )

ants = 20
iterations = 100

alpha = 1
beta = 2
evaporation = 0.5
Q = 100

pheromone = [[1.0] * n for _ in range(n)]

best_route = None
best_distance = float('inf')

convergence = []

for iteration in range(iterations):

    all_routes = []

    for ant in range(ants):

        start = random.randint(0, n - 1)
        route = [start]
        unvisited = list(range(n))
        unvisited.remove(start)

        while unvisited:

            current = route[-1]
            probabilities = []

            for city in unvisited:

                p = (pheromone[current][city] ** alpha) * (
                    (1 / distance[current][city]) ** beta
                )

                probabilities.append(p)

            total = sum(probabilities)

            probabilities = [p / total for p in probabilities]

            next_city = random.choices(
                unvisited, weights=probabilities
            )[0]

            route.append(next_city)
            unvisited.remove(next_city)

        route.append(start)

        total_distance = sum(
            distance[route[i]][route[i + 1]]
            for i in range(n)
        )

        all_routes.append((route, total_distance))

        if total_distance < best_distance:
            best_distance = total_distance
            best_route = route.copy()

    for i in range(n):
        for j in range(n):
            pheromone[i][j] *= (1 - evaporation)

    for route, route_distance in all_routes:

        deposit = Q / route_distance

        for i in range(n):
            a = route[i]
            b = route[i + 1]

            pheromone[a][b] += deposit
            pheromone[b][a] += deposit

    convergence.append(best_distance)

print("Best Route:", best_route)
print("Minimum Distance:", round(best_distance, 2))

plt.figure(figsize=(7, 5))

x = [cities[i][0] for i in best_route]
y = [cities[i][1] for i in best_route]

plt.plot(x, y, 'bo-')

for i in range(n):
    plt.text(cities[i][0], cities[i][1], str(i))

plt.title("Travelling Salesman Problem using ACO")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.grid()
plt.show()

plt.figure(figsize=(7, 5))

plt.plot(convergence)

plt.title("ACO Convergence Graph")
plt.xlabel("Iterations")
plt.ylabel("Best Distance")
plt.grid()
plt.show()
