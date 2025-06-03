import math
from scipy.stats import chi2  # Importamos la función para obtener el valor crítico de chi-cuadrado

def metodo_congruencial_aditivo():
    print("=== MÉTODO CONGRUENCIAL ADITIVO ===")

    # Ingreso de datos por parte del usuario
    m = int(input("Ingrese el módulo (m): "))  # Módulo m
    k = int(input("Ingrese cuántas semillas iniciales desea usar (k): "))  # Número de semillas k

    # Carga de las k semillas iniciales
    semillas = []
    for i in range(k):
        valor = int(input(f"Ingrese semilla X{i}: "))  # Cada semilla se pide por separado
        semillas.append(valor)

    n = int(input("Ingrese cuántos números pseudoaleatorios desea generar: "))  # Cantidad de números a generar

    # Copiamos las semillas y preparamos lista para los números normalizados
    numeros = semillas.copy()
    normalizados = []

    print("\n🔁 Paso a paso de cada iteración:")
    for i in range(n):
        x_1 = numeros[-1]          # Último número generado
        x_k = numeros[-k]          # Número que está k posiciones atrás
        nuevo = (x_1 + x_k) % m    # Fórmula del método aditivo
        numeros.append(nuevo)      # Agregamos el nuevo número a la lista
        u = nuevo / m              # Normalizamos dividiendo por m
        normalizados.append(u)     # Guardamos el número normalizado

        # Mostramos la información de la iteración actual
        print(f"\nIteración {i+1}:")
        print(f"  Último valor (X{i + k - 1})      = {x_1}")
        print(f"  Valor hace k posiciones (X{i})   = {x_k}")
        print(f"  Nuevo valor (X{i + k})           = ({x_1} + {x_k}) mod {m} = {nuevo}")
        print(f"  Normalizado (U{i + k})           = {u:.4f}")

    # Mostramos los valores normalizados generados
    print("\n📈 Valores normalizados:")
    for i, u in enumerate(normalizados):
        print(f"  U{i + k} = {u:.4f}")

    # PRUEBA DE CHI-CUADRADO
    n_total = len(normalizados)                    # Total de valores normalizados
    k_inter = math.ceil(math.log2(n_total) + 1)    # Cantidad de intervalos según regla de Sturges
    fe = n_total / k_inter                         # Frecuencia esperada
    intervalos = [0] * k_inter                     # Inicializamos los contadores por intervalo

    # Contamos cuántos valores caen en cada intervalo
    for valor in normalizados:
        indice = min(int(valor * k_inter), k_inter - 1)  # Asegura que no supere el último índice
        intervalos[indice] += 1

    # Calculamos el estadístico de Chi-Cuadrado
    chi_cuadrado = sum((fo - fe) ** 2 / fe for fo in intervalos)

    print("\n📊 Prueba de Chi-Cuadrado:")
    for i in range(k_inter):
        print(f"  Intervalo {i+1}: Observado = {intervalos[i]}, Esperado = {fe:.2f}")

    print(f"\nEstadístico Chi-Cuadrado = {chi_cuadrado:.4f}")
    alfa = 0.05                           # Nivel de significancia
    gl = k_inter - 1                      # Grados de libertad
    valor_critico = chi2.ppf(1 - alfa, gl)  # Valor crítico de la tabla de chi-cuadrado
    print(f"Valor crítico (α = {alfa}, gl = {gl}) = {valor_critico:.4f}")

    # Evaluamos si el estadístico cae dentro del rango aceptable
    if chi_cuadrado < valor_critico:
        print("✅ Los números PASAN la prueba de Chi-Cuadrado (uniformes).")
    else:
        print("❌ Los números NO pasan la prueba de Chi-Cuadrado (no uniformes).")

# Ejecutar el generador
metodo_congruencial_aditivo()

