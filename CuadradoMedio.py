import math
from scipy.stats import chi2  # Para obtener el valor crítico de la distribución chi-cuadrado

# Método del Cuadrado Medio
def middle_square(seed, iterations):
    seed_str = str(seed)
    digits = len(seed_str)  # Número de dígitos de la semilla

    # Se recomienda usar una semilla con cantidad par de dígitos
    if digits % 2 != 0:
        print("⚠️ Advertencia: es mejor usar una semilla con cantidad PAR de dígitos.")

    results = []         # Lista para almacenar los números generados
    current = seed       # Semilla actual

    for i in range(iterations):
        squared = current ** 2  # Eleva la semilla al cuadrado
        squared_str = str(squared).zfill(2 * digits)  # Rellena con ceros a la izquierda para mantener longitud

        # Extrae los dígitos centrales del número al cuadrado
        start = (len(squared_str) - digits) // 2
        middle = squared_str[start:start + digits]
        next_seed = int(middle)  # Nueva semilla extraída del medio

        # Muestra los pasos de la iteración actual
        print(f"\nIteración {i+1}:")
        print(f"  Semilla actual       : {current}")
        print(f"  Cuadrado             : {current}^2 = {squared}")
        print(f"  Cuadrado con ceros   : {squared_str}")
        print(f"  Dígitos del medio    : {middle}")
        print(f"  Nueva semilla        : {next_seed}")

        results.append(next_seed)  # Guarda el número generado
        current = next_seed        # Actualiza la semilla para la próxima iteración

    return results  # Devuelve la lista de números generados

# Función para normalizar los valores entre 0 y 1
def normalizar(valores, maximo):
    normalizados = [x / maximo for x in valores]  # Divide cada valor por el máximo posible

    print("\n📈 Valores normalizados:")
    for i, u in enumerate(normalizados):
        print(f"  U{i+1} = {u:.4f}")  # Muestra los valores normalizados con 4 decimales

    return normalizados  # Devuelve la lista normalizada

# Función para realizar la prueba de Chi-Cuadrado
def prueba_chi_cuadrado(valores_normalizados):
    n = len(valores_normalizados)              # Cantidad total de valores
    k = math.ceil(math.log2(n) + 1)            # Número de intervalos según la regla de Sturges
    fe = n / k                                 # Frecuencia esperada en cada intervalo
    intervalos = [0] * k                       # Inicializa los contadores por intervalo

    # Contabiliza cuántos valores caen en cada intervalo
    for valor in valores_normalizados:
        indice = min(int(valor * k), k - 1)    # Determina el intervalo del valor
        intervalos[indice] += 1

    # Calcula el estadístico de Chi-Cuadrado
    chi_cuadrado = sum((fo - fe) ** 2 / fe for fo in intervalos)

    # Muestra la tabla de frecuencias observadas y esperadas
    print("\n📊 Prueba de Chi-Cuadrado:")
    for i in range(k):
        print(f"  Intervalo {i+1}: Observado = {intervalos[i]}, Esperado = {fe:.2f}")

    print(f"\nEstadístico Chi-Cuadrado = {chi_cuadrado:.4f}")
    return chi_cuadrado, k  # Devuelve el estadístico y la cantidad de intervalos

# Bloque principal de ejecución
try:
    # Solicita al usuario los datos de entrada
    seed = int(input("Ingrese la semilla (ej: 123456 o 12345678): "))
    iterations = int(input("Cantidad de iteraciones a generar: "))

    # Genera los números pseudoaleatorios usando el método del cuadrado medio
    numeros = middle_square(seed, iterations)

    # Define el valor máximo posible según la cantidad de dígitos de la semilla
    maximo = 10 ** len(str(seed))

    # Normaliza los números generados entre 0 y 1
    normalizados = normalizar(numeros, maximo)

    # Realiza la prueba de Chi-Cuadrado
    chi, k = prueba_chi_cuadrado(normalizados)

    # Define el nivel de significancia (alfa) y obtiene el valor crítico
    alfa = 0.05
    valor_critico = chi2.ppf(1 - alfa, k - 1)
    print(f"\nValor crítico (α = {alfa}, gl = {k-1}) = {valor_critico:.4f}")

    # Compara el valor calculado con el valor crítico para decidir si pasa la prueba
    if chi < valor_critico:
        print("✅ Los números PASAN la prueba de Chi-Cuadrado.")
    else:
        print("❌ Los números NO pasan la prueba de Chi-Cuadrado.")

# Control de errores si el usuario no ingresa números enteros
except ValueError:
    print("❌ Error: Ingrese solo números enteros válidos.")
