El algoritmo funciona mejor que el random en tableros pequenos. Juega bien incluso contra mi.

En tableros grandes (n = 20), es como un random.

El algoritmo actual, que no es monte carlo pero esta basado en el.
Para el estado actual del tablero mira todas las posibles acciones ( casillas vacias)
Luego mientras le quede tiempo, elige una al azar.
Y simula una partida desde esa accion, jugando siempre al azar para ambos
Entonces, anota para cada accion cuantas partida gana.
Y devuelve la accion que gane mas partidas

Una mejora que se le puede hacer es acotar la cantidad de acciones inicial.
Para esto aplicare la estrategia de los caminos de costo minimo.

En resumen:
Transforma el grafo del hex en un dag. Tiene un procedimiento especifico por capas.
Haya los caminos de costo minimo.
Reduce las acciones posibles a jugar en esos caminos de costo minimo.