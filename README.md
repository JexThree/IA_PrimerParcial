# Módulo de Grafos Dirigidos

Este proyecto implementa una estructura de datos basada en grafos dirigidos con restricciones estrictas de validación (nodos del 0 al 5, aristas controladas, costos enteros y protección del grafo original), junto con una capa adaptadora para exportar los resultados.

---

## Estructura del Proyecto

```text
ModuloGrafo/
│
├── nodo.py          # Clase que representa cada nodo individual y sus vecinos.
├── grafo.py         # Clase principal que valida el JSON y construye el grafo de forma atómica.
├── adaptador.py     # Capa extra para exportar el grafo en un formato estándar en memoria o JSON.
└── test2Adaptador.py # Script de prueba para validar el funcionamiento y la exportación.
└── test1Grafo.py     # Script de prueba para validar el funcionamiento del grafo.
```

---

## Descripción y Uso de las Clases

### 1. Clase `Nodo` (`nodo.py`)
Representa un nodo individual dentro del grafo. Almacena su identificador único (`id`) y una lista de sus vecinos con sus respectivos costos en una lista de tuplas.

* **Función principal:** `addVecino(nodo_vecino, costo)`
* **Códigos de retorno:**
  * `0`: Intento de auto-conexión (prohibido).
  * `1`: Conexión añadida con éxito.
  * `2`: Conexión duplicada (ya existía).

---

### 2. Clase `Grafo` (`grafo.py`)
Se encarga de leer un archivo JSON, validar todas las restricciones del sistema (exactamente 6 nodos del 0 al 5, costos enteros de 1 a 9, máximo 30 aristas y sin dejar un estado parcialmente construido si ocurre un error) de forma segura.

**Ejemplo de uso:**
```python
from grafo import Grafo

# Inicializa el grafo indicando el nodo de origen, de destino y la ruta del JSON
mi_grafo = Grafo(id_origen=0, id_destino=5, nombreJson="tu_archivo.json")

# Verifica que el grafo se haya construido correctamente
if mi_grafo.listaNodos:
    print(f"Grafo cargado con éxito. Total de aristas: {mi_grafo.aristas}")
```

---

### 3. Clase `AdaptadorGrafo` (`adaptador.py`)
Actúa como una capa adicional que transforma la estructura interna del grafo en un formato estandarizado en forma de diccionario de Python o directamente exportado como archivo físico en formato JSON.

**Formato de salida generado:**
```json
{
    "n": 6,
    "inicio": 0,
    "meta": 5,
    "aristas": [
        [0, 1, 2],
        [0, 2, 4],
        [1, 3, 3],
        [1, 5, 8],
        [2, 3, 1],
        [3, 4, 5],
        [4, 5, 2]
    ]
}
```

**Ejemplo de uso:**
```python
from grafo import Grafo
from adaptador import AdaptadorGrafo

# 1. Creamos y validamos el grafo
mi_grafo = Grafo(id_origen=0, id_destino=5, nombreJson="tu_archivo.json")

if mi_grafo.listaNodos:
    # 2. Instanciamos el adaptador pasándole el grafo
    adaptador = AdaptadorGrafo(mi_grafo)
    
    # Obtener el diccionario directamente en memoria
    datos_diccionario = adaptador.generar_diccionario()
    print(datos_diccionario)
    
    # O exportarlo directamente a un archivo físico
    adaptador.exportar_json("grafo_adaptado.json")
```

---

## Configuración y Ejecución de Pruebas

### Archivo de Entrada JSON de Ejemplo (`tu_archivo.json`)
El archivo JSON de entrada debe estructurarse de la siguiente manera, asegurando que los identificadores de nodos sean del `0` al `5`:

```json
{
    "nodos": {
        "0": { "1": 2, "2": 4 },
        "1": { "3": 3, "5": 8 },
        "2": { "3": 1 },
        "3": { "4": 5 },
        "4": { "5": 2 },
        "5": {}
    }
}
```

### Ejecutar las Pruebas
Para ejecutar los scripts de prueba ubicados en la carpeta `Test/` desde la raíz del proyecto evitando errores de rutas relativas o de importación, utiliza el siguiente comando como módulo:

```bash
python3 -m Test.test2Adaptador
