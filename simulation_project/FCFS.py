from art import text2art
import csv
a = text2art("FIRST COME FIRST SERVE")
print(a)


class Process:
    def __init__(self, name: str, arrival: int, burst: int):
        self.name = name        # nazwa procesu
        self.arrival = arrival  # czas w ktorym proces przyszedl
        self.burst = burst      # czas wykonywania procesu
        self.wait = 0           # ile czasu proces czekał na wykonanie
        self.exit = 0           # chwila w której proces się zakończył
        self.tat = 0            # turn around time (exit - arrival), czas w ktorej przyszedl - w ktorej sie skonczyl


process: list[Process] = []     # tworzymy pusta liste z obiektami nalezacymi do klasy Process

with open("processes.csv", newline="", encoding="utf-8") as f:   # arival, burst
    reader = csv.reader(f, skipinitialspace=True)                # usuwamy spację po przecinku
    for i, row in enumerate(reader, 1):
        if not row:                                              # całkiem pusta linia
            continue
        if len(row) < 2:                                         # za mało pól
            continue

        arrival, burst = map(int, (row[0], row[1]))
        process.append(Process(f"proces {i}", arrival, burst))

number = len(process)
process.sort(key=lambda item: item.arrival)                # lambda - anonimowa funkcja dla podanej strony p, zwraca liczbe odwolan


for index, p in enumerate(process):                        # index kazdego p (p to poszczegolny proces)
    if index == 0:                                         # dla pierwszego procesu
        p.exit = p.arrival + p.burst                       # czas wyjscia to czas przyjscia + wykonania
    else:
        start  = max(p.arrival, process[index - 1].exit)   # porownujemy czas przyjscia i czas wykonania 1 procesu
        p.exit = start + p.burst                           # bo cpu moze czekac na nastepny proces, po wykonaniu 1

    p.tat  = p.exit - p.arrival
    p.wait = p.tat  - p.burst

avg_wait = sum(p.wait for p in process)                    # obliczamy sredni czas czekania
avg_wait /= number


print("\nNAME     | ARR | BRST | EXIT | TAT | WAIT  ")
print("-----------------------------------------")
for p in process:
    print(f"{p.name:>3} | {p.arrival:>3} | {p.burst:>3} | "
          f"{p.exit:>4} | {p.tat:>4} | {p.wait:>4}")        # ">" wyrownaj do prawej, "3" i zarezerwuj miejsce na 3 znaki
print(f"\nAverage waiting time: {avg_wait:.2f}")            # .2f - liczba zmiennoprzecinkowa ( 2 cyfr po przecinku )








