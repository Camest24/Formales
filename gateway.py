from functions import convertir_nfa_a_dfa , conjunto_a_string # exportamos las funciones de functions 

#/convert
#Primero va para el nfa a dfa
#Conjunto a string

def convert (estados, alfabeto, inicial,aceptacion,transiciones): 
  estados_dfa, transiciones_dfa, estado_inicial_dfa = convertir_nfa_a_dfa(estados, alfabeto, inicial,aceptacion,transiciones) #ejecutamos el algortitmo  y guardamos cosas del DFA
  dfaStates = [conjunto_a_string(x) for x in estados_dfa]  #recorremos cada set dentro del dfa y los convertimos a string
  
  transitions = [] #lista nueva donde ir guardando las transiciones ya convertidaS
  for t in transiciones_dfa: #recorremos cada transicion vieja  del dfa
      nueva_transicion = {"from": conjunto_a_string(t["from"]), "symbol": t["symbol"], "to": conjunto_a_string(t["to"])} #acá estamos armando la transicion en fformato de texto(from y to como string, symbol mismo caso xd)
      transitions.append(nueva_transicion) # la agregamos a la lista de trasiciones ya convertidas

      #ahora falta convertir el estado inicial a un texto ahi
  dfaInitial = conjunto_a_string (estado_inicial_dfa)
  acceptingStates = [conjunto_a_string(estado) for estado in estados_dfa if any(x in aceptacion for x in estado)] # recorremos cada conjuto del estados dfa ,despues lo poasamos por un fiiltro,solo lo dejar pasar si dentro dde estre estasdo un x es aceptado, y por ultimo los que si pasan arman una lista quedandome con el estadd completo

  return {"dfaStates": dfaStates, "transitions": transitions,  "acceptingStates": acceptingStates} #devolvemos un diccionario con todo lo que necesitamos del propio dfa              


#Siguente función
def simulate (dfaStates, transitions, acceptingStates,cadena):
   actual= dfaStates[0] # el primer elemnto de la lista, q es el inicial tambiie
   camino = [actual] # arrancamos igual que en simular del functions,con el inical ya dentro

   for simbolo in cadena: #recorremos cadena
     encuentra_transicion = False # variable q dice si encontramos una transicion
     for t in transitions: #recorremos cada transiicion del dfa
           if t["from"] == actual and t["symbol"] == simbolo:
                actual = t["to"] # si encontramos una transicion q salga del estado actual y sea simbolo,nos movenos a ese estado destino
                encuentra_transicion = True # si encontramos una transicion, ponemos la variable en True
                camino.append(t["to"]) # agregamos el estado
                break # salimos del estado rokpiendo los for

     if encuentra_transicion == False: # si no encontraoms una transicion,la cadena no es aceptada
           return {"path": camino ,"accepted" : False} # retornamos
           
   return {"path": camino, "accepted": actual in acceptingStates} # si terminamos de recorrer la cadena, retornamos el camino y el si el estado final es aceptado")    

#Probamos que funcione
if __name__ == "__main__":
    estados = [0, 1, 2, 3, 4, 5]
    alfabeto = ["a", "b"]
    inicial = 0
    aceptacion = [4]
    transiciones = [
        {"from": 0, "to": 1, "symbol": "eps"},
        {"from": 0, "to": 3, "symbol": "eps"},
        {"from": 1, "to": 2, "symbol": "a"},
        {"from": 3, "to": 4, "symbol": "b"},
        {"from": 2, "to": 5, "symbol": "eps"},
        {"from": 4, "to": 5, "symbol": "eps"},
    ]
    print(convert(estados, alfabeto, inicial, aceptacion, transiciones))

    dfa = convert(estados, alfabeto, inicial, aceptacion, transiciones)
    print(simulate(dfa["dfaStates"], dfa["transitions"], dfa["acceptingStates"], "ab")) # funciona bien