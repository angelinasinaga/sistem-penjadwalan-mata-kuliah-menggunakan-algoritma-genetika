import random, copy
from Classes import *
from math import ceil, log2
import math
import pandas as pd
Kelas.kelas = [Kelas("11SI1", 20), Kelas("11SI2", 22), Kelas("12SI1", 30), 
               Kelas("12SI2", 30), Kelas("13SI1", 28), Kelas('13I2', 25)]

Dosen.dosen = [Dosen("Mr. Mario Simaremare"), Dosen("Mr. Tennov"), Dosen("Mrs. Parmonangan"),
                Dosen("Mrs. Junita"), Dosen("Mr. Samuel"), Dosen("Mr. Humasak")]

CourseClass.classes = [CourseClass("KUS1002"),CourseClass("MAS1101"),CourseClass("KUS2002"),CourseClass("TIS1101"),
                       CourseClass("KUS1001"),CourseClass("FIS1103"),CourseClass("12S1101"),
                        CourseClass("TIS3001")]

Room.rooms = [Room("GD512", 40), Room("GD513", 40), Room("GD514", 40),
              Room("GD522", 40, is_lab=True),Room("GD523", 40, is_lab=True)]

Schedule.schedules = [Schedule("08:15", "10:00", "Mon"), Schedule("10:15", "12:00", "Mon"),
                      Schedule("13:15", "15:00", "Mon"), Schedule("15:15", "17:00", "Mon"), 
                      Schedule("08:15", "10:00", "tue"), Schedule("10:15", "12:00", "tue"),
                      Schedule("13:15", "15:00", "tue"), Schedule("15:15", "17:00", "tue"),
                      Schedule("08:15", "10:00", "wed"), Schedule("10:15", "12:00", "wed"),
                      Schedule("13:15", "15:00", "wed"), Schedule("15:15", "17:00", "wed"),
                      Schedule("08:15", "10:00", "thu"), Schedule("10:15", "12:00", "thu"),
                      Schedule("13:15", "15:00", "thu"), Schedule("15:15", "17:00", "thu"),]


max_score = None

cpg = []
lts = []
slots = []
bits_needed_backup_store = {}  # to improve performance


def bits_needed(x):
    global bits_needed_backup_store
    r = bits_needed_backup_store.get(id(x))
    if r is None:
        r = int(ceil(log2(len(x))))
        bits_needed_backup_store[id(x)] = r
    return max(r, 1)


def join_cpg_pair(_cpg):
    res = []
    for i in range(0, len(_cpg), 3):
        res.append(_cpg[i] + _cpg[i + 1] + _cpg[i + 2])
    return res


def convert_input_to_bin():
    global cpg, lts, slots, max_score

    cpg = [CourseClass.find("KUS1002"), Dosen.find("Mr. Mario Simaremare"), Kelas.find("13SI1"),
           CourseClass.find("FIS1103"), Dosen.find("Mr. Mario Simaremare"), Kelas.find("13SI1"),
           CourseClass.find("KUS1001"), Dosen.find("Mrs. Junita"), Kelas.find("11SI1"),
           CourseClass.find("TIS1101"), Dosen.find("Mr. Humasak"), Kelas.find("13SI2"),
           CourseClass.find("KUS2002"), Dosen.find("Mr. Samuel"), Kelas.find("13SI2"),
           CourseClass.find("MAS1101"), Dosen.find("Mr. Tennov"), Kelas.find("11SI2"),
           CourseClass.find("KUS1001"), Dosen.find("Mrs. Junita"), Kelas.find("12SI1"),
           CourseClass.find("KUS2002"), Dosen.find("Mrs. Parmonangan"), Kelas.find("13SI2"),
           CourseClass.find("KUS1002"), Dosen.find("Mr. Mario Simaremare"), Kelas.find("13SI2"),
           CourseClass.find("FIS1103"), Dosen.find("Mr. Mario Simaremare"), Kelas.find("13SI2"),
           CourseClass.find("KUS1001"), Dosen.find("Mrs. Junita"), Kelas.find("11SI2"),
           CourseClass.find("TIS3001"), Dosen.find("Mr. Humasak"), Kelas.find("13SI1"),
           CourseClass.find("KUS2002"), Dosen.find("Mr. Samuel"), Kelas.find("13SI1"),
           CourseClass.find("MAS1101"), Dosen.find("Mr. Tennov"), Kelas.find("11SI1"),
           CourseClass.find("KUS1001"), Dosen.find("Mrs. Junita"), Kelas.find("12SI2"),
           CourseClass.find("KUS2001"), Dosen.find("Mrs. Parmonangan"), Kelas.find("13SI2")
           ]

    for _c in range(len(cpg)):
        if _c % 3:  # CourseClass
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(CourseClass.classes), '0')
        elif _c % 3 == 1:  # Dosen
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Dosen.dosen), '0')
        else:  # Kelas
            cpg[_c] = (bin(cpg[_c])[2:]).rjust(bits_needed(Kelas.kelas), '0')

    cpg = join_cpg_pair(cpg)
    for r in range(len(Room.rooms)):
        lts.append((bin(r)[2:]).rjust(bits_needed(Room.rooms), '0'))

    for t in range(len(Schedule.schedules)):
        slots.append((bin(t)[2:]).rjust(bits_needed(Schedule.schedules), '0'))

    # print(cpg)
    max_score = (len(cpg) - 1) * 3 + len(cpg) * 3


