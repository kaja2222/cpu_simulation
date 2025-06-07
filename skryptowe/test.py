import matplotlib.pyplot as plt
import numpy as np

# Dane z symulacji
steps = np.arange(1, 9)

# 1 = page‑fault, 0 = hit
lru_fault_flags = np.array([1, 1, 1, 1, 0, 1, 0, 1])
mfu_fault_flags = np.array([1, 1, 1, 1, 0, 1, 1, 1])

# Skumulowana liczba błędów na kolejnych krokach
lru_cumulative = np.cumsum(lru_fault_flags)
mfu_cumulative = np.cumsum(mfu_fault_flags)

# Wykres słupkowy: łączna liczba błędów
plt.figure()
plt.bar(['LRU', 'MFU'], [lru_fault_flags.sum(), mfu_fault_flags.sum()])
plt.title('Łączna liczba błędów stronicowania')
plt.ylabel('Błędy stronicowania')
plt.tight_layout()
plt.show()

# Wykres liniowy: skumulowane błędy w czasie
plt.figure()
plt.plot(steps, lru_cumulative, marker='o', label='LRU')
plt.plot(steps, mfu_cumulative, marker='o', label='MFU')
plt.title('Skumulowane błędy stronicowania na kolejnych krokach')
plt.xlabel('Krok symulacji')
plt.ylabel('Liczba błędów (narastająco)')
plt.legend()
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
plt.tight_layout()
plt.show()
