En este repositorio se tiene un jugador de HEX, basado en una busqueda de Monte Carlo pura(pure Monte Carlo search), utilizando
una estrategia de caminos de costo minimo.

## Busqueda de Monte Carlo pura

Partiendo de un estado ( un tablero de HEX con jugadas hechas y el jugador actual).

Se elige una jugada inicial al azar dentro de unas posibles jugadas.

Luego se simula una partida completa desde esta jugada. 

Y esto se repite mientras haya tiempo.

Al final se elige la jugada inicial con mayor porcentaje de victorias.

## Estrategia de los caminos de costo minimo:

Resumen: Considera jugar SOLO en las casillas desocupadas que pertenecen a algun camino de costo minimo.
Porque si consigues ocuparlas, ganaras en la menor cantidad de movimientos posibles.

Para esta estrategia considera el tablero del hex como un grafo con las conexiones usuales. Donde:
-Moverse a un nodo del otro jugador es imposible ( costo infinito),
-Moverse a un nodo que no pertenece a ningun jugador tiene costo 1,
-Moverse a un nodo propio tiene costo 0.

Ademas el grafo tiene una fuente y un sumidero. (source and sink).
La fuente (S) esta conectada al extremo inicial. (izquierda o superior)
El sumidero (T) esta conectado al extremo final. (derecha o inferior)

Y se busca jugar en los caminos de costo minimo de S a T.

## Como se integra esta estrategia con Monte Carlo

El conjunto de jugadas iniciales a partir de un estado se determinan usando esta estrategia.

Ademas a la hora de simular una partida solo se consideran jugadas en los caminos de costo minimo.

## Desventajas

Cuando existen varios nodos para jugar en un camino de costo minimo. Y alguno de ellos es critico, porque si el oponente lo ocupa el costo del camino de costo minima aumenta. EL algoritmo decide aleatoriamente y no se da cuenta de ese "eslabon debil".

```
    3
1       4
    2
```

Por ejemplo, supon que 1,2,3,4 son nodos en un camino de costo minimo. 1 conectado a 2,3. 2,3 conectado a 4.
Si ya se jugo en 1. Jugar en 4 es mejor que jugar en 2 o 3. Pero el algoritmo quizas elija jugar en 2, y el oponente
puede jugar en 4 eliminando ese camino de costo minimo.
