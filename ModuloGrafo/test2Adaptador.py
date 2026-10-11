from grafo import Grafo
from adaptador import AdaptadorGrafo

# 1. Creamos tu grafo normalmente
mi_grafo = Grafo(id_origen=0, id_destino=5, nombreJson="grafo.json")

# 2. Si el grafo se creó correctamente, usamos el adaptador
if mi_grafo.listaNodos:
    adaptador = AdaptadorGrafo(mi_grafo)
    
    # Obtener el diccionario directamente en memoria:
    diccionario_resultado = adaptador.generar_diccionario()
    print(diccionario_resultado)
    
    # O bien, guardarlo directamente como un nuevo archivo JSON:
    adaptador.exportar_json("grafo_adaptado.json")