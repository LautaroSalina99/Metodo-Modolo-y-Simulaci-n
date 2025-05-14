import numpy as np
from scipy.stats import chisquare

# ====================== GENERADORES DE NÚMEROS ALEATORIOS ======================

def cuadrados_medios(seed, n, d=4):
    nums = []
    x = seed
    for _ in range(n):
        x2 = str(x ** 2).zfill(2 * d)
        medio = x2[len(x2)//2 - d//2 : len(x2)//2 + d//2]
        x = int(medio)
        nums.append(x / (10**d))
    return nums

def fibonacci_mod(seed1, seed2, m, n):
    nums = [seed1, seed2]
    while len(nums) < n:
        nums.append((nums[-1] + nums[-2]) % m)
    return [x / m for x in nums]

def congruencia_aditiva_correcta(lista_semillas, m, j, k, n):
    if len(lista_semillas) < j:
        raise ValueError(f"Se requieren al menos {j} semillas iniciales.")
    seq = lista_semillas.copy()
    for i in range(n - len(seq)):
        nuevo = (seq[-j] + seq[-k]) % m
        seq.append(nuevo)
    return [x / m for x in seq[:n]]

def congruencia_multiplicativa(a, m, seed, n):
    nums = []
    x = seed
    for _ in range(n):
        x = (a * x) % m
        nums.append(x / m)
    return nums

def congruencia_mixta(a, c, m, seed, n):
    x = seed
    nums = []
    for _ in range(n):
        x = (a * x + c) % m
        nums.append(x / m)
    return nums

# ====================== CHI-CUADRADO ======================

def test_chi_cuadrado(numeros, k):
    n = len(numeros)
    obs, _ = np.histogram(numeros, bins=k, range=(0, 1))
    esp = [n/k] * k
    chi2_stat, p_value = chisquare(f_obs=obs, f_exp=esp)
    gl = k - 1
    return chi2_stat, p_value, gl, obs

# ====================== SIMULACIÓN ATENCIÓN CLIENTES ======================

def simular_atencion(clientes, cajeros, barras, llegada_rng, caja_rng, barra_rng):
    eventos = []
    for i in range(clientes):
        llegada = sum(llegada_rng[:i+1]) * 5
        tiempo_caja = caja_rng[i] * 4 + 1
        tiempo_barra = barra_rng[i] * 5 + 1
        eventos.append(f"Cliente {i+1}: Llegada {llegada:.2f} min, Caja {tiempo_caja:.2f} min, Barra {tiempo_barra:.2f} min")
    return eventos

# ====================== EJEMPLO DE USO ======================

if __name__ == "__main__":
    print("Seleccione el método para generar números aleatorios:")
    print("1 - Cuadrados Medios")
    print("2 - Fibonacci")
    print("3 - Congruencia Aditiva")
    print("4 - Congruencia Multiplicativa")
    print("5 - Congruencia Mixta")

    opcion = input("Ingrese el número del método: ")

    if opcion == "1":
        metodo = "Cuadrados Medios"
    elif opcion == "2":
        metodo = "Fibonacci"
    elif opcion == "3":
        metodo = "Congruencia Aditiva"
    elif opcion == "4":
        metodo = "Congruencia Multiplicativa"
    elif opcion == "5":
        metodo = "Congruencia Mixta"
    else:
        print("Opción inválida. Se usará 'Cuadrados Medios' por defecto.")
        metodo = "Cuadrados Medios"

    print(f"\nMétodo seleccionado: {metodo}")

    n_clientes = 10
    k_intervalos = 10
    alpha = 0.05

    # Generación de números aleatorios según el método
    if metodo == "Cuadrados Medios":
        llegada_rng = cuadrados_medios(seed=5731, n=n_clientes)
        caja_rng = cuadrados_medios(seed=5831, n=n_clientes)
        barra_rng = cuadrados_medios(seed=5931, n=n_clientes)
    elif metodo == "Fibonacci":
        llegada_rng = fibonacci_mod(5, 8, 100, n_clientes)
        caja_rng = fibonacci_mod(15, 18, 100, n_clientes)
        barra_rng = fibonacci_mod(25, 28, 100, n_clientes)
    elif metodo == "Congruencia Aditiva":
        semillas = [5, 8, 12, 3, 7]
        llegada_rng = congruencia_aditiva_correcta(semillas, 100, 5, 3, n_clientes)
        caja_rng = congruencia_aditiva_correcta([x+5 for x in semillas], 105, 5, 3, n_clientes)
        barra_rng = congruencia_aditiva_correcta([x+10 for x in semillas], 110, 5, 3, n_clientes)
    elif metodo == "Congruencia Multiplicativa":
        llegada_rng = congruencia_multiplicativa(17, 100, 13, n_clientes)
        caja_rng = congruencia_multiplicativa(18, 100, 14, n_clientes)
        barra_rng = congruencia_multiplicativa(19, 100, 15, n_clientes)
    elif metodo == "Congruencia Mixta":
        llegada_rng = congruencia_mixta(17, 43, 100, 13, n_clientes)
        caja_rng = congruencia_mixta(18, 44, 100, 14, n_clientes)
        barra_rng = congruencia_mixta(19, 45, 100, 15, n_clientes)

    # Simulación de atención
    eventos = simular_atencion(n_clientes, cajeros=2, barras=2, llegada_rng=llegada_rng, caja_rng=caja_rng, barra_rng=barra_rng)

    # Resultados de la simulación
    print("\n--- Simulación de Atención a Clientes ---")
    for e in eventos:
        print(e)

    # Test de Chi-cuadrado
    chi2, p_valor, gl, observados = test_chi_cuadrado(llegada_rng, k_intervalos)
    print("\n--- Test Chi-cuadrado ---")
    print(f"Chi² = {chi2:.4f}")
    print(f"p-valor = {p_valor:.4f}")
    print(f"Grados de libertad = {gl}")
    print("Frecuencias observadas por intervalo:", observados)
    print("Distribución uniforme" + (" aceptada" if p_valor > alpha else " rechazada"))

