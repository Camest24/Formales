#Equivalencia de estados de UN DFA con el Algoritmo de tabla de Pares , Marcado por kozen en la Lectura 14
#Solo Tiene la logica, el servidor despues llama a equivalent_pairs

#La idea es Dos Estaods p y q son equivalentes si ninguna cadena x los separa,osea basicamente , para toda x(delta(p,x) es final si y solo si delta(q,x) es final)
#Por el contrario,si existe una cadena x q los separe decimos que p y q son distingibles y marcamos el par {p,q}
#El algoritmo va marcando todos los pares distingibiles . Los q al final quedan sin marcar son exactaente los pares equivalentes

#combinations(lista 2, genera todos los pares posibles sin repetir y invertir el orden, (0,1) y (0,2)....., (1,2) . siempre con p < q)
from itertools import combinations

