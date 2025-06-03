def metodo_cuadrado_medio(semilla, cantidad):
    resultados = []
    actual = semilla
    for _ in range(cantidad):
        cuadrado = str(actual ** 2).zfill(8)  # Siempre 8 dígitos
        medio = int(cuadrado[2:6])  # Extrae los 4 dígitos del medio
        resultados.append(medio % 100)  # Escala a [0, 99]
        actual = medio
    return resultados

def construir_intervalos(valores, probabilidades):
    intervalos = []
    inicio = 0
    for p in probabilidades:
        fin = inicio + int(p * 100)
        intervalos.append((inicio, fin - 1))
        inicio = fin
    return intervalos

def obtener_valor_por_indice(indice, intervalos, valores):
    for i, (ini, fin) in enumerate(intervalos):
        if ini <= indice <= fin:
            return valores[i]
    return None

def generar_muestra_con_cuadrado_medio(valores, probabilidades, semilla, tamaño_muestra):
    intervalos = construir_intervalos(valores, probabilidades)
    indices = metodo_cuadrado_medio(semilla, tamaño_muestra)
    muestra = []
    print("\n🔢 Índice | Valor asignado | Intervalo")
    print("-" * 40)
    for num in indices:
        valor = obtener_valor_por_indice(num, intervalos, valores)
        intervalo_str = ""
        for (ini, fin), val in zip(intervalos, valores):
            if ini <= num <= fin:
                intervalo_str = f"[{ini}-{fin}] → {val}"
                break
        muestra.append(valor)
        print(f"{str(num).zfill(2)}     | {valor:<14} | {intervalo_str}")
    return muestra

# --- ENTRADA ---
n = int(input("¿Cuántos valores tendrá la tabla? "))

valores = []
probabilidades = []

print("Ingrese los valores y sus probabilidades (entre 0 y 1, deben sumar 1):")
for i in range(n):
    valor = float(input(f"Valor #{i+1}: "))
    prob = float(input(f"Probabilidad del valor {valor}: "))
    valores.append(valor)
    probabilidades.append(prob)

# Validación de la suma de probabilidades
if round(sum(probabilidades), 2) != 1.00:
    print("❌ Error: las probabilidades no suman 1.")
else:
    semilla = int(input("Ingrese una semilla de 4 dígitos (ej: 1234): "))
    tamaño_muestra = int(input("Ingrese el tamaño de la muestra a generar: "))
    muestra = generar_muestra_con_cuadrado_medio(valores, probabilidades, semilla, tamaño_muestra)

    print("\n📊 Muestra generada:")
    print(muestra)
