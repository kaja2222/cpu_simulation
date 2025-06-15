from art import text2art
print(text2art("LRU      PAGE   REPLACEMENT"))
class LRU:
    def __init__(self, frames: int, reference: list[int]):
        self.frame = frames
        self.ref    = reference
        self.ram    = []          # posortowana wedlug: pierwszy = najdawniej użyty, ostatni = najnowszy
        self.faults = 0           # liczba fault stron
        self.history = []         # historia poszczegolnych krokow

    def run(self):
        for page in self.ref:
            fault = False
            if page in self.ram:                   # HIT, strona jest w zapisana w pamieci RAM
                self.ram.remove(page)              # usuwam z obecnego miejsca
                self.ram.append(page)              # wstawiam na koniec, aby strona zostala wpisana jako najnowsza
            else:                                  # MISS, page fault, nie ma strony w RAM
                self.faults += 1
                fault = True
                if len(self.ram) == self.frame:                     # jesli RAM jest pełny wyrzuć najdawniej uzywany
                    self.ram.pop(0)                                 # usuwamy pierwszy, czyli najdawniej uzywany
                self.ram.append(page)                               # wczytaj nową stronę
            self.history.append((page, self.ram.copy(), fault))     # tworzymy tabele z krokami, dana strona i aktualna ramka

    def ratio(self):
        return self.faults / len(self.ref) if self.ref else 0.0      # liczba bledow do liczby odwolan, sprawdzamy jak dobrze algorytm dziala (nie dzielimy przez 0)

    def report(self):
        print("\nKrok | Strona | Ramki      |    czy blad")
        print("-" * 44)                                              # printuje 44-razy -, czyli -------------
        for step, (pg, state, fl) in enumerate(self.history, 1):     # step - nr kroku, pg - nr strony, fl - true jesli wystapil page fault
            ram_view = " ".join(f"{s:>2}" for s in state)            # [7,0,1] → " 7 0 1" (każda liczba wyrównana do prawej i odstep 2 wartosci)
            print(f"{step:>4} | {pg:>6} | {ram_view:<14} ",          # wyrowanie lub odsuniecie (>; <), o ilosc jednostek (np. 4)
                  "tak" if fl else "nie")                            # sprawdza page faults
        print("-" * 44)
        print("liczba bledu :", self.faults)
        print("ratio bledu :", f"{self.ratio():.2%}")                # zaokragla do dwoch miejsc po kropce i oblicza procent

frames = int(input("Liczba ramek w pamięci RAM: "))
reference: list[int] = []

with open("reference", encoding="utf-8") as f:
    for ln_no, ln in enumerate(f, 1):
        txt = ln.strip()
        if not txt:                    # pusta linia
            continue
        reference.append(int(txt))


simulation = LRU(frames, reference)
simulation.run()
simulation.report()


