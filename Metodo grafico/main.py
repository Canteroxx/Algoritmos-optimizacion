import matplotlib.pyplot as plt
import numpy as np

m = [[2,1,100],
	 [1,3,80],
     [1,0,45],
     [0,1,100],
     [-1,0,0],
	 [0,-1,0]]
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
    no_factibles = []
    for punto in puntos:
        if factible(punto, restricciones):
            p_factibles.append(punto)
        else:
            no_factibles.append(punto)
    return p_factibles, no_factibles

def limpiar(n):
    return 0 if abs(n) < 1e-9 else n

def funcion_objetivo(puntos, fo, v):
    x = puntos[0]
    ecuacion = fo[0]*x[0] + fo[1]*x[1]
    for x1, x2 in puntos:
        z = fo[0]*x1 + fo[1]*x2
        if v == "max" and z > ecuacion:
            x = (x1, x2)
            ecuacion = z
        elif v == "min" and z < ecuacion:
            x = (x1, x2)
            ecuacion = z
    return x, ecuacion

def ordenar_puntos(puntos):
    centro = np.mean(puntos, axis=0)
    return sorted(puntos, key=lambda p: np.arctan2(p[1]-centro[1], p[0]-centro[0]))

def graficar(m, puntos_factibles, no_factibles, optimo, fo):
    plt.figure(figsize=(8,6))

    if puntos_factibles:
        xs = [p[0] for p in puntos_factibles]
        ys = [p[1] for p in puntos_factibles]

        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)
        xmin, ymin = min(xmin, 0), min(ymin, 0)

        rango_x = xmax - xmin
        rango_y = ymax - ymin

        if rango_x == 0: rango_x = 10
        if rango_y == 0: rango_y = 10

        margen_x = rango_x * 0.2
        margen_y = rango_y * 0.2

        x_min, x_max = xmin - margen_x, xmax + margen_x
        y_min, y_max = ymin - margen_y, ymax + margen_y
    else:
        x_min, x_max = -10, 10
        y_min, y_max = -10, 10

    x = np.linspace(x_min, x_max, 800)
    
    colores = plt.cm.tab10.colors

    for i, (a, b, c) in enumerate(m):
        if (a == -1 and b == 0) or (a == 0 and b == -1):
            continue

        color = colores[i % len(colores)]
        if b != 0:
            y = (c - a*x) / b
            plt.plot(x, y, linestyle='--', color=color, label=f"R{i+1} {a}x1 + {b}x2 ≤ {c}")

        elif a != 0:
            plt.axvline(x=c/a, linestyle='--', color=color, label=f"R{i+1} {a}x1 + {b}x2 ≤ {c}")

    plt.axhline(0, linewidth=2, color='black')
    plt.axvline(0, linewidth=2, color='black')

    if puntos_factibles:
        puntos_ordenados = ordenar_puntos(puntos_factibles)
        px = [p[0] for p in puntos_ordenados]
        py = [p[1] for p in puntos_ordenados]
        plt.fill(px, py, alpha=0.3, color='green')

    for px, py in puntos_factibles:
        plt.scatter(px, py, color='green', marker='o')
        plt.text(px+0.3, py+0.3, f"({px:.1f},{py:.1f})")

    for px, py in no_factibles:
        plt.scatter(px, py, color='red', marker='x')
        plt.text(px+0.3, py+0.3, f"({px:.1f},{py:.1f})")

    if optimo:
        (x_opt, y_opt), z_opt = optimo
        plt.scatter(x_opt, y_opt, marker='X', s=150, label="Óptimo", color='green')
        plt.text(x_opt+0.3, y_opt+0.3, f"Óptimo\nZ={z_opt:.1f}")

        x_line = np.linspace(x_min, x_max, 400)
        y_line = (z_opt - fo[0]*x_line) / fo[1]
        plt.plot(x_line, y_line, label="Función objetivo", color='green')

    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title("Método Gráfico - Programación Lineal")
    plt.grid()
    plt.legend(loc='upper right', bbox_to_anchor=(1, 1))

    plt.show()

puntos = intersecciones(m)
puntos = list(set(puntos))
factibles, no_factibles = filtrar(puntos, m)

optimo = funcion_objetivo(factibles, fo, v)
graficar(m, factibles, no_factibles, optimo, fo)