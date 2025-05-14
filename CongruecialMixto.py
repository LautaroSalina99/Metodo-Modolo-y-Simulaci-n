import math
from scipy.stats import chi2

def metodo_congruencial_mixto(semilla, a, c, m, cantidad):
    numeros = []
    x = semilla
    print("\n📘 Detalles de cada iteración:")
    for i in range(cantidad):
        x = (a * x + c) % m
        r = x / m  # Normalizado entre 0 y 1
        numeros.append(r)

        # Mostrar paso a paso
        print(f"\nIteración {i+1}:")
        print(f"  x{i} = ({a} * {semilla} + {c}) mod {m} = {x}")
        print(f"  r{i+1} = {x} / {m} = {r:.4f}")

        semilla = x  # Actualizar semilla para la próxima iteración

    return numeros

def prueba_chi_cuadrado(valores_normalizados):
    n = len(valores_normalizados)
    k = math.ceil(math.log2(n) + 1)  # Regla de Sturges
    fe = n / k
    intervalos = [0] * k

    for valor in valores_normalizados:
        indice = min(int(valor * k), k - 1)
        intervalos[indice] += 1

    chi_cuadrado = sum((fo - fe) ** 2 / fe for fo in intervalos)

    print("\n📊 Prueba de Chi-Cuadrado:")
    for i in range(k):
        print(f"  Intervalo {i+1}: Observado = {intervalos[i]}, Esperado = {fe:.2f}")

    print(f"\nEstadístico Chi-Cuadrado = {chi_cuadrado:.4f}")
    return chi_cuadrado, k

# Cargar datos desde consola
print("🧮 Método Congruencial Mixto")
try:
    semilla = int(input("Ingrese la semilla (X0): "))
    a = int(input("Ingrese el multiplicador (a): "))
    c = int(input("Ingrese la constante aditiva (c): "))
    m = int(input("Ingrese el módulo (m): "))
    cantidad = int(input("¿Cuántos números aleatorios desea generar?: "))

    # Generar los números
    resultado = metodo_congruencial_mixto(semilla, a, c, m, cantidad)

    # Mostrar resultados finales
    print("\n🎲 Números pseudoaleatorios generados:")
    for i, num in enumerate(resultado, 1):
        print(f"  R{i} = {num:.4f}")

    # Prueba de Chi-Cuadrado
    chi, k = prueba_chi_cuadrado(resultado)
    alfa = 0.05
    valor_critico = chi2.ppf(1 - alfa, k - 1)
    print(f"\nValor crítico (α = {alfa}, gl = {k-1}) = {valor_critico:.4f}")

    if chi < valor_critico:
        print("✅ Los números PASAN la prueba de Chi-Cuadrado.")
    else:
        print("❌ Los números NO pasan la prueba de Chi-Cuadrado.")

except ValueError:
    print("❌ Error: Ingrese solo valores numéricos enteros.")
