import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Tygrys:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.upper_vector_length = random.uniform(1, 3)
        self.lower_vector_length = random.uniform(1, 3)
        self.left_point = [0, 0]
        self.right_point = [0, 0]
        self.upper_left_point = [0, 0]
        self.upper_right_point = [0, 0]

def polar_angle(p, q):
    return np.arctan2(q.y - p.y, q.x - p.x)

def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0  # Colinear points
    return 1 if val > 0 else -1  # Clockwise or Counterclockwise

def graham_scan_step_by_step(tygrysy):
    n = len(tygrysy)
    if n < 3:
        return tygrysy

    tygrysy.sort(key=lambda tygrys: (tygrys.x, tygrys.y))
    start_point = tygrysy[0]
    tygrysy[1:] = sorted(tygrysy[1:], key=lambda tygrys: polar_angle(start_point, tygrys))

    stack_list = [tygrysy[0], tygrysy[1]]
    stack_copy_list = [stack_list.copy()]

    for i in range(2, n):
        while len(stack_list) > 1 and orientation(stack_list[-2], stack_list[-1], tygrysy[i]) != -1:
            stack_list.pop()
        stack_list.append(tygrysy[i])
        stack_copy_list.append(stack_list.copy())

    return stack_copy_list

# Inicjalizacja losowych punktów (tygrysów)
random.seed(42)
tygrysy = [Tygrys(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(20)]

# Rysowanie otoczki wypukłej krok po kroku
stack_copy_list = graham_scan_step_by_step(tygrysy)

# Wizualizacja wyników
punkty_x, punkty_y = zip(*[(tygrys.x, tygrys.y) for tygrys in tygrysy])

# Przechowywanie współrzędnych otoczki
otoczka_x, otoczka_y = [], []

def update(frame):
    global otoczka_x, otoczka_y
    plt.clf()
    
    # Rysowanie otoczki
    if frame < len(stack_copy_list):
        stack_copy = stack_copy_list[frame]
        otoczka_x, otoczka_y = zip(*[(punkt.x, punkt.y) for punkt in stack_copy])
        plt.plot(otoczka_x , otoczka_y)
    
    # Aktualizacja pozycji punktów i generowanie wektorów
    for tygrys in tygrysy:
        tygrys.x += random.uniform(-0.05, 0.05)
        tygrys.y += random.uniform(-0.05, 0.05)
        tygrys.x = max(0, min(tygrys.x, 10))
        tygrys.y = max(0, min(tygrys.y, 10))
        upper_vector = [tygrys.x, tygrys.y + tygrys.upper_vector_length]
        lower_vector = [tygrys.x, tygrys.y - tygrys.lower_vector_length]
        
        # Punkt na lewo od końcówki wektora górnego
        tygrys.left_point = [upper_vector[0] - np.cos(np.pi/2.5), upper_vector[1] - np.sin(np.pi/2.5)]
        # Punkt na prawo od końcówki wektora górnego
        tygrys.right_point = [upper_vector[0] + np.cos(np.pi/2.5), upper_vector[1] - np.sin(np.pi/2.5)]
        
        # Punkt na lewo od końcówki wektora dolnego
        tygrys.upper_left_point = [lower_vector[0] - np.cos(np.pi/2.5), lower_vector[1] + np.sin(np.pi/2.5)]
        # Punkt na prawo od końcówki wektora dolnego
        tygrys.upper_right_point = [lower_vector[0] + np.cos(np.pi/2.5), lower_vector[1] + np.sin(np.pi/2.5)]
        
        # Rysowanie wektorów górnego i dolnego
        plt.plot([tygrys.x, upper_vector[0]], [tygrys.y, upper_vector[1]], color='orange', linestyle='--')
        plt.plot([tygrys.x, lower_vector[0]], [tygrys.y, lower_vector[1]], color='purple', linestyle='--')
        
        # Rysowanie linii łączących punkty
        plt.plot([tygrys.left_point[0], tygrys.upper_left_point[0], lower_vector[0], tygrys.upper_right_point[0], tygrys.right_point[0], tygrys.left_point[0]],
                 [tygrys.left_point[1], tygrys.upper_left_point[1], lower_vector[1], tygrys.upper_right_point[1], tygrys.right_point[1], tygrys.left_point[1]], color='purple')
    
    # Rysowanie punktów
    plt.scatter([tygrys.x for tygrys in tygrysy], [tygrys.y for tygrys in tygrysy], label='Punkty (Tygrysy)', color='blue')
    
    # Rysowanie aktualnej otoczki
    if frame>18:
        plt.plot(otoczka_x + (otoczka_x[0],), otoczka_y + (otoczka_y[0],), color='blue')
    
    plt.xlabel('Współrzędna X')
    plt.ylabel('Współrzędna Y')
    plt.title('Otoczka wypukła dla Tygrysów - Krok {}'.format(frame))
    plt.legend()

# Inicjalizacja animacji
animation = FuncAnimation(plt.figure(), update, frames=len(stack_copy_list)+50, interval=1000, repeat=False)

# Wyświetlenie animacji
plt.show()
