import math
from scipy.stats import chi2

# Función para generar números pseudoaleatorios con el método congruencial multiplicativo
def metodo_congruencial_multiplicativo(semilla, a, m, cantidad):
    xi = semilla
    numeros = []

    print("\n🔁 Iteraciones del método congruencial multiplicativo:")
    for i in range(cantidad):
        producto = a * xi              # Se multiplica xi por el multiplicador a
        xi = producto % m              # Se aplica el módulo m
        ri = xi / m                    # Se normaliza a [0, 1)
        numeros.append(ri)            # Se guarda el número

        print(f"\nIteración {i+1}:")
        print(f"  xi anterior     = {xi}")
        print(f"  a * xi          = {a} * {xi} = {producto}")
        print(f"  xi mod m        = {producto} mod {m} = {xi}")
        print(f"  Número normalizado ri = {xi} / {m} = {ri:.4f}")

    return numeros

# Función para realizar la prueba de Chi-Cuadrado
def prueba_chi_cuadrado(valores_normalizados):
    n = len(valores_normalizados)
    k = math.ceil(math.log2(n) + 1)   # Regla de Sturges para determinar el número de intervalos
    fe = n / k                        # Frecuencia esperada por intervalo
    intervalos = [0] * k              # Contadores por intervalo

    for valor in valores_normalizados:
        indice = min(int(valor * k), k - 1)  # Asegura que 1.0 no desborde
        intervalos[indice] += 1

    chi_cuadrado = sum((fo - fe) ** 2 / fe for fo in intervalos)

    print("\n📊 Prueba de Chi-Cuadrado:")
    for i in range(k):
        print(f"  Intervalo {i+1}: Observado = {intervalos[i]}, Esperado = {fe:.2f}")

    print(f"\nEstadístico Chi-Cuadrado = {chi_cuadrado:.4f}")
    return chi_cuadrado, k

# Programa principal
print("🔢 Método Congruencial Multiplicativo")
try:
    semilla = int(input("Ingrese la semilla (X0): "))
    a = int(input("Ingrese el multiplicador (a): "))
    m = int(input("Ingrese el módulo (m): "))
    cantidad = int(input("Ingrese la cantidad de números a generar: "))

    # Generar los números
    resultado = metodo_congruencial_multiplicativo(semilla, a, m, cantidad)

    print("\n📈 Números normalizados generados:")
    for i, r in enumerate(resultado):
        print(f"  r{i+1} = {r:.4f}")

    # Validar con Chi-Cuadrado
    chi, k = prueba_chi_cuadrado(resultado)
    alfa = 0.05
    valor_critico = chi2.ppf(1 - alfa, k - 1)
    print(f"\nValor crítico (α = {alfa}, gl = {k-1}) = {valor_critico:.4f}")

    if chi < valor_critico:
        print("✅ Los números PASAN la prueba de Chi-Cuadrado.")
    else:
        print("❌ Los números NO pasan la prueba de Chi-Cuadrado.")

except ValueError:
    print("❌ Error: ingrese solo números enteros válidos.")
