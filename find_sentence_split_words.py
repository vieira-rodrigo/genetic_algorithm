# Example of a Genetic Algorithm implementation in order to find a sentence.
# This example splits the sentence words and apply the Genetic Algorithm in order to find each word.
# By Rodrigo Vieira (vieirarodrigo1990@gmail.com)

import random
import string
import time

# init constants
GENERATIONS_LIMIT = 50000
POPULATION_LEN = 100
MUTABILITY_FACTOR = .1
ALPHABET = string.printable + "ÀàÂâÃãÁáÓóÇçÚúÊêÉé"


def _calc_fitness(individual, target):
    fitness = 0
    for index, c in enumerate(individual):
        if c == target[index]:
            fitness += 1

    return fitness


def _evaluate(pop, target):
    pop_fit = {}
    for i in pop:
        pop_fit[i] = _calc_fitness(i, target)

    return sorted(pop_fit, key=pop_fit.get, reverse=True)


def _mutate(individual):
    if random.uniform(0, 1) > MUTABILITY_FACTOR:
        return individual

    individual_list = list(individual)
    position = random.randint(0, len(individual) - 1)
    individual_list[position] = random.choice(ALPHABET)
    return "".join(individual_list)


def _crossover_and_mutate(pop, p):
    new_population = []
    for i in range(POPULATION_LEN // 2):
        parents = random.sample(pop, k=2)
        child_1 = parents[0][:p] + parents[1][p:p * 2] + parents[0][p * 2: len(parents[0])]
        child_2 = parents[1][:p] + parents[0][p:p * 2] + parents[1][p * 2: len(parents[1])]
        new_population.append(_mutate(child_1))
        new_population.append(_mutate(child_2))

    return new_population


# read the sentence
sentence_target = input("Type a word or a sentence: ")
sentence_start = time.time()
words = sentence_target.split()
sentence_result = ""

for word in words:
    start = time.time()
    the_best = ""
    current_generation = 0
    population = ["".join(random.choices(ALPHABET, k=len(word))) for i in range(POPULATION_LEN)]

    while current_generation < GENERATIONS_LIMIT:
        current_generation += 1

        # evaluate the population based on fitness function
        evaluated_pop = _evaluate(population, word)
        the_best = evaluated_pop[0]

        # stop the search if the target is founded
        if the_best == word:
            break

        # select the bests individuals from population
        selected_pop = evaluated_pop[:len(population) // 2]

        # create a new population with crossover and mutation
        target_len = len(word)
        point = 1 if target_len < 3 else target_len // 3
        population = _crossover_and_mutate(selected_pop, point)

    end = time.time()
    sentence_result += the_best + " "

    print("\n -------------- WORLD RESULT --------------")
    print("Word Target: {}".format(word))
    print("Generations: {}".format(current_generation))
    print("The best result: {}".format(the_best))
    print("Word Time: {} seconds.".format(int(end - start)))

sentence_end = time.time()
print("\n ################## SENTENCE RESULT ##################")
print("Target: {}".format(sentence_target))
print("Result: {}".format(sentence_result))
print("Time: {} seconds.".format(int(sentence_end - sentence_start)))
