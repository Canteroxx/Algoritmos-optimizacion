import matplotlib.pyplot as plt
import numpy as np


def ordenar_puntos(puntos):
    centro = np.mean(puntos, axis=0)
    return sorted(puntos, key=lambda p: np.arctan2(p[1]-centro[1], p[0]-centro[0]))

def inter(m):
    p=[]
    for i in range(len(m)-1):
        for j in range(i+1,len(m)):
            a1,b1,c1=m[i]; a2,b2,c2=m[j]
            d=a1*b2-a2*b1
            if d:
                x=(b1*c2-b2*c1)/d
                y=(c1*a2-c2*a1)/d
                p.append((x,y))
    return p

# --- FILTRAR FACTIBLES ---
def factibles(puntos, restricciones):
    validos = []
    for x,y in puntos:
        if all(a*x + b*y + c <= 1e-6 for a,b,c in restricciones):
            validos.append((x,y))
    return validos

# --- FUNCIÓN OBJETIVO ---
def evaluar(puntos):
    mejor = None
    max_z = float('-inf')
    for x,y in puntos:
        z = 2*x + 2*y
        if z > max_z:
            max_z = z
            mejor = (x,y,z)
    return mejor

# --- RESTRICCIONES ---
matriz = [
    [2,1,-100],   # r1
    [1,3,-80],    # r2
    [1,0,-45],    # r3
    [1,0,-100],   # r4
    [-1,0,0],     # r5  x>=0
    [0,-1,0],      # r6  y>=0
    [-2,0,0],     # r7  x>=0
    [0,-2,0]      # r8  y>=0    
]

# --- CALCULO ---
puntos = inter(matriz)
fact = factibles(puntos, matriz)
opt = evaluar(fact)

# --- GRAFICO ---
x = np.linspace(-30, 110, 500)

plt.figure(figsize=(10,7))

# r1
plt.plot(x, (100 - 2*x), '--', color='blue')
# r2
plt.plot(x, (80 - x)/3, '--', color='orange')
# r3
plt.axvline(x=45, linestyle='--', label="r3: 1*x1 <= 45")
# r4
plt.axvline(x=100, linestyle='--', color='red', label="r4: 1*x1 <= 100")
# r5
plt.axvline(x=0, linestyle='--', color='purple', label="r5: 1*x1 >= 0")
# r6
plt.axhline(y=0, linestyle='--', color='brown', label="r6: 1*x2 >= 0")
# r7
plt.axhline(y=0, linestyle='--', color='pink', label="r7: 1*x1 >= 0")
# r8
plt.axhline(y=0, linestyle='--', color='gray', label="r8: 1*x2 >= 0")

# --- PUNTOS FACTIBLES ---
for px,py in fact:
    z = 2*px + 2*py
    plt.scatter(px, py, color='black')
    plt.text(px+1, py+1, f"({px:.1f},{py:.1f}), z={z:.1f}")

# --- SOMBREADO ---
if fact:
	fact_ordenados = ordenar_puntos(fact)
	xs, ys = zip(*fact_ordenados)
	plt.fill(xs, ys, color='lightblue', alpha=0.5)

# --- FUNCION OBJETIVO ---
x_line = np.linspace(0,100,100)
y_line = (112 - 2*x_line)/2
plt.plot(x_line, y_line, color='green', label="Función Objetivo: 2x1 + 2x2 = 112")

# --- OPTIMO ---
if opt:
    x_opt, y_opt, z = opt
    plt.scatter(x_opt, y_opt, color='green', marker='X', s=120, label="Óptimo")
    plt.text(x_opt+2, y_opt, f"Óptimo\n({x_opt:.1f},{y_opt:.1f})")

# --- DETALLES ---
plt.xlim(-30,110)
plt.ylim(-10,110)
plt.xlabel("x1")
plt.ylabel("x2")
plt.title("Método Gráfico: Región Factible y Solución Óptima")
plt.grid()
plt.legend()

plt.show()