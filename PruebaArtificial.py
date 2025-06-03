import random

def normalizar(probabilidades):
    total = sum(probabilidades)
    return [p / total for p in probabilidades]

def generar_muestra():
    # Paso 1: Ingreso de datos
    valores_input = input("Ingrese los valores (separados por coma): ")
    probabilidades_input = input("Ingrese las probabilidades correspondientes (separadas por coma): ")
    
    # Paso 2: Procesamiento
    try:
        valores = [float(v.strip()) for v in valores_input.split(",")]
        probabilidades = [float(p.strip()) for p in probabilidades_input.split(",")]
    except ValueError:
        print("Error: asegúrese de ingresar solo números.")
        return

    if len(valores) != len(probabilidades):
        print("Error: la cantidad de valores debe coincidir con la de probabilidades.")
        return

    if sum(probabilidades) != 1.0:
        print("Advertencia: las probabilidades no suman 1. Se normalizarán.")
        probabilidades = normalizar(probabilidades)

    # Paso 3: Tamaño de la muestra
    try:
        tamaño_muestra = int(input("Ingrese el tamaño de la muestra a generar: "))
    except ValueError:
        print("Error: el tamaño de la muestra debe ser un número entero.")
        return

    # Paso 4: Generar muestra artificial
    muestra = random.choices(valores, weights=probabilidades, k=tamaño_muestra)

    # Paso 5: Mostrar resultados
    print("\nMuestra generada:")
    print(muestra)

if __name__ == "__main__":
    generar_muestra()

