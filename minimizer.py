#Equivalencia de estados de UN DFA con el Algoritmo de tabla de Pares , Marcado por kozen en la Lectura 14
#Solo Tiene la logica, el servidor despues llama a equivalent_pairs

#La idea es Dos Estaods p y q son equivalentes si ninguna cadena x los separa,osea basicamente , para toda x(delta(p,x) es final si y solo si delta(q,x) es final)
#Por el contrario,si existe una cadena x q los separe decimos que p y q son distingibles y marcamos el par {p,q}
#El algoritmo va marcando todos los pares distingibiles . Los q al final quedan sin marcar son exactaente los pares equivalentes

#combinations(lista 2, genera todos los pares posibles sin repetir y invertir el orden, (0,1) y (0,2)....., (1,2) . siempre con p < q)
from itertools import combinations

def equivalent_pairs(delta,finals):
    #delta[q][i] #Estados al que va q con el i-esimo simbolo, finals= finales
    n= len(delta) #Numero de estados = numeros de filas de la tabla
    finals = set(finals) #Set para preguntar "está en finales"

    #Paso 1 : todos los pares {p,q} con p menor q ,sin marcar
    marked ={pair: False for pair in combinations(range(n),2)} #Diccionario con todos los pares posibles, inicialmente sin marcar

    #Paso 2 : marcar todos los pares {p,q} con p final y q no final
    for p, q in marked: # recorremos cada par
        if(p in finals) !=(q in finals): # uno final y el otro no
            marked[p, q] = True #Se distinguen con la cadena vacía

    #Paso 3 : Propagar marcas hasta q una vuelta no cambie nada
    changed = True #Dice si la ultimas vuelta marcó algo
    while changed: # repetimos mientras haya cambios
        changed = False #asumimos q en esta vuelta no cambia nada
        for (p, q), is_marked in marked.items(): #recorremos todos los pares
          if is_marked: # si ya esta marcado lo saltamos
            continue
          for a in range(len(delta [p])): # probamos cada simbolo
             r, s = delta[p][a], delta[q][a] #Estados a los que van p y q con el simbolo a
             if r !=s and marked[(min(r,s), max(r,s))]: # Destinos ya dinstingibles
                marked[(p, q)] = True #Entonces p y q tambien lo son
                changed = True # hace otra vuelta
                break # no hace falta comprobar mas

    #Paso 4: Los pares sin marcar son los equivalentres ( ya salen en orden)
    return[[p,q] for (p,q), is_marked in marked.items() if not is_marked]
           