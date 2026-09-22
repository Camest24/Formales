#Prueba con minimizer.equivalent_pairs.
#Se ejecutan con python de toda la vida
import unittest #libreria de pruebas
from minimizer import equivalent_pairs #funcion a probar

class TestEquivalentPairs(unittest.TestCase): #cada metodo es un test
    def test_ejemplo_del_pdf(self):
      #DFA de 6 Estados del Enunciado, el unico par equivalente despues de las pruebas fue (4,5)
      delta = [[1, 2], [3, 4], [4, 3], [5, 5], [5, 5], [5, 5]]  # tabla de transiciones (columnas: a, b), el único par equivalente debe ser (4, 5); finales = 1, 4, 5
      self.assertEqual(equivalent_pairs(delta, [1, 4, 5]), [[4, 5]]) 

    def test_un_solo_estado(self): # caso borde. solo el estado 0
     #Sin pares posibles la lista es vacia
      self.assertEqual(equivalent_pairs([[0]], [0]), []) #unico estado es final
      self.assertEqual(equivalent_pairs([[0, 0]], []), []) # sin finales,alfabeto de 2 letras

    def test_alfabeto_de_una_letra_ya_minimo(self):  # caso borde: una sola columna
        delta = [[1], [2], [2]]  # 0 -> 1 -> 2 -> 2
        # solo el 2 es final y todos se distinguen: no hay equivalentes
        self.assertEqual(equivalent_pairs(delta, [2]), [])

    def test_todos_equivalentes(self):  # todos los estados hacen lo mismo
        delta = [[1], [1]]  # 0 va a 1 y 1 se queda en 1
        # ambos son finales, así que 0 y 1 son equivalentes
        self.assertEqual(equivalent_pairs(delta, [0, 1]), [[0, 1]])

    def test_varios_pares_equivalentes(self): # 1 y 2 van a finales; 3 y 4 son finales que se quedan en sí mismos ,# por eso 1 ≡ 2 y 3 ≡ 4; el 0 se distingue de todos
    
      delta = [[1, 2], [3, 4], [4, 3], [3, 3], [4, 4]] # 1 y 2 vana ser finales, 3 y 4 se quedan en si mismos, #1=2 y 3=4 el 0 se dinstigue de todos
      self.assertEqual(equivalent_pairs(delta, [3, 4]), [[1, 2], [3, 4]])

    def test_pares_ordenados_y_con_p_menor_que_q(self):  #revisa el formato de la salida
        delta = [[1, 2], [3, 4], [4, 3], [3, 3], [4, 4]] # mismo DFA de la prueba pasada
        pares = equivalent_pairs(delta, [3, 4]) # guardamos el resultado
        self.assertEqual(pares, sorted(pares)) # deben venir en orden "lexicografico curiosamente"
        for p, q in pares: # revisamos cada par
            self.assertLess(p, q) # siempre p menor que q

if __name__ == '__main__': # solo si se ejectua este archivo directamente
    unittest.main() #corre toda prueba