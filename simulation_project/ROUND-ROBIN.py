from art import text2art
import csv
a = text2art("ROUND ROBIN SCHEDULLING")
print(a)


class Process:
    def __init__(self, name: str, arrival: int, burst: int):
        self.name = name            # nazwa procesu
        self.arrival = arrival      # czas w ktorym proces przyszedl
        self.burst = burst          # czas wykonywania procesu
        self.remaining = burst      # pozostały czas do wykonania procesu
        self.wait = 0               # ile czasu proces czekał na wykonanie
        self.exit = 0               # chwila w której proces się zakończył
        self.tat = 0                # turn around time (exit - arrival), czas w ktorej przyszedl - w ktorej sie skonczyl


quantum = int(input("Enter time quantum: "))    # przydzielony czas dla kazdego procesu
proces: list[Process] = []                      # tworzymy pusta liste z obiektami nalezacymi do klasy Process



with open("processes.csv", encoding="utf-8") as f:       # otwieramy plik z danymi
    reader = csv.reader(f, skipinitialspace=True)        # usuwamy spacje po przecinku
    for i, row in enumerate(reader, 1):
        # pomijamy puste lub niekompletne wiersze
        if len(row) < 2 or not row[0].strip() or not row[1].strip():
            continue
        arrival, burst = map(int, (row[0], row[1]))
        proces.append(Process(f"Process{i}", arrival, burst))

number = len(proces)

proces.sort(key=lambda p: p.arrival)   # sortujemy wedlug czasu przyjścia, lambda to anonimowa funkcja, sprawdza dla kazdego p czas przyjscia
time       = 0                         # aktualny czas
ready_in_queque    = []                # lista procesów gotowych i czekających na wykonanie
index_next   = 0                       # wskaźnik na kolejny, który dopiero nadejdzie
gantt      = []                        # podglądowe wartości, które procesy kiedy sie wykonywały

while ready_in_queque or index_next < number:                           # jesli są procesy w kolejce lub index_next jest mniejszą liczbą od number (liczby wszystkich procesow)
    # dodaje nowe procesy, które właśnie przyszły
    while index_next < number and proces[index_next].arrival <= time:   # jesli czas przybycia procesu jest mniejszy lub rowny aktualnego czasu, proces zostaje dodany do kolejki
        ready_in_queque.append(proces[index_next])
        index_next += 1

    if not ready_in_queque:                                             # CPU czeka na pierwszy proces, jesli jeszcze nie przybyl
        time = proces[index_next].arrival                               # czas zamienia sie w czas przybycia pierwszego procesu
        continue

    # bierzemy proces z początku kolejki
    p = ready_in_queque.pop(0)
    exec_time = min(quantum, p.remaining)                               # sprawdzamy czy proces wykonal sie w czasie przydzielonym quantum
    start     = time
    time     += exec_time
    p.remaining -= exec_time                                            # obliczamy pozostaly czas do wykonania procesu
    gantt.append((p.name, start, time))                                 # dodajemy wartosci do gantt dla kazdego czasu quantum

    while index_next < number and proces[index_next].arrival <= time:   # dodaje ewentualne „nowe” procesy przybyłych w trakcie trwania quantum
        ready_in_queque.append(proces[index_next])
        index_next += 1

    if p.remaining == 0:                                                # sprawdzamy czy proces skończył sie czy wraca na koniec kolejki
        p.completion = time
        p.tat  = p.completion - p.arrival
        p.wait = p.tat - p.burst
    else:
        ready_in_queque.append(p)                                       # wraca na koniec, jesli czas remaining nie jest rowny 0


avg_wait = sum(p.wait for p in proces) / number                         # sredni czas czekania i wykonywania
avg_tat  = sum(p.tat for p in proces) / number

print("\n Name   | ARRIVAL | BRST | COMPL | TAT | WAIT")
print("------------------------------------------")
for p in proces:
    print(f"{p.name:>3} | {p.arrival:>6} | {p.burst:>4} | "             # ">" wyrownaj do prawej, "3" i zarezerwuj miejsce na 3 znaki
          f"{p.completion:>4} | {p.tat:>4} | {p.wait:>4}")

print(f"\nAverage waiting time   : {avg_wait:.2f}")
print(f"Average turn-around time: {avg_tat:.2f}")

# wyswietlenie informacji gant
print("\nGantt chart:")
for seg in gantt:
    print(f"{seg[0]}: {seg[1]} → {seg[2]}")

