def fibonacci_mod_normalizado(x0, x1, m, iteraciones):
    resultados = [x0, x1]
    normalizados = [x0 / m, x1 / m]

    print(f"\n📌 Semillas iniciales: X0 = {x0}, X1 = {x1}")
    print(f"🔄 Módulo (m): {m}\n")

    for i in range(2, iteraciones):
        suma = resultados[-1] + resultados[-2]
        xn = suma % m
        resultados.append(xn)
        normalizados.append(xn / m)
        print(f"Iteración {i}: ({resultados[-2]} + {resultados[-3]}) = {suma} -> {suma} mod {m} = {xn} -> normalizado = {xn/m:.4f}")

    return resultados, normalizados

def prueba_chi_cuadrado(valores_normalizados, k=10):
    from math import pow
    n = len(valores_normalizados)
    fe = n / k
    intervalos = [0] * k

    # Contar cuántos valores caen en cada intervalo
    for valor in valores_normalizados:
        indice = min(int(valor * k), k - 1)  # Evitar índice fuera de rango
        intervalos[indice] += 1

    chi_cuadrado = sum((fo - fe) ** 2 / fe for fo in intervalos)

    print("\n📊 Prueba de Chi-Cuadrado:")
    for i in range(k):
        print(f" Intervalo {i + 1}: Observado = {intervalos[i]}, Esperado = {fe}")

    print(f"\nEstadístico Chi-Cuadrado = {chi_cuadrado:.4f}")
    return chi_cuadrado

# Entrada por consola
try:
    x0 = int(input("Ingrese la primera semilla (X0): "))
    x1 = int(input("Ingrese la segunda semilla (X1): "))
    m = int(input("Ingrese el valor del módulo (m): "))
    iteraciones = int(input("Ingrese la cantidad de iteraciones: "))
    k = int(input("Ingrese la cantidad de intervalos para Chi-Cuadrado (por ejemplo, 10): "))

    enteros, normalizados = fibonacci_mod_normalizado(x0, x1, m, iteraciones)

    print("\n📈 Valores normalizados [0, 1):")
    for i, num in enumerate(normalizados):
        print(f"  U{i} = {num:.4f}")

    chi = prueba_chi_cuadrado(normalizados, k)

    # Opcional: comparación con valor crítico (por ejemplo, 16.92 para k=10, alfa=0.05)
    from scipy.stats import chi2
    alfa = 0.05
    valor_critico = chi2.ppf(1 - alfa, k - 1)
    print(f"\nValor crítico (α = {alfa}, gl = {k-1}): {valor_critico:.4f}")

    if chi < valor_critico:
        print("✅ Los números pasan la prueba de Chi-Cuadrado (distribución uniforme).")
    else:
        print("❌ Los números NO pasan la prueba de Chi-Cuadrado.")

except ValueError:
    print("❌ Error: Ingrese solo valores numéricos válidos.")
