#los arboles son datos jerarquicos, como un mapa mental o un oranigrama

from treelib import Tree
escuela = Tree() #aqui se crea el arbol

#Su base es un nodo raiz, es el elemento principal del arbol
escuela.create_node("Aula", "01") #definimos el nodo raiz con el nombre y el id

#se agregan nodos hijos al nodo raiz
escuela.create_node("Profesor", "prof", parent = "01") #se declara el pariente por su id
escuela.create_node("Representante", "repre", parent = "01")
escuela.create_node("Estudiantes", "alumn", parent = "01")

#aqui ya puedo definir los nombres de los nodos agregando hijos a los nodos
escuela.create_node("Mel", "alumna", parent = "alumn")
escuela.create_node("Salazar", "Maestro", parent = "prof")
escuela.create_node("Lala", "repre1", parent = "repre")

#para mostrar el arbol se usa .show()
escuela.show()