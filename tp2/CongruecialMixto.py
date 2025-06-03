import math  # Importa funciones matemáticas como logaritmos y redondeo
from scipy.stats import chi2  # Importa la distribución chi-cuadrado para obtener valores críticos

# Función que implementa el Método Congruencial Mixto
def metodo_congruencial_mixto(semilla, a, c, m, cantidad):
    numeros = []  # Lista para almacenar los números normalizados
    x = semilla  # Se inicializa con la semilla ingresada

    print("\n📘 Detalles de cada iteración:")
    for i in range(cantidad):  # Repite 'cantidad' veces
        x = (a * x + c) % m  # Fórmula del método congruencial mixto: Xn+1 = (aXn + c) mod m
        r = x / m  # Se normaliza el valor a un número entre 0 y 1
        numeros.append(r)  # Se guarda el número generado

        # Mostrar paso a paso cómo se generó cada número
        print(f"\nIteración {i+1}:")
        print(f"  x{i} = ({a} * {semilla} + {c}) mod {m} = {x}")
        print(f"  r{i+1} = {x} / {m} = {r:.4f}")

        semilla = x  # Actualiza la semilla para usarla en la siguiente iteración

    return numeros  # Retorna la lista de números generados

# Función para realizar la prueba de Chi-Cuadrado
def prueba_chi_cuadrado(valores_normalizados):
    n = len(valores_normalizados)  # Cantidad de números generados
    k = math.ceil(math.log2(n) + 1)  # Cantidad de intervalos según la regla de Sturges
    fe = n / k  # Frecuencia esperada en cada intervalo
    intervalos = [0] * k  # Lista con k intervalos inicializados en 0

    for valor in valores_normalizados:
        indice = min(int(valor * k), k - 1)  # Determina en qué intervalo cae el valor
        intervalos[indice] += 1  # Incrementa la frecuencia observada en ese intervalo

    # Calcula el estadístico de chi-cuadrado: ∑((fo - fe)^2 / fe)
    chi_cuadrado = sum((fo - fe) ** 2 / fe for fo in intervalos)

    print("\n📊 Prueba de Chi-Cuadrado:")
    for i in range(k):
        print(f"  Intervalo {i+1}: Observado = {intervalos[i]}, Esperado = {fe:.2f}")

    print(f"\nEstadístico Chi-Cuadrado = {chi_cuadrado:.4f}")
    return chi_cuadrado, k  # Retorna el estadístico y la cantidad de intervalos

# Inicio del programa principal
print("🧮 Método Congruencial Mixto")
try:
    # Solicita al usuario los parámetros necesarios
    semilla = int(input("Ingrese la semilla (X0): "))
    a = int(input("Ingrese el multiplicador (a): "))
    c = int(input("Ingrese la constante aditiva (c): "))
    m = int(input("Ingrese el módulo (m): "))
    cantidad = int(input("¿Cuántos números aleatorios desea generar?: "))

    # Llama a la función generadora
    resultado = metodo_congruencial_mixto(semilla, a, c, m, cantidad)

    # Muestra los números generados
    print("\n🎲 Números pseudoaleatorios generados:")
    for i, num in enumerate(resultado, 1):
        print(f"  R{i} = {num:.4f}")

    # Llama a la función para hacer la prueba de chi-cuadrado
    chi, k = prueba_chi_cuadrado(resultado)
    alfa = 0.05  # Nivel de significancia
    valor_critico = chi2.ppf(1 - alfa, k - 1)  # Calcula el valor crítico con scipy

    print(f"\nValor crítico (α = {alfa}, gl = {k-1}) = {valor_critico:.4f}")

    # Compara el estadístico con el valor crítico
    if chi < valor_critico:
        print("✅ Los números PASAN la prueba de Chi-Cuadrado.")
    else:
        print("❌ Los números NO pasan la prueba de Chi-Cuadrado.")

except ValueError:
    # Si el usuario ingresa un dato no numérico
    print("❌ Error: Ingrese solo valores numéricos enteros.")