def course_bits(chromosome):
    i = 0

    return chromosome[i:i + bits_needed(CourseClass.classes)]


def dosen_bits(chromosome):
    i = bits_needed(CourseClass.classes)

    return chromosome[i: i + bits_needed(Dosen.dosen)]


def kelas_bits(chromosome):
    i = bits_needed(CourseClass.classes) + bits_needed(Dosen.dosen)

    return chromosome[i:i + bits_needed(Kelas.kelas)]


def slot_bits(chromosome):
    i = bits_needed(CourseClass.classes) + bits_needed(Dosen.dosen) + \
        bits_needed(Kelas.kelas)

    return chromosome[i:i + bits_needed(Schedule.schedules)]


def lt_bits(chromosome):
    i = bits_needed(CourseClass.classes) + bits_needed(Dosen.dosen) + \
        bits_needed(Kelas.kelas) + bits_needed(Schedule.schedules)

    return chromosome[i: i + bits_needed(Room.rooms)]


def slot_clash(a, b):
    if slot_bits(a) == slot_bits(b):
        return 1
    return 0


# checks that a faculty member teaches only one course at a time.
def faculty_member_one_class(chromosome):
    scores = 0
    for i in range(len(chromosome) - 1):  # select one cpg pair
        clash = False
        for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j])\
                    and dosen_bits(chromosome[i]) == dosen_bits(chromosome[j]):
                clash = True
        if not clash:
            scores = scores + 1
    return scores


# check that a kelas member takes only one class at a time.
def kelas_member_one_class(chromosomes):
    scores = 0

    for i in range(len(chromosomes) - 1):
        clash = False
        for j in range(i + 1, len(chromosomes)):
            if slot_clash(chromosomes[i], chromosomes[j]) and\
                    kelas_bits(chromosomes[i]) == kelas_bits(chromosomes[j]):
                clash = True
                break
        if not clash:
            scores = scores + 1
    return scores


# checks that a course is assigned to an available classroom. 
def use_spare_classroom(chromosome):
    scores = 0
    for i in range(len(chromosome) - 1):  # select one cpg pair
        clash = False
        for j in range(i + 1, len(chromosome)):  # check it with all other cpg pairs
            if slot_clash(chromosome[i], chromosome[j]) and lt_bits(chromosome[i]) == lt_bits(chromosome[j]):
                clash = True
        if not clash:
            scores = scores + 1
    return scores


# checks that the classroom capacity is large enough for the classes that
def classroom_size(chromosomes):
    scores = 0
    for _c in chromosomes:
        if Kelas.kelas[int(kelas_bits(_c), 2)].size <= Room.rooms[int(lt_bits(_c), 2)].size:
            scores = scores + 1
    return scores


# check that room is appropriate for particular class/lab
def appropriate_room(chromosomes):
    scores = 0
    for _c in chromosomes:
        if CourseClass.classes[int(course_bits(_c), 2)].is_lab == Room.rooms[int(lt_bits(_c), 2)].is_lab:
            scores = scores + 1
    return scores


# check that lab is allocated appropriate time slot
def appropriate_timeslot(chromosomes):
    scores = 0
    for _c in chromosomes:
        if CourseClass.classes[int(course_bits(_c), 2)].is_lab == Schedule.schedules[int(slot_bits(_c), 2)].is_lab_slot:
            scores = scores + 1
    return scores


def evaluate(chromosomes):
    global max_score
    score = 0
    score = score + use_spare_classroom(chromosomes)
    score = score + faculty_member_one_class(chromosomes)
    score = score + classroom_size(chromosomes)
    score = score + kelas_member_one_class(chromosomes)
    score = score + appropriate_room(chromosomes)
    score = score + appropriate_timeslot(chromosomes)
    return score / max_score

