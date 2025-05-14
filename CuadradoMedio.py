import math
from scipy.stats import chi2

def middle_square(seed, iterations):
    seed_str = str(seed)
    digits = len(seed_str)

    if digits % 2 != 0:
        print("⚠️ Advertencia: es mejor usar una semilla con cantidad PAR de dígitos.")

    results = []
    current = seed

    for i in range(iterations):
        squared = current ** 2
        squared_str = str(squared).zfill(2 * digits)  # Rellenar con ceros

        start = (len(squared_str) - digits) // 2
        middle = squared_str[start:start + digits]
        next_seed = int(middle)

        # Mostrar detalles de la iteración
        print(f"\nIteración {i+1}:")
        print(f"  Semilla actual       : {current}")
        print(f"  Cuadrado             : {current}^2 = {squared}")
        print(f"  Cuadrado con ceros   : {squared_str}")
        print(f"  Dígitos del medio    : {middle}")
        print(f"  Nueva semilla        : {next_seed}")

        results.append(next_seed)
        current = next_seed

    return results

def normalizar(valores, maximo):
    normalizados = [x / maximo for x in valores]
    print("\n📈 Valores normalizados:")
    for i, u in enumerate(normalizados):
        print(f"  U{i+1} = {u:.4f}")
    return normalizados

def prueba_chi_cuadrado(valores_normalizados):
    n = len(valores_normalizados)
    k = math.ceil(math.log2(n) + 1)  # Regla de Sturges
    fe = n / k
    intervalos = [0] * k

    # Contar cuántos valores caen en cada intervalo
    for valor in valores_normalizados:
        indice = min(int(valor * k), k - 1)  # Evita índice fuera de rango
        intervalos[indice] += 1

    chi_cuadrado = sum((fo - fe) ** 2 / fe for fo in intervalos)

    print("\n📊 Prueba de Chi-Cuadrado:")
    for i in range(k):
        print(f"  Intervalo {i+1}: Observado = {intervalos[i]}, Esperado = {fe:.2f}")

    print(f"\nEstadístico Chi-Cuadrado = {chi_cuadrado:.4f}")
    return chi_cuadrado, k

# Ingreso por consola
try:
    seed = int(input("Ingrese la semilla (ej: 123456 o 12345678): "))
    iterations = int(input("Cantidad de iteraciones a generar: "))

    numeros = middle_square(seed, iterations)
    maximo = 10 ** len(str(seed))  # Para normalizar según los dígitos
    normalizados = normalizar(numeros, maximo)

    chi, k = prueba_chi_cuadrado(normalizados)

    alfa = 0.05
    valor_critico = chi2.ppf(1 - alfa, k - 1)
    print(f"\nValor crítico (α = {alfa}, gl = {k-1}) = {valor_critico:.4f}")

    if chi < valor_critico:
        print("✅ Los números PASAN la prueba de Chi-Cuadrado.")
    else:
        print("❌ Los números NO pasan la prueba de Chi-Cuadrado.")

except ValueError:
    print("❌ Error: Ingrese solo números enteros válidos.")
