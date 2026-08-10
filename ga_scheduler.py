import random
import sys

population_size = int(sys.argv[1])
generations = int(sys.argv[2])
print("\n========== GA PARAMETERS ==========")
print("Population Size:", population_size)
print("Generations:", generations)

processing_time = {
    "Corolla": 5,
    "Camry": 7,
    "RAV4": 6,
    "Highlander": 8,
    "Prius": 4
}

assembly_capacity = 28

# -----------------------------
# Vehicles
# -----------------------------
vehicles = [
    "Corolla",
    "Camry",
    "RAV4",
    "Highlander",
    "Prius"
]

# -----------------------------
# Create Initial Population
# -----------------------------
population = []

for i in range(population_size):
    chromosome = random.sample(vehicles, len(vehicles))
    population.append(chromosome)

# -----------------------------
# Fitness Function
# -----------------------------
def fitness(chromosome):

    total_time = 0
    score = 100

    for car in chromosome:
        total_time += processing_time[car]

    # Penalty if production exceeds capacity
    if total_time > assembly_capacity:
        score -= (total_time - assembly_capacity) * 5

    # Priority Vehicles
    if chromosome[0] == "Corolla":
        score += 15

    if chromosome[1] == "Camry":
        score += 10

    if chromosome[2] == "Prius":
        score += 5

    # Shorter production time gets higher score
    score += max(0, 50 - total_time)

    return score

# -----------------------------
# Show Population
# -----------------------------
print("========== INITIAL POPULATION ==========\n")

for i, chromosome in enumerate(population, start=1):
    print(f"Chromosome {i}: {chromosome}")
    print("Fitness:", fitness(chromosome))
    print()


print("\n========== GENETIC ALGORITHM ==========")
print(f"Population Size : {population_size}")
print(f"Generations     : {generations}")
print("Selection       : Best Parents")
print("Crossover       : Order Crossover")
print("Mutation        : Swap Mutation")
print("---------------------------------------")

# -----------------------------
# Best Chromosome
# -----------------------------
for generation in range(generations):

    print(
    f"Generation {generation + 1}/{generations} "
    f"| Population = {len(population)}"
)
    population.sort(key=fitness, reverse=True)

    parent1 = population[0]
    parent2 = population[1]

    new_population = population[:2]

    while len(new_population) < population_size:

        point = random.randint(1, len(vehicles)-2)

        child = parent1[:point]

        for gene in parent2:
            if gene not in child:
                child.append(gene)

        # Mutation
        if random.random() < 0.2:

            i, j = random.sample(range(len(child)),2)

            child[i], child[j] = child[j], child[i]

        new_population.append(child)

    population = new_population

    best = max(population,key=fitness)

    print(
    f"Generation {generation+1:02d} | Best Fitness = {fitness(best)}"
)

    print(
        f"Generation {generation+1} | Fitness = {fitness(best)}"
    )

# -----------------------------
# Select Parents
# -----------------------------
parent1 = population[0]
parent2 = population[1]

print("\n========== PARENTS ==========\n")
print("Parent 1:", parent1)
print("Parent 2:", parent2)

# -----------------------------
# Crossover
# -----------------------------
point = random.randint(1, len(vehicles) - 2)

child = parent1[:point]

for gene in parent2:
    if gene not in child:
        child.append(gene)

print("\n========== CHILD ==========\n")
print(child)

# -----------------------------
# Mutation
# -----------------------------
mutated_child = child.copy()

index1, index2 = random.sample(range(len(mutated_child)), 2)

mutated_child[index1], mutated_child[index2] = (
    mutated_child[index2],
    mutated_child[index1]
)

print("\n========== MUTATED CHILD ==========\n")
print(mutated_child)

makespan = sum(processing_time[v] for v in mutated_child)

print("\n========== SCHEDULE ==========")
print("Processing Time:", makespan, "hours")

best = max(population,key=fitness)

print("\n========== FINAL RESULT ==========")

print(best)

print("Fitness =",fitness(best))

