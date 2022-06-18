class Gato():
      def __init__(self, coef):
            self.Ren = len(coef)
            self.Col = len(coef[0])
            self.M = []
            # Crea la matriz
            for i in range(self.Ren):
                  self.M.append([0]*self.Col)
            # Llena la Matriz
            for i in range(self.Ren):
                  for j in range(self.Col):
                        self.M[i][j] = coef[i][j]

      def __str__(self):
            """Visualiza la matriz"""
            L = ["   ", " x ", " o "]
            r = ""
            for i in range(self.Ren):
                  for j in range(self.Col):
                        r += L[self.M[i][j]]
                        if j < 2:
                              r += " | "
                  r += "\n---------------\n"       
            return r

      def visualiza(self):
            """Visualiza la matriz"""
            print(self)

      def revisa(self):
            for i in range(3):
                  for j in range (3):
                        #Horizontales
                        if self.M[j][0] == self.M[j][1] and self.M[j][1] == self.M[j][2] and self.M[j][2] == i:
                              return i
                        #Verticales
                        if self.M[0][j] == self.M[1][j] and self.M[1][j] == self.M[2][j] and self.M[2][j] == i:
                              return i
            #Diagonales
            if self.M[0][0] == self.M[1][1] and self.M[1][1] == self.M[2][2] and self.M[2][2] == i:
                  return i
            if self.M[0][2] == self.M[1][1] and self.M[1][1] == self.M[2][0] and self.M[2][0] == i:
                   return i
                  #Si aun quedan movimientos#
            for k in range(self.Ren):
                   for m in range(self.Col):
                        if self.M[m][k] == 0:
                              return 0
            return 3

                

      def asigna(self, i, j, v):
            r = self.Ren
            c = self.Col
            if r >= 0 and r <= 3 and c >= 0 and c <= 3 and (v == 1 or v == 2):
                  self.M[i][j] = v




      def juego(self):
            self.visualiza()
            jugador = - 1
            while jugador < 1 or jugador > 2:

                  jugador = int(input("¿Quieres ser jugador 1 (X) o jugador 2 (O): "))
                  if jugador > 2 or jugador < 1:
                        print ("Opción incorrecta.\nSolo puedes escoger 1 o 2.")

            gano = 0
            while gano == 0:

                  if jugador == 3:
                        print ("Turno del jugador 1 con ficha X")
                  if jugador == 2:
                        print ("Turno del jugador 2 con ficha O")      
                  if jugador > 2:
                        jugador = 1
                  vacio = 1


                  while vacio != 0:

                        i = -1
                        while i < 0 or i > 3:
                              i = int(input("Dame el renglon donde quieres a tirar: (0, 1 o 2)  "))

                              if i < 0 or i > 2:
                                    print ("Solo puedes escoger 0, 1 o 2 como posición.")
                                    i = int(input("Dame el renglon donde quieres a tirar: (0, 1 o 2)  "))



                        j = -1
                        while j < 0 or j > 3:
                              j = int(input("Dame la columna donde quieres a tirar: (0, 1 o 2)  "))

                              if j < 0 or j > 2:
                                    print ("Solo puedes escoger 0, 1 o 2.")
                                    j = int(input("Dame la columna donde quieres a tirar: (0, 1 o 2)  "))



                        vacio = self.M[i][j]

                  self.asigna(i, j, jugador)
                  self.visualiza()
                  self.gano()
                  gano = self.revisa()
                  jugador += 1










      def gano(self):

            if self.revisa() == 1:
                  print("¡¡Felicidades!! ¡¡El jugador 1 ha ganado !!")
            if self.revisa() == 2:
                  print("¡¡Felicidades!! ¡¡El jugador 2 ha ganado!!")
            if self.revisa() == 3:
                  print("Gato --> (=^･ω･^=)")





                  
      """
      Prueba de las clases
      """
if __name__ == '__main__':
      a = Gato([[0,0,0], [0,0,0], [0,0,0]])
      #a.visualiza()
      a.juego()