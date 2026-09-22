def epsilon_closure(estados,transiciones):#Definicion la función la cual confirma un estado,  y desde tal estado a donde puedesllegar sin gastar ningun simbolo
    resultado = set(estados) #Set(estados) crea una copia xd
    pila = list(estados) #eso de pila es un alista q vamos a usar como pendientes por ver

    while pila: # repite lo de adentro mientras pila no este vació
           estado = pila.pop()  # saca un elemento de pila y lo pone en el estado
           for t in transiciones: # recorre todas las transiciones
               if t["from"] == estado and t["symbol"] == "eps":  #filtra solo si transicion sale del estilo epsilon y es tipo epsilon
                  resultado.add(t["to"]) #agrega el destino al resultao
                  pila.append(t["to"])# si se paso del filtro agrega el destin a resultao

    return resultado # cuando el while termina devuelv eel rsultado



def move(estados,simbolo,transiciones): # recibe un conjunto de estados y un simbolo y nos dice a que estados llegamos desde cualquiera de esoss si seguimos una transicion a entese simbolo
 resultado = set() # set vacio donde vammo guardando los estados destno
 for estado in estados:  # recorremos cada estado conjuto entrada
     for t in transiciones: # por cada estado,recorremo transiciones
         if t["from"] == estado and t["symbol"] == simbolo: # si la transicion sale de ese estado y es con el simbolo q andamos buscando
             resultado.add(t["to"]) # agregamos el estado destino al resultado
 return resultado # retornamos todos los estados a los q se llega


def convertir_nfa_a_dfa(estados, alfabeto, inicial,aceptacion,transiciones):
    estado_inicial_dfa = epsilon_closure({inicial}, transiciones)
    estados_dfa = [estado_inicial_dfa] # lista de todos los estados del DFA que vamo viendo
    pendientes = [estado_inicial_dfa] # lista de los q nos faltan por revisar
    transiciones_dfa = [    ] # lista de transiciones del dfa que vamos a ir construyendo
    while pendientes: # mientas haya algun pendiente o algo por revisar
         actual = pendientes.pop() # sacamos uo de la lista pendientes pa procesarlo despues
         for simbolo in alfabeto: # recorremos cada simbolo del alfabeto uno por uno
             nuevo_conjunto = epsilon_closure(move(actual,simbolo,transiciones), transiciones) # desde el  conjunto actual a cauntos estamos llegamos gastando ese simbolo, con epsilon envolvemos el resultado
             if not nuevo_conjunto: # un set vacio se comporta como falso asi que esto pregunta si eso quedó vacio
                 continue # le dice al for q se salte el resto de esa vuelta,pase directo al siguente simbolo y queno hagamos nads mas con el caso
             
             transiciones_dfa.append({"from": actual, "symbol":simbolo, "to": nuevo_conjunto})

             if nuevo_conjunto not in estados_dfa: # revisamos si ese conjutno ya esta en la listad estados del dfa que llevamos hasta ahorita
                estados_dfa.append(nuevo_conjunto) # si no está, es un estado nuevo y lo agregamos . pa q ue quede parte del dfa final
                pendientes.append(nuevo_conjunto) #tambien lo agregsamos a pendientes porque si es nuevo tambien hay q revisarlo por si algo
    return estados_dfa, transiciones_dfa, estado_inicial_dfa #retornamos normal



def simular (estados_dfa, transiciones_dfa, estado_inicial_dfa,aceptacion,cadena): #simularemos el dfa que construimos 
    actual = estado_inicial_dfa #empezamos en el estado inicial del dfaa
    camino = [estado_inicial_dfa] # es la lista de estado q vamos pasando en orden

    for simbolo in cadena: #recorremos cadena
        encuentra_transicion = False # variable q dice si encontramos una transicion


        for t in transiciones_dfa: #recorremos cada transicion del dfa
             if t["from"] == actual and t["symbol"] == simbolo:
               actual = t["to"] # si encontramos una transicion q salga del estado actual y sea simbolo,nos movenos a ese estado destino
               encuentra_transicion = True # si encontramos una transicion, ponemos la variable en True
               camino.append(t["to"]) # agregamos el estado
               break # salimos del estado rokpiendo los for

        if encuentra_transicion == False: # si no encontraoms una transicion,la cadena no es aceptada
          return {"path": camino ,"accepted" : False} # retornamos

    return {"path": camino, "accepted": any(estado in aceptacion    for estado in actual)} # si terminamos de recorrer la cadena, retornamos el camino y el si el estado final es aceptado o no")    


#funcion conjunto a string
def conjunto_a_string(conjunto):
    ordenado = sorted(conjunto) # ordena el conjunto
    convertido = [str(x) for x in ordenado] # convierte el conjunto a string
    return ("" . join(convertido)) # retorna el string

#Prueba

if __name__ == "__main__":
    transiciones = [
        {"from": 0, "to": 1, "symbol": "eps"},
        {"from": 0, "to": 3, "symbol": "eps"},
        {"from": 1, "to": 2, "symbol": "a"},
        {"from": 3, "to": 4, "symbol": "b"},
        {"from": 2, "to": 5, "symbol": "eps"},
        {"from": 4, "to": 5, "symbol": "eps"},
    ]
    estados = [0,1,2,3,4,5,6]
    alfabeto = ["a","b"]
    inicial = 0
    aceptacion =[4]

    print(epsilon_closure({0}, transiciones))

    #probamos 
    print(conjunto_a_string({0, 1, 3}))

#Probamo la simulación
    estados_dfa, transiciones_dfa, estado_inicial_dfa = convertir_nfa_a_dfa(estados, alfabeto, inicial, aceptacion, transiciones)
    print(simular(estados_dfa, transiciones_dfa, estado_inicial_dfa, aceptacion, "a"))
    print(simular(estados_dfa, transiciones_dfa, estado_inicial_dfa, [5], "a"))#testeamos con los datos q ya teniamos antes
    print(simular(estados_dfa, transiciones_dfa, estado_inicial_dfa, [4], "a"))# mismo caso
    print(convertir_nfa_a_dfa(estados,alfabeto,inicial,aceptacion,transiciones)) # printeamos y probamos
    print(move({1,3}, "a", transiciones)) # {2}