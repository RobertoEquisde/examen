class Ajedrez:
    def __init__(self, estado=[]):
        fvacias = [[0 for i in range(8)] for j in range(4)]
        """Constructor"""
        self.estado = fvacias + fvacias
        self.visualiza()
        npiezas = -1
        while npiezas < 0 or npiezas > 64:
            npiezas = int(input("Ingrese número de piezas a ingresar: "))
        if npiezas == 0:
            self.estado = (
                [[1, 2, 3, 4, 5, 3, 2, 1], [6 for i in range(8)]]
                + fvacias
                + [[-6 for i in range(8)], [-1, -2, -3, -4, -5, -3, -2, -1]]
            )
        else:
            piezas = [
                "(1) ♖ ♜ Torre | "
                "(2) ♘ ♞ Caballlo | "
                "(3) ♗ ♝ Alfil | "
                "(4) ♕ ♛ Reina | "
                "(5) ♔ ♚ Rey | "
                "(6) ♙ ♟ Peon | "
            ]
            for i in range(npiezas):
                print("Pieza", i + 1, "de", npiezas)
                fila, col, jugador, code_pieza = -1, -1, -1, 0
                while fila < 0 or fila > 7:
                    fila = int(input("Ingrese número de fila de la pieza (0-7): "))
                while col < 0 or col > 7:
                    col = int(input("Ingrese número de columna de la pieza (0-7): "))
                while jugador != 1 and jugador != 2:
                    jugador = int(
                        input("Ingrese a qué jugador el pertenece la pieza (1,2): ")
                    )
                for p in piezas:
                    print(p)
                while code_pieza < 1 or code_pieza > 6:
                    code_pieza = int(input("Ingrese el código de pieza (1-6): "))
                signo = 1 if jugador == 1 else -1
                self.estado[fila][col] = code_pieza * signo

        self.torres = [[False, False], [False, False]]
        self.kingmov = [False, False]
        self.capP = []

    def __str__(self):
        """Cadena del estado del juego"""
        tam = 8
        contador_fila = 1
        juego = "   "
        for i in range(8):
            juego += " " + str(i) + "  "
        juego += "\n  ┌" + "───┬" * 7 + "───┐\n"
        for fila in self.estado:
            juego += str(contador_fila - 1) + " │"
            contador_col = 1
            for columna in fila:
                if columna > 0:
                    S = [" ♜ ", " ♞ ", " ♝ ", " ♛ ", " ♚ ", " ♟ "]
                    juego += S[columna - 1]
                elif columna < 0:
                    S = [" ♖ ", " ♘ ", " ♗ ", " ♕ ", " ♔ ", " ♙ "]
                    juego += S[(columna * -1) - 1]
                else:
                    juego += "   "

                if contador_col < tam:
                    juego += "│"
                else:
                    juego += "│\n"

                contador_col += 1

            if contador_fila < tam:
                juego += "  ├" + "───┼" * (tam - 1) + "───┤" + "\n"
            contador_fila += 1
        juego += "  └" + "───┴" * 7 + "───┘"
        return juego

    def visualiza(self):
        """Impresión de la matriz"""
        print(self)

    def mover(self, fila, col, pieza):
        print("Antes:", self.estado)
        self.estado[fila][col] = pieza
        print("Después:", self.estado)

    def asigna(self, fila, col, fpieza, cpieza, jugador):
        """Afecta el estado del juego para reflejar las decisiones del jugador"""
        print("Blancas: ", jugador == 1 and fpieza >= 0)
        print("Negras:  ", jugador == 2 and fpieza <= 0)
        if (jugador == 1 and self.estado[fpieza][cpieza] >= 0) or (
            jugador == 2 and self.estado[fpieza][cpieza] <= 0
        ):
            validez = self.revisaTirada(
                fila,
                col,
                fpieza,
                cpieza,
            )
            if validez == 0:
                print("No es un movimiento válido, ingrese una posición válida")
                return False
            elif validez == 2:
                return True
            else:
              
                self.mover(fila, col, self.estado[fpieza][cpieza])
                self.mover(fpieza, cpieza, 0)
                return True
        else:
            print("Seleccione las piezas del jugador correcto")
            return False

    def capturaAlPaso(self, fmovida, cmovida, capturadoras):
        pieza_movida = self.estado[fmovida][cmovida]
        cmovida = "blanco" if pieza_movida > 0 else "negro"
        ccapturadora = "negro" if pieza_movida > 0 else "blanco"
        print(
            "Se puede capturar al paso el peón",
            cmovida,
            "en",
            fmovida,
            ",",
            cmovida,
        )
        print("Los peones de color", ccapturadora, "que pueden capturarlo son:")
        for i in range(len(capturadoras)):
            print(str(i) + ") Peón en", capturadoras[i][0], ",", capturadoras[i][1])
        print(
            "Para capturar al paso ingresa el número de peón, de otro modo ingresa -1"
        )
        respuesta = -2
        while respuesta < -1 or respuesta >= len(capturadoras):
            respuesta = int(input("Peón que va a capturar al paso: "))
        self.capP = []
        if respuesta == -1:
            return 1
        else:
            if pieza_movida > 0:
                print(
                    "Peón capturado blanco:",
                    fmovida,
                    ",",
                    cmovida,
                    ",",
                    -1 * pieza_movida,
                )
                self.mover(fmovida - 1, cmovida, -1 * pieza_movida)
            else:
                print(
                    "Peón capturado negro:",
                    fmovida,
                    ",",
                    cmovida,
                    ",",
                    -1 * pieza_movida,
                )
                self.mover(fmovida + 1, cmovida, -1 * pieza_movida)
            self.mover(capturadoras[respuesta][0], capturadoras[respuesta][1], 0)
            self.mover(fmovida, cmovida, 0)
            return 2

    def revisaTirada(self, fila, col, fpieza, cpieza):
        posTab = lambda x: x >= 0 and x <= 7
    
        if (
            posTab(fpieza)
            and posTab(cpieza)
            and posTab(fila)
            and posTab(col)
        ):
         
            pieza = self.estado[fpieza][cpieza]
          
            celda_final = self.estado[fila][col]
            if pieza != 0:
                if pieza * celda_final <= 0 or pieza * celda_final == 5:
                    if abs(pieza) == 1:
                        validez = self.revT(fila, col, fpieza, cpieza)
                        if validez == 1:
                            return 1
                        elif validez == 2:
                            return 2
                    elif abs(pieza) == 2:
                        if self.revcab(fila, col, fpieza, cpieza) == 1:
                            return 1
                    elif abs(pieza) == 3:
                        if self.revAlf(fila, col, fpieza, cpieza) == 1:
                            return 1
                    elif abs(pieza) == 4:
                        if self.revqueen(fila, col, fpieza, cpieza) == 1:
                            return 1
                    elif abs(pieza) == 5:
                        if self.revking(fila, col, fpieza, cpieza) == 1:
                            return 1
                    else:
                        if self.revP(fila, col, fpieza, cpieza) == 1:
                            return 1
                    print(
                        "Movimiento no válido para el tipo de pieza seleccionado, reingrese las posiciones"
                    )
                else:
                    print("Las piezas son del mismo jugador, reingrese las posiciones")
            else:
                print("Seleccionaste una casilla vacía, reingrese las posiciones")
                print("fila:", fpieza, "col:", cpieza)
                print(self.estado[fpieza])
                print(self.estado[fpieza][cpieza])
        else:
            print(
                "Alguna de las posiciones ingresadas no es válida, reingrese las posiciones"
            )
        return 0

    def revT(self, fila, col, fpieza, cpieza):
   
        pieza = self.estado[fpieza][cpieza]
        destino = self.estado[fila][col]
        if pieza > 0 and destino == 5 and not self.kingmov[0] and fpieza == 0:
            print("Enroque blancas")
            if cpieza == 0 and not self.torres[0][0]:
                print("Torre izquierda")
                for i in range(1, 4):
                    if self.estado[fila][i] != 0:
                        return 0
                self.torres[0][0] = True
                self.kingmov[0] = True
                self.mover(fila, col, 1)
                self.mover(fpieza, cpieza, 5)
                print("Fin enroque 1")
                return 2
            elif cpieza == 7 and not self.torres[0][1]:
                print("Torre derecha")
                for i in range(5, 7):
                    if self.estado[fila][i] != 0:
                        return 0
                self.torres[0][1] = True
                self.kingmov[0] = True
                self.mover(fila, col, 1)
                self.mover(fpieza, cpieza, 5)
                print("Fin enroque 2")
                return 2
        elif (
            pieza < 0 and destino == -5 and not self.kingmov[1] and fpieza == 7
        ):
            print("Enroque negras")
            if cpieza == 0 and not self.torres[1][0]:
                for i in range(1, 4):
                    if self.estado[fila][i] != 0:
                        return 0
                self.torres[1][0] = True
                self.kingmov[1] = True
                self.mover(fila, col, -1)
                self.mover(fpieza, cpieza, -5)
                return 2
            elif cpieza == 7 and not self.torres[1][1]:
                for i in range(5, 7):
                    if self.estado[fila][i] != 0:
                        return 0
                self.torres[1][1] = True
                self.kingmov[1] = True
                self.mover(fila, col, -1)
                self.mover(fpieza, cpieza, -5)
                return 2
        print("Movimientos normales Torre")
   
        if pieza * destino <= 0:
            if fila - fpieza == 0 and abs(col - cpieza) <= 7:
                a = min([col, cpieza])
                b = max([col, cpieza])
                for i in range(a + 1, b):
                    if self.estado[fila][i] != 0:
                        return 0
                if fpieza == 1:
                    if cpieza == 0:
                        self.torres[0][0] = True
                    elif cpieza == 7:
                        self.torres[0][1] = True
                elif fpieza == 7:
                    if cpieza == 0:
                        self.torres[1][0] = True
                    elif cpieza == 7:
                        self.torres[1][1] = True
                return 1
            elif col - cpieza == 0 and abs(fila - fpieza) <= 7:
                a = min([fila, fpieza])
                b = max([fila, fpieza])
                for i in range(a + 1, b):
                    if self.estado[i][col] != 0:
                        return 0
                return 1
        return 0

    def revcab(self, fila, col, fpieza, cpieza):
        if abs(fila - fpieza) == 1:
            if abs(col - cpieza) == 2:
                return 1
        elif abs(fila - fpieza) == 2:
            if abs(col - cpieza) == 1:
                return 1
        return 0

    def revAlf(self, fila, col, fpieza, cpieza):
        dif_fila = fila - fpieza
        dif_col = col - cpieza
        if abs(dif_fila) == abs(dif_col):
            if dif_fila > 0:
                busca_fila = -1
            else:
                busca_fila = 1
            if dif_col > 0:
                busca_col = -1
            else:
                busca_col = 1
            fila_camino = fila + busca_fila
            col_camino = col + busca_col
            while fila_camino != fpieza:
                if self.estado[fila_camino][col_camino] != 0:
                    return 0
                fila_camino += busca_fila
                col_camino += busca_col
            return 1
        return 0

    def revqueen(self, fila, col, fpieza, cpieza):
        if (
            self.revT(fila, col, fpieza, cpieza) == 1
            or self.revAlf(fila, col, fpieza, cpieza) == 1
        ):
            return 1
        return 0

    def revking(self, fila, col, fpieza, cpieza):
        pieza = self.estado[fpieza][cpieza]
        destino = self.estado[fila][col]
        # Enroque
        if pieza > 0 and destino == 1 and not self.kingmov[0] and fpieza == 0:
            print("Enroque blancas")
            if col == 0 and not self.torres[0][0]:
                print("Torre izquierda")
                for i in range(1, 4):
                    if self.estado[fila][i] != 0:
                        return 0
                self.torres[0][0] = True
                self.kingmov[0] = True
                self.mover(fila, col, 5)
                self.mover(fpieza, cpieza, 1)
                print("Fin enroque 1")
                # Hace que no se vuelvan a asignar las piezas
                return 2
            elif col == 7 and not self.torres[0][1]:
                print("Torre derecha")
                for i in range(5, 7):
                    if self.estado[fila][i] != 0:
                        return 0
                self.torres[0][1] = True
                self.kingmov[0] = True
                self.mover(fila, col, 5)
                self.mover(fpieza, cpieza, 1)
                print("Fin enroque 2")
                return 2
       
        elif (
            pieza < 0 and destino == -1 and not self.kingmov[1] and fpieza == 7
        ):
            print("Enroque negras")
            if col == 0 and not self.torres[1][0]:
                for i in range(1, 4):
                    if self.estado[fila][i] != 0:
                        return 0
                self.torres[1][0] = True
                self.kingmov[1] = True
                self.mover(fila, col, -5)
                self.mover(fpieza, cpieza, -1)
                return 2
            elif col == 7 and not self.torres[1][1]:
                for i in range(5, 7):
                    if self.estado[fila][i] != 0:
                        return 0
                self.torres[1][1] = True
                self.kingmov[1] = True
                self.mover(fila, col, -5)
                self.mover(fpieza, cpieza, -1)
                return 2
        print("Movimiento normal")
        dif_fila = abs(fila - fpieza)
        dif_col = abs(col - cpieza)
        if (
            (dif_fila == 0 and dif_col == 1)
            or (dif_fila == 1 and dif_col == 0)
            or (dif_fila == 1 and dif_col == 1)
        ):
            if pieza > 0:
                self.kingmov[0] = True
            else:
                self.kingmov[1] = True
            return 1
        return 0

    def revP(self, fila, col, fpieza, cpieza):
        # TODO: En passant
        pieza = self.estado[fpieza][cpieza]
        celda_destino = self.estado[fila][col]
        # TODO: Coronación
        if pieza * celda_destino == 0:
            if pieza > 0:
                if fila - fpieza == 1 and col - cpieza == 0:
                    return 1
                elif (
                    fila - fpieza == 2 and col - cpieza == 0 and fpieza == 1
                ):
                    # Checa si se cumplen las condiciones para captura al paso
                    if cpieza == 0:
                        if self.estado[fila][col + 1] == -6:
                            self.capP.append([fila, col])
                            self.capP.append([fila, col + 1])
                    elif cpieza == 7:
                        if self.estado[fila][col - 1] == -6:
                            self.capP.append([fila, col])
                            self.capP.append([fila, col - 1])
                    else:
                        peonIzq = self.estado[fila][col - 1] == -6
                        peonDer = self.estado[fila][col + 1] == -6
                        if peonIzq or peonDer:
                            self.capP.append([fila, col])
                            if peonIzq:
                                self.capP.append([fila, col - 1])
                            if peonDer:
                                self.capP.append([fila, col + 1])
                    return 1
            else:
                if fila - fpieza == -1 and col - cpieza == 0:
                    return 1
                elif (
                    fila - fpieza == -2 and col - cpieza == 0 and fpieza == 6
                ):
                    if cpieza == 0:
                        if self.estado[fila][col + 1] == 6:
                            self.capP.append([fila, col])
                            self.capP.append([fila, col + 1])
                    elif cpieza == 7:
                        if self.estado[fila][col - 1] == 6:
                            self.capP.append([fila, col])
                            self.capP.append([fila, col - 1])
                    else:
                        peonIzq = self.estado[fila][col - 1] == 6
                        peonDer = self.estado[fila][col + 1] == 6
                        if peonIzq or peonDer:
                            self.capP.append([fila, col])
                            if peonIzq:
                                self.capP.append([fila, col - 1])
                            if peonDer:
                                self.capP.append([fila, col + 1])
                    return 1
      
        else:
           
            if pieza > 0:
                if fila - fpieza == 1 and (
                    col - cpieza == 1 or col - cpieza == -1
                ):
                    return 1
          
            elif fila - fpieza == -1 and (
                col - cpieza == 1 or col - cpieza == -1
            ):
                return 1
        return 0

    def jugar(self):
        pedirMov = True
        jugador = 1
        while pedirMov:
          
            self.visualiza()
            try:
                print("Turno de ", end="")
                mensaje = "blancas" if jugador == 1 else "negras"
                print(mensaje)
                if self.capP == []:
                    fila, col, fpieza, cpieza = -1, -1, -1, -1
                    while fpieza < 0 or fpieza > 7:
                        fpieza = int(
                            input("Ingrese el numero de fila de la pieza (0,8): ")
                        )
                    while cpieza < 0 or cpieza > 7:
                        cpieza = int(
                            input("Ingrese el numero de columna de la pieza (0,8): ")
                        )
                    while fila < 0 or fila > 8:
                        fila = int(
                            input("Ingrese el numero de fila de destino (0,8): ")
                        )
                    while col < 0 or col > 8:
                        col = int(
                            input("Ingrese el numero de columna de destino (0,8): ")
                        )
                    if self.asigna(fila, col, fpieza, cpieza, jugador):
                        self.visualiza()
                        jugador = 2 if jugador == 1 else 1
                else:
                    movida = self.capP.pop(0)
                    resultado = self.capturaAlPaso(
                        movida[0], movida[1], self.capP
                    )
                    if resultado == 2:
                        jugador = 2 if jugador == 1 else 1

            except KeyboardInterrupt:
                pedirMov = False
                print("\nJuego interrumpido")


"""
a = Ajedrez(
    [
        [1, 0, 0, 0, 5, 0, 0, 1],
        [6, 0, 0, 0, 6, 0, 0, 6],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, -6, 0, -6, 0, -6, -6, 0],
        [0, 6, 0, 6, 0, 6, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-6, 0, 0, 0, -6, 0, 0, -6],
        [-1, 0, 0, 0, -5, 0, 0, -1],
    ]
)
a = Ajedrez(
    [
        [1, 2, 3, 4, 5, 3, 2, 1],
        [6, 6, 6, 6, 6, 6, 6, 6],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-6, -6, -6, -6, -6, -6, -6, -6],
        [-1, -2, -3, -4, -5, -3, -2, -1],
    ]
)
a = Ajedrez(
    [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 2, 2, -2, 2, 0],
        [0, -2, 2, -2, -2, -2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [-2, -2, -2, -2, 2, 2, 2, 2],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
)
"""
a = Ajedrez()

print("Estado inicial: ", a.estado, "\n")
a.jugar()
