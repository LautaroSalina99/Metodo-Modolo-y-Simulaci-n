from math import pow
from scipy.stats import chi2  # Para obtener el valor crítico de chi-cuadrado

# Método de Fibonacci Modificado y Normalizado
def fibonacci_mod_normalizado(x0, x1, m, iteraciones):
    resultados = [x0, x1]                     # Lista con los dos primeros valores (semillas)
    normalizados = [x0 / m, x1 / m]           # Lista de valores normalizados entre 0 y 1

    print(f"\n📌 Semillas iniciales: X0 = {x0}, X1 = {x1}")
    print(f"🔄 Módulo (m): {m}\n")

    for i in range(2, iteraciones):
        suma = resultados[-1] + resultados[-2]       # Suma de los dos anteriores
        xn = suma % m                                # Se aplica el módulo
        resultados.append(xn)                        # Se agrega a la lista de enteros
        normalizados.append(xn / m)                  # Se normaliza y agrega a la lista

        print(f"Iteración {i}: ({resultados[-2]} + {resultados[-3]}) = {suma} -> {suma} mod {m} = {xn} -> normalizado = {xn/m:.4f}")

    return resultados, normalizados

# Prueba de Chi-Cuadrado
def prueba_chi_cuadrado(valores_normalizados, k=10):
    n = len(valores_normalizados)
    fe = n / k
    intervalos = [0] * k

    for valor in valores_normalizados:
        indice = min(int(valor * k), k - 1)
        intervalos[indice] += 1

    chi_cuadrado = sum((fo - fe) ** 2 / fe for fo in intervalos)

    print("\n📊 Prueba de Chi-Cuadrado:")
    for i in range(k):
        print(f" Intervalo {i + 1}: Observado = {intervalos[i]}, Esperado = {fe}")

    print(f"\nEstadístico Chi-Cuadrado = {chi_cuadrado:.4f}")
    return chi_cuadrado

# Bloque principal
try:
    # Entrada de datos
    x0 = int(input("Ingrese la primera semilla (X0): "))
    x1 = int(input("Ingrese la segunda semilla (X1): "))
    m = int(input("Ingrese el valor del módulo (m): "))
    iteraciones = int(input("Ingrese la cantidad de iteraciones: "))
    k = int(input("Ingrese la cantidad de intervalos para Chi-Cuadrado (por ejemplo, 10): "))
    
    # NUEVO: Solicitar el intervalo [a, b]
    a = float(input("Ingrese el límite inferior del intervalo (a): "))
    b = float(input("Ingrese el límite superior del intervalo (b): "))

    # Generar números
    enteros, normalizados = fibonacci_mod_normalizado(x0, x1, m, iteraciones)

    # Mostrar valores normalizados
    print("\n📈 Valores normalizados [0, 1):")
    for i, num in enumerate(normalizados):
        print(f"  U{i} = {num:.4f}")

    # NUEVO: Transformar a intervalo [a, b]
    print(f"\n🎯 Valores transformados al intervalo [{a}; {b}]:")
    transformados = []
    for i, u in enumerate(normalizados):
        x = a + u * (b - a)
        transformados.append(x)
        print(f"  X{i} = {x:.4f}")

    # Prueba de Chi-Cuadrado sobre los normalizados (no sobre los transformados)
    chi = prueba_chi_cuadrado(normalizados, k)

    alfa = 0.05
    valor_critico = chi2.ppf(1 - alfa, k - 1)
    print(f"\nValor crítico (α = {alfa}, gl = {k-1}): {valor_critico:.4f}")

    if chi < valor_critico:
        print("✅ Los números pasan la prueba de Chi-Cuadrado (distribución uniforme).")
    else:
        print("❌ Los números NO pasan la prueba de Chi-Cuadrado.")

except ValueError:
    print("❌ Error: Ingrese solo valores numéricos válidos.")
