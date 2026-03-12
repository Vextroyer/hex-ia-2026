# MCTSV1

El primer algoritmo, que no es monte carlo pero esta basado en el.
Para el estado actual del tablero mira todas las posibles acciones ( casillas vacias )
Luego mientras le quede tiempo, elige una al azar.
Y simula una partida desde esa accion, jugando siempre al azar para ambos.
Entonces, anota para cada accion cuantas partida gana.
Y devuelve la accion que gane mas partidas

## Resultados
El algoritmo funciona mejor que el random en tableros pequenos (n = 5). Juega bien incluso contra mi.

En tableros grandes (n = 20), es como un random. Hace jugadas aleatorias que no lo acercan a conectar sus caminos.
Es como si estuviese "confundido".

Una mejora que se le puede hacer es acotar la cantidad de acciones inicial.
Para esto aplicare la estrategia de los caminos de costo minimo.

# Estrategia de los caminos de costo minimo:

Resumen: Considera hacer tu jugada, SOLO en las casillas desocupadas que pertenecen a algun camino de costo minimo.
Porque si consigues ocuparlas, ganaras en la menor cantidad de movimientos posibles.

Para esta estrategia considera el tablero del hex como un grafo con las conexiones usuales. Donde:
-Moverse a un nodo del otro jugador es imposible ( costo infinito),
-Moverse a un nodo que no pertenece a ningun jugador tiene costo 1,
-Moverse a un nodo propio tiene costo 0.

Ademas el grafo tiene una fuente y un sumidero. (source and sink).
La fuente (S) esta conectada al extremo inicial. (izquierda o superior)
El sumidero (T) esta conectado al extremo final. (derecha o inferior)

Y se busca jugar en los caminos de costo minimo de S a T.

## Implementacion y complejidad
Con una modificacion al algoritmo de Dijkstra es posible hallar los nodos que pertenecen a estos caminos.
Se guarda para cada nodo sus "padres", es decir, sus predecesores en los distintos caminos de costo minimo.
Despues se explora estos caminos, de hijos a padres, desde el sumidero hasta la fuente.
Si el tamano del tablero es NxN. Hay un orden de M = N^2 nodos.
El algoritmo de Dijkstra con una cola de prioridad toma O(ElogV), en este caso O(MlogM). La cantidad de aristas es O(6M) que es O(M).
Y la exploracion esta acotada a O(M). Porque cada nodo solo se explora una vez.
Por tanto la complejidad de esta estrategia es de O(MlogM)

# MCTSV2

El mismo algoritmo que antes. Con un cambio.

Solo considera como acciones jugar en nodos que pertenecen a algun camino de costo minimo.

## Resultados
El algoritmo mantiene el rendimiento contra el random en tableros pequenos. (n = 5)

Y en tableros grandes ya no se confunde. Al contrario, se concentra. Es como si jugara en una linea recta.
En tableros con n = 20, consistentemente derrota al random en 20 jugadas. Teoricamente lo mejor.

Pero.

Cuando existen varios nodos para ocupar. Y alguno de ellos es critico, porque si el oponente lo ocupa el costo del
camino de costo minima aumentara. EL algoritmo decide aleatoriamente y no se da cuenta de ese "eslabon debil".

# MCTSV3

En la simulacion. Jugar tambien en los caminos de costo minimo. Superior al algoritmo anterior.