import math
from scipy.stats import chi2

def metodo_congruencial_aditivo():
    print("=== MÉTODO CONGRUENCIAL ADITIVO ===")

    # Ingreso de datos
    m = int(input("Ingrese el módulo (m): "))
    k = int(input("Ingrese cuántas semillas iniciales desea usar (k): "))

    semillas = []
    for i in range(k):
        valor = int(input(f"Ingrese semilla X{i}: "))
        semillas.append(valor)

    n = int(input("Ingrese cuántos números pseudoaleatorios desea generar: "))

    # Generador
    numeros = semillas.copy()
    normalizados = []

    print("\n🔁 Paso a paso de cada iteración:")
    for i in range(n):
        x_1 = numeros[-1]
        x_k = numeros[-k]
        nuevo = (x_1 + x_k) % m
        numeros.append(nuevo)
        u = nuevo / m
        normalizados.append(u)

        print(f"\nIteración {i+1}:")
        print(f"  Último valor (X{i + k - 1})      = {x_1}")
        print(f"  Valor hace k posiciones (X{i})   = {x_k}")
        print(f"  Nuevo valor (X{i + k})           = ({x_1} + {x_k}) mod {m} = {nuevo}")
        print(f"  Normalizado (U{i + k})           = {u:.4f}")

    # Prueba de Chi-Cuadrado
    print("\n📈 Valores normalizados:")
    for i, u in enumerate(normalizados):
        print(f"  U{i + k} = {u:.4f}")

    n_total = len(normalizados)
    k_inter = math.ceil(math.log2(n_total) + 1)  # regla de Sturges
    fe = n_total / k_inter
    intervalos = [0] * k_inter

    for valor in normalizados:
        indice = min(int(valor * k_inter), k_inter - 1)
        intervalos[indice] += 1

    chi_cuadrado = sum((fo - fe) ** 2 / fe for fo in intervalos)

    print("\n📊 Prueba de Chi-Cuadrado:")
    for i in range(k_inter):
        print(f"  Intervalo {i+1}: Observado = {intervalos[i]}, Esperado = {fe:.2f}")

    print(f"\nEstadístico Chi-Cuadrado = {chi_cuadrado:.4f}")
    alfa = 0.05
    gl = k_inter - 1
    valor_critico = chi2.ppf(1 - alfa, gl)
    print(f"Valor crítico (α = {alfa}, gl = {gl}) = {valor_critico:.4f}")

    if chi_cuadrado < valor_critico:
        print("✅ Los números PASAN la prueba de Chi-Cuadrado (uniformes).")
    else:
        print("❌ Los números NO pasan la prueba de Chi-Cuadrado (no uniformes).")

# Ejecutar
metodo_congruencial_aditivo()
