import matplotlib.pyplot as plt
import numpy as np


m = [[2,1,100],
	 [1,3,80],
	 [1,0,45],
     [0,1,100],
     [-1,0,0], # x1 >= 0
	 [0,-1,0]  # x2 >= 0
     ]

fo = [2, 2]
v = "max"

def intersecciones(m):
    puntos = []
    lec = len(m)
    for i in range(lec - 1):
        for j in range(i + 1, lec):
            a1, b1, c1 = m[i]
            a2, b2, c2 = m[j]
            Det = a1 * b2 - a2 * b1
            if Det != 0:
                Dx1 = c1 * b2 - c2 * b1
                Dx2 = a1 * c2 - a2 * c1
                x1 = limpiar(Dx1 / Det)
                x2 = limpiar(Dx2 / Det)
                puntos.append((x1, x2))
    return puntos

def factible(puntos, restricciones):
    x1 , x2 = puntos
    for a, b, c in restricciones:
        if a*x1 + b*x2 > c:
            return False
    return True

def filtrar(puntos, restricciones):
	p_factibles = []
	for punto in puntos:
		if factible(punto, restricciones):
			p_factibles.append(punto)
	return p_factibles

def limpiar(n):
    return 0 if abs(n) < 1e-9 else n

def funcion_objetivo(puntos, fo, v):
    vec = None
    val = None
    for x1, x2 in puntos:
        z = fo[0] * x1 + fo[1] * x2
        if vec is None:
            vec = (x1, x2)
            val = z
        else:
            if v == "max" and z > val:
                vec = (x1, x2)
                val = z
            elif v == "min" and z < val:
                vec = (x1, x2)
                val = z
    return vec, val

def ordenar_puntos(puntos):
    centro = np.mean(puntos, axis=0)
    return sorted(puntos, key=lambda p: np.arctan2(p[1]-centro[1], p[0]-centro[0]))

def graficar(m, puntos_factibles, optimo, fo):
    plt.figure(figsize=(8,6))
    xs = [p[0] for p in puntos_factibles]
    ys = [p[1] for p in puntos_factibles]
    x_max = max(xs) + 2
    y_max = max(ys) + 2
    x = np.linspace(0, x_max, 400)

    for i, (a, b, c) in enumerate(m):
        if (a == -1 and b == 0) or (a == 0 and b == -1):
            continue
        if b != 0:
            y = (c - a*x) / b
            plt.plot(x, y, linestyle='--', label=f"R{i+1}")
        else:
            if a != 0:
                plt.axvline(x=c/a, linestyle='--', label=f"R{i+1}")

    plt.axhline(0, linewidth=2)
    plt.axvline(0, linewidth=2)
    
    if puntos_factibles:
        puntos_ordenados = ordenar_puntos(puntos_factibles)
        px = [p[0] for p in puntos_ordenados]
        py = [p[1] for p in puntos_ordenados]
        plt.fill(px, py, alpha=0.3)

    for px, py in puntos_factibles:
        z = fo[0]*px + fo[1]*py
        plt.scatter(px, py)
        plt.text(px+0.1, py+0.1, f"({px:.1f},{py:.1f})")

    if optimo:
        (x_opt, y_opt), z_opt = optimo
        plt.scatter(x_opt, y_opt, marker='X', s=150, label="Óptimo")
        plt.text(x_opt+0.2, y_opt+0.2, f"Óptimo\nZ={z_opt:.1f}")
        x_line = np.linspace(0, x_max, 200)
        y_line = (z_opt - fo[0]*x_line) / fo[1]
        plt.plot(x_line, y_line, label="Función objetivo")

    plt.xlim(-10, 110)
    plt.ylim(-10, 110)
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title("Método Gráfico - Programación Lineal")
    plt.grid()
    plt.legend()
    plt.show()

puntos = intersecciones(m)
puntos = list(set(puntos))
puntos = filtrar(puntos, m)

optimo = funcion_objetivo(puntos, fo, v)

print("Óptimo:", optimo)

graficar(m, puntos, optimo, fo)