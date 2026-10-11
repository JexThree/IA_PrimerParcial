import json
from nodo import Nodo

class Grafo:
    def __init__(self, id_origen, id_destino, nombreJson):
        self.aristas = 0
        self.listaNodos = []
        self.id_origen = None
        self.id_destino = None

        # 1. Validación de argumentos de entrada (id_origen e id_destino deben estar entre 0 y 5)
        if not isinstance(id_origen, int) or not (0 <= id_origen <= 5):
            print("Error: El id_origen proporcionado no es un entero válido entre 0 y 5.")
            return
        if not isinstance(id_destino, int) or not (0 <= id_destino <= 5):
            print("Error: El id_destino proporcionado no es un entero válido entre 0 y 5.")
            return

        # Leemos el archivo .json de forma segura
        try:
            with open(nombreJson, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except Exception as e:
            print(f"Error al leer o decodificar el archivo JSON: {e}")
            return

        nodos_dict = datos.get("nodos")
        if not isinstance(nodos_dict, dict):
            print("Error: El JSON no contiene una estructura 'nodos' válida.")
            return

        # 2. Construcción atómica: Si falla algo, el grafo no se inicializa parcialmente
        if self._construirGrafo(nodos_dict):
            # Validar que los IDs de origen y destino existan en los nodos creados
            origen_nodo = next((n for n in self.listaNodos if n.id == id_origen), None)
            destino_nodo = next((n for n in self.listaNodos if n.id == id_destino), None)

            if not origen_nodo:
                print(f"Error: El nodo origen ({id_origen}) no existe dentro de los 6 nodos del grafo.")
                return
            if not destino_nodo:
                print(f"Error: El nodo destino ({id_destino}) no existe dentro de los 6 nodos del grafo.")
                return

            self.id_origen = id_origen
            self.id_destino = id_destino
            print("Grafo creado e inicializado con éxito.")
        else:
            print("Error: El grafo no pudo ser construido debido a fallas en las restricciones.")
            # Limpieza para evitar dejar un estado parcialmente utilizable
            self.listaNodos = []
            self.aristas = 0

    def _construirGrafo(self, nodos):
        # Exigir exactamente los identificadores del 0 al 5
        esperados = {0, 1, 2, 3, 4, 5}
        
        # Verificar que las llaves principales correspondan exactamente a los 6 nodos requeridos
        keys_convertidas = set()
        for k in nodos.keys():
            if not isinstance(k, str) or not k.isdigit():
                print(f"Error: Identificador de nodo no numérico o inválido en JSON: {k}")
                return False
            keys_convertidas.add(int(k))

        if keys_convertidas != esperados:
            print(f"Error: El grafo debe constar exactamente de los nodos 0 a 5. Encontrados: {sorted(list(keys_convertidas))}")
            return False

        nodos_mapeo = {}
        for i in range(6):
            nodos_mapeo[i] = Nodo(i)

        total_aristas = 0

        # Procesar aristas y restricciones de vecinos
        for id_origen_str, vecinos in nodos.items():
            origen_id = int(id_origen_str)
            nodo_origen = nodos_mapeo[origen_id]

            if not isinstance(vecinos, dict):
                print(f"Error: Los vecinos del nodo {origen_id} deben estructurarse en un objeto/diccionario.")
                return False

            for id_destino_str, costo in vecinos.items():
                if not isinstance(id_destino_str, str) or not id_destino_str.isdigit():
                    print(f"Error: ID de destino inválido: {id_destino_str}")
                    return False

                destino_id = int(id_destino_str)
                if destino_id < 0 or destino_id > 5:
                    print(f"Error: El ID de destino {destino_id} está fuera del rango 0-5.")
                    return False

                # Rechazar booleanos explícitamente (en Python isinstance(True, int) es True)
                if isinstance(costo, bool) or not isinstance(costo, int):
                    print(f"Error: El costo '{costo}' debe ser estrictamente un número entero (no booleano).")
                    return False

                if not (1 <= costo <= 9):
                    print(f"Error: El costo {costo} debe estar entre 1 y 9.")
                    return False

                nodo_destino = nodos_mapeo[destino_id]

                # Intentar añadir la arista evaluando reglas de negocio
                resultado = nodo_origen.addVecino(nodo_destino, costo)

                if resultado == 0:
                    print(f"Error: Se prohíbe conectar al nodo {origen_id} consigo mismo.")
                    return False
                elif resultado == 2:
                    print(f"Error: Se detectó una arista duplicada hacia el mismo destino desde el nodo {origen_id}.")
                    return False
                elif resultado == 1:
                    total_aristas += 1
                    if total_aristas > 30:
                        print("Error: Se ha superado el límite máximo de 30 aristas permitidas.")
                        return False

        self.listaNodos = [nodos_mapeo[i] for i in range(6)]
        self.aristas = total_aristas
        return True