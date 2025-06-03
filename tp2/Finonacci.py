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

        # Muestra paso a paso la generación del número y su normalización
        print(f"Iteración {i}: ({resultados[-2]} + {resultados[-3]}) = {suma} -> {suma} mod {m} = {xn} -> normalizado = {xn/m:.4f}")

    return resultados, normalizados  # Devuelve ambos: enteros generados y sus versiones normalizadas

# Prueba de Chi-Cuadrado para verificar uniformidad
def prueba_chi_cuadrado(valores_normalizados, k=10):
    n = len(valores_normalizados)        # Número total de valores
    fe = n / k                           # Frecuencia esperada por intervalo
    intervalos = [0] * k                 # Contador de frecuencias observadas

    # Contar cuántos valores caen en cada intervalo
    for valor in valores_normalizados:
        indice = min(int(valor * k), k - 1)  # Determina en qué intervalo cae (evita índice fuera de rango)
        intervalos[indice] += 1

    # Cálculo del estadístico chi-cuadrado
    chi_cuadrado = sum((fo - fe) ** 2 / fe for fo in intervalos)

    # Mostrar tabla de frecuencias
    print("\n📊 Prueba de Chi-Cuadrado:")
    for i in range(k):
        print(f" Intervalo {i + 1}: Observado = {intervalos[i]}, Esperado = {fe}")

    print(f"\nEstadístico Chi-Cuadrado = {chi_cuadrado:.4f}")
    return chi_cuadrado  # Devuelve el valor del estadístico

# Bloque principal de ejecución
try:
    # Solicita al usuario las semillas, módulo, iteraciones y cantidad de intervalos
    x0 = int(input("Ingrese la primera semilla (X0): "))
    x1 = int(input("Ingrese la segunda semilla (X1): "))
    m = int(input("Ingrese el valor del módulo (m): "))
    iteraciones = int(input("Ingrese la cantidad de iteraciones: "))
    k = int(input("Ingrese la cantidad de intervalos para Chi-Cuadrado (por ejemplo, 10): "))

    # Generación de números usando el método de Fibonacci modificado
    enteros, normalizados = fibonacci_mod_normalizado(x0, x1, m, iteraciones)

    # Mostrar los valores normalizados generados
    print("\n📈 Valores normalizados [0, 1):")
    for i, num in enumerate(normalizados):
        print(f"  U{i} = {num:.4f}")

    # Aplicar prueba de Chi-Cuadrado
    chi = prueba_chi_cuadrado(normalizados, k)

    # Comparación con el valor crítico
    alfa = 0.05
    valor_critico = chi2.ppf(1 - alfa, k - 1)  # Valor crítico para k-1 grados de libertad
    print(f"\nValor crítico (α = {alfa}, gl = {k-1}): {valor_critico:.4f}")

    # Evaluación del resultado
    if chi < valor_critico:
        print("✅ Los números pasan la prueba de Chi-Cuadrado (distribución uniforme).")
    else:
        print("❌ Los números NO pasan la prueba de Chi-Cuadrado.")

# Captura de errores si se ingresan datos inválidos
except ValueError:
    print("❌ Error: Ingrese solo valores numéricos válidos.")