def cost(solution):
    return 1 / float(evaluate(solution))

def init_population(n):
    global cpg, lts, slots
    chromosomes = []
    for _n in range(n):
        chromosome = []
        for _c in cpg:
            chromosome.append(_c + random.choice(slots) + random.choice(lts))
        chromosomes.append(chromosome)
    return chromosomes


# Modified Combination of Row_reselect, Column_reselect
def mutate(chromosome):
    # print("Before mutation: ", end="")
    # printChromosome(chromosome)

    rand_slot = random.choice(slots)
    rand_lt = random.choice(lts)

    a = random.randint(0, len(chromosome) - 1)
    
    chromosome[a] = course_bits(chromosome[a]) + dosen_bits(chromosome[a]) +\
        kelas_bits(chromosome[a]) + rand_slot + rand_lt

    # print("After mutation: ", end="")
    # printChromosome(chromosome)


def crossover(population):
    a = random.randint(0, len(population) - 1)
    b = random.randint(0, len(population) - 1)
    cut = random.randint(0, len(population[0]))  # assume all chromosome are of same len
    population.append(population[a][:cut] + population[b][cut:])
    

def selection(population, n):
    population.sort(key=evaluate, reverse=True)
    while len(population) > n:
        population.pop()


def print_chromosome(chromosome):
    print(
          Schedule.schedules[int(slot_bits(chromosome), 2)],"|",
          Room.rooms[int(lt_bits(chromosome), 2)],'|',
          Kelas.kelas[int(kelas_bits(chromosome), 2)], " | ",
          CourseClass.classes[int(course_bits(chromosome), 2)], " | ",
          Dosen.dosen[int(dosen_bits(chromosome), 2)]
          )

# Simple Searching Neighborhood
# It randomly changes timeslot of a class/lab
def ssn(solution):
    rand_slot = random.choice(slots)
    rand_lt = random.choice(lts)
    
    a = random.randint(0, len(solution) - 1)
    
    new_solution = copy.deepcopy(solution)
    new_solution[a] = course_bits(solution[a]) + dosen_bits(solution[a]) +\
        kelas_bits(solution[a]) + rand_slot + lt_bits(solution[a])
    return [new_solution]


# It randomy selects two classes 
def swn(solution):
    a = random.randint(0, len(solution) - 1)
    b = random.randint(0, len(solution) - 1)
    new_solution = copy.deepcopy(solution)
    temp = slot_bits(solution[a])
    new_solution[a] = course_bits(solution[a]) + dosen_bits(solution[a]) +\
        kelas_bits(solution[a]) + slot_bits(solution[b]) + lt_bits(solution[a])

    new_solution[b] = course_bits(solution[b]) + dosen_bits(solution[b]) +\
        kelas_bits(solution[b]) + temp + lt_bits(solution[b])
    return [new_solution]

def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    else:
        return math.exp((old_cost - new_cost) / temperature)

def simulated_annealing():
    alpha = 0.9
    T = 1.0
    T_min = 0.00001
    
    convert_input_to_bin()
    population = init_population(1) # as simulated annealing is a single-state method
    old_cost = cost(population[0])
    # print("Cost of original random solution: ", old_cost)
    # print("Original population:")
    # print(population)

    for __n in range(500):
        new_solution = swn(population[0])
        new_solution = ssn(population[0])
        new_cost = cost(new_solution[0])
        ap = acceptance_probability(old_cost, new_cost, T)
        if ap > random.random():
            population = new_solution
            old_cost = new_cost
        T = T * alpha
    print("\n----------------------- Schedule -----------------------\n")
    for lec in population[0]:
        print_chromosome(lec)
    print("Score: ", evaluate(population[0]))


def genetic_algorithm():
    generation = 0
    convert_input_to_bin()
    population = init_population(3)

    # print("Original population:")
    # print(population)
    print("\n------------- Genetic Algorithm --------------\n")
    while True:
        
        # if termination criteria are satisfied, stop.
        if evaluate(max(population, key=evaluate)) == 1 or generation == 500:
            print("Generations:", generation)
            print("Best Chromosome fitness value", evaluate(max(population, key=evaluate)))
            print("Best Chromosome: ", max(population, key=evaluate))
            for lec in max(population, key=evaluate):
                print_chromosome(lec)
            break
        
        # Otherwise continue
        else:
            for _c in range(len(population)):
                crossover(population)
                selection(population, 5)
                mutate(population[_c])
        generation = generation + 1



def main():
    random.seed()
    genetic_algorithm()
    simulated_annealing()

main()
