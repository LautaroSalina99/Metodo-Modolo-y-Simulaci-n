import numpy as np
from scipy.stats import chisquare

"""
Módulo de generadores de números pseudoaleatorios y simulación de atención de clientes.
Contiene métodos: cuadrados_medios, fibonacci_mod, congruencia_aditiva_correcta,
congruencia_multiplicativa, congruencia_mixta, test_chi_cuadrado y simular_atencion.
"""

# Generador de numeros aleatorios

def cuadrados_medios(seed, n, d=4):
    """
    Genera 'n' números en [0,1) usando el método de los cuadrados medios.

    Args:
        seed (int): Semilla inicial.
        n (int): Cantidad de números a generar.
        d (int): Número de dígitos que se extraen del cuadrado.
    Returns:
        List[float]: Lista de 'n' valores normalizados entre 0 y 1.
    """
    nums = []
    x = seed
    for _ in range(n):
        # Eleva al cuadrado y rellena con ceros para asegurar longitud 2*d
        x2 = str(x ** 2).zfill(2 * d)
        # Extrae los dígitos centrales
        medio = x2[len(x2)//2 - d//2 : len(x2)//2 + d//2]
        x = int(medio)
        # Normaliza dividiendo por 10^d
        nums.append(x / (10**d))
    return nums


def fibonacci_mod(seed1, seed2, m, n):
    """
    Generador basado en la sucesión de Fibonacci módulo m.

    Args:
        seed1 (int): Primer valor semilla.
        seed2 (int): Segundo valor semilla.
        m (int): Módulo para la operación.
        n (int): Número de valores a producir.
    Returns:
        List[float]: Sucesión normalizada dividiendo cada valor por m.
    """
    nums = [seed1, seed2]
    # Genera hasta alcanzar n elementos usando la suma de los dos previos modulo m
    while len(nums) < n:
        nums.append((nums[-1] + nums[-2]) % m)
    # Normaliza los valores
    return [x / m for x in nums]


def congruencia_aditiva_correcta(lista_semillas, m, j, k, n):
    """
    Genera números usando el método de congruencia aditiva:
    X_i = (X_{i-j} + X_{i-k}) mod m.

    Args:
        lista_semillas (List[int]): Semillas iniciales de longitud al menos j.
        m (int): Módulo.
        j (int): Retardo mayor.
        k (int): Retardo menor.
        n (int): Cantidad de números a generar.
    Returns:
        List[float]: Secuencia normalizada.
    Raises:
        ValueError: Si no hay suficientes semillas.
    """
    if len(lista_semillas) < j:
        raise ValueError(f"Se requieren al menos {j} semillas iniciales.")
    seq = lista_semillas.copy()
    # Calcula nuevo valor usando los dos retardos definidos
    for i in range(n - len(seq)):
        nuevo = (seq[-j] + seq[-k]) % m
        seq.append(nuevo)
    return [x / m for x in seq[:n]]


def congruencia_multiplicativa(a, m, seed, n):
    """
    Genera números con congruencia multiplicativa:
    X_{i+1} = (a * X_i) mod m.

    Args:
        a (int): Multiplicador.
        m (int): Módulo.
        seed (int): Semilla inicial.
        n (int): Cantidad de números.
    Returns:
        List[float]: Lista de valores en [0,1).
    """
    nums = []
    x = seed
    for _ in range(n):
        x = (a * x) % m
        nums.append(x / m)
    return nums


def congruencia_mixta(a, c, m, seed, n):
    """
    Genera números con congrencia mixta (lineal):
    X_{i+1} = (a * X_i + c) mod m.

    Args:
        a (int): Multiplicador.
        c (int): Incremento.
        m (int): Módulo.
        seed (int): Semilla.
        n (int): Cantidad de valores.
    Returns:
        List[float]: Valores normalizados.
    """
    x = seed
    nums = []
    for _ in range(n):
        x = (a * x + c) % m
        nums.append(x / m)
    return nums

# Chi-Cuadrado

def test_chi_cuadrado(numeros, k):
    """
    Realiza la prueba de bondad de ajuste Chi-cuadrado para distribución uniforme.

    Args:
        numeros (List[float]): Datos en [0,1).
        k (int): Cantidad de intervalos.
    Returns:
        chi2_stat (float), p_value (float), gl (int), obs (ndarray)
    """
    n = len(numeros)
    # Calcula frecuencias observadas
    obs, _ = np.histogram(numeros, bins=k, range=(0, 1))
    # Frecuencias esperadas (uniforme)
    esp = [n/k] * k
    chi2_stat, p_value = chisquare(f_obs=obs, f_exp=esp)
    gl = k - 1
    return chi2_stat, p_value, gl, obs

# Simulación atencion al cliente

def simular_atencion(clientes, cajeros, barras, llegada_rng, caja_rng, barra_rng):
    """
    Simula tiempos de atención en caja y barra de un bar.

    Args:
        clientes (int): Número de clientes.
        cajeros (int): Cantidad de cajeros (no usado en esta versión simple).
        barras (int): Cantidad de barras (no usado aquí).
        llegada_rng, caja_rng, barra_rng (List[float]): Listas de tiempos aleatorios normalizados.
    Returns:
        List[str]: Mensajes con tiempos de llegada y servicio.
    """
    eventos = []
    for i in range(clientes):
        # Tiempo de llegada acumulado (multiplicado por 5 min)
        llegada = sum(llegada_rng[:i+1]) * 5
        tiempo_caja = caja_rng[i] * 4 + 1  # Servicio en caja entre 1 y 5
        tiempo_barra = barra_rng[i] * 5 + 1  # Servicio en barra entre 1 y 6
        eventos.append(
            f"Cliente {i+1}: Llegada {llegada:.2f} min, Caja {tiempo_caja:.2f} min, Barra {tiempo_barra:.2f} min"
        )
    return eventos

if __name__ == "__main__":
    # Menú de selección de método
    print("Seleccione el método para generar números aleatorios:")
    opciones = ["Cuadrados Medios", "Fibonacci", "Congruencia Aditiva",
                "Congruencia Multiplicativa", "Congruencia Mixta"]
    for idx, name in enumerate(opciones, 1):
        print(f"{idx} - {name}")

    opcion = input("Ingrese el número del método: ")
    try:
        metodo = opciones[int(opcion)-1]
    except Exception:
        metodo = opciones[0]  # Por defecto
    print(f"\nMétodo seleccionado: {metodo}")

    # Parámetros básicos
    n_clientes = 10
    k_intervalos = 10
    alpha = 0.05

    # Generación de números según método
    if metodo == "Cuadrados Medios":
        llegada_rng = cuadrados_medios(seed=731, n=n_clientes)
        caja_rng   = cuadrados_medios(seed=831, n=n_clientes)
        barra_rng  = cuadrados_medios(seed=931, n=n_clientes)
    elif metodo == "Fibonacci":
        llegada_rng = fibonacci_mod(5, 8, 100, n_clientes)
        caja_rng   = fibonacci_mod(15, 18, 100, n_clientes)
        barra_rng  = fibonacci_mod(25, 28, 100, n_clientes)
    elif metodo == "Congruencia Aditiva":
        semillas = [5, 8, 12, 3, 7]
        llegada_rng = congruencia_aditiva_correcta(semillas,    100, 5, 3, n_clientes)
        caja_rng    = congruencia_aditiva_correcta([x+5 for x in semillas], 105, 5, 3, n_clientes)
        barra_rng   = congruencia_aditiva_correcta([x+10 for x in semillas],110, 5, 3, n_clientes)
    elif metodo == "Congruencia Multiplicativa":
        llegada_rng = congruencia_multiplicativa(17, 100, 13, n_clientes)
        caja_rng    = congruencia_multiplicativa(18, 100, 14, n_clientes)
        barra_rng   = congruencia_multiplicativa(19, 100, 15, n_clientes)
    else:
        llegada_rng = congruencia_mixta(17, 43, 100, 13, n_clientes)
        caja_rng    = congruencia_mixta(18, 44, 100, 14, n_clientes)
        barra_rng   = congruencia_mixta(19, 45, 100, 15, n_clientes)

    # Simulación y resultados
    eventos = simular_atencion(n_clientes, 2, 2, llegada_rng, caja_rng, barra_rng)
    print("\n -Simulación de Atención a Clientes- ")
    for e in eventos:
        print(e)

    # Prueba Chi-cuadrado para uniformidad de llegadas
    chi2, p_valor, gl, observados = test_chi_cuadrado(llegada_rng, k_intervalos)
    print("\n -Test Chi-cuadrado- ")
    print(f"Chi² = {chi2:.4f}")
    print(f"p-valor = {p_valor:.4f}")
    print(f"Grados de libertad = {gl}")
    print("Frecuencias observadas por intervalo:", observados)
    print("Distribución uniforme" + (" aceptada" if p_valor > alpha else " rechazada"))