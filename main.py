import chess
import random
import openai

openai.api_key = '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'

def imprimir_tablero(tablero):
    letras = '  a b c d e f g h'
    numeros = '87654321'
    for i in range(8):
        fila = [str(tablero.piece_at((7-i)*8 + j)) if tablero.piece_at((7-i)*8 + j) is not None else '.' for j in range(8)]
        print(f'{numeros[i]} {" ".join(fila)}')
    print(letras)

def obtener_movimiento_gpt(tablero):
    movimientos = " ".join([str(mov) for mov in tablero.move_stack])
    movimientos_legales = ", ".join([str(m) for m in tablero.legal_moves])
    color_jugador = "blancas" if tablero.turn == chess.WHITE else "negras"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"Eres un asistente de ajedrez jugando como las {color_jugador}. Analiza el estado actual del juego y detecta los peligros y amenzadas de tus piezas, da una breve descripción sobre el estado del juego en general y analiza lo bueno y malo de cada uno de tus movimientos posibles, finalmente proporciona tu probabilidad de ganar o perder la partida, y sugiere tu siguiente movimiento. Por favor, proporciona el movimiento sugerido en una nueva línea al final de tu mensaje en formato UCI (por ejemplo, 'e2e4'). Por ejemplo, si el estado actual del juego es '1.e4 e5 2.Cf3 Cc6 3.Ab5 a6', podrías responder con 'Las blancas tienen una ligera ventaja debido a un mejor control del centro. La probabilidad de ganar para las blancas es del 60%. Movimiento sugerido: e1g1'."},
            {"role": "user", "content": f"El estado actual del tablero es: {movimientos}. Los posibles movimientos legales son: {movimientos_legales}. Analiza el estado actual del juego y detecta los peligros y amenzadas de tus piezas, da una breve descripción sobre el estado del juego en general y analiza lo bueno y malo de cada uno de tus movimientos posibles, finalmente proporciona tu probabilidad de ganar o perder la partida, y sugiere tu siguiente movimiento de acuerdo a tu estudio. Recuerda el formato del movimiento sugerido, como: e1g1, no uses el número de movimiento ni puntos: no es útil, por ejemplo, '1...c7c5', tampoco: `d7d6` o 'd7d6' (no uses comillas), solo queremos el movimiento. Solamente: c7c5 es necesario."}
        ]
    )
    respuesta = response.choices[0].message["content"].strip()
    print("\n" + respuesta + "\n")
    movimiento_sugerido = respuesta.split("\n")[-1].split(":")[-1].strip()  # Extraemos el movimiento sugerido de la última línea
    return movimiento_sugerido

def jugar_ajedrez():
    tablero = chess.Board()
    turno = input("¿Quieres ser las blancas o las negras? (b/n): ")

    while not tablero.is_checkmate() and not tablero.is_stalemate():
        imprimir_tablero(tablero)
        if (turno == "b" and tablero.turn == chess.WHITE) or (turno == "n" and tablero.turn == chess.BLACK):
            print("\nMovimientos posibles: ", [tablero.san(m) for m in tablero.legal_moves])            
            movimiento = input("Ingresa tu movimiento: ")
            try:
                movimiento_uci = tablero.parse_san(movimiento)
                if movimiento_uci in tablero.legal_moves:
                    tablero.push(movimiento_uci)
                else:
                    print("Movimiento ilegal. Intenta de nuevo.")
            except:
                print("Movimiento no válido. Intenta de nuevo.")
        else:
            movimiento = obtener_movimiento_gpt(tablero)
            if chess.Move.from_uci(movimiento) in tablero.legal_moves:
                tablero.push(chess.Move.from_uci(movimiento))
            else:
                print("Movimiento sugerido por GPT es ilegal. Seleccionando un movimiento aleatorio.")
                movimiento = random.choice([move for move in tablero.legal_moves])
                tablero.push(movimiento)

    if tablero.is_checkmate():
        if (turno == "b" and not tablero.turn) or (turno == "n" and tablero.turn):
            print("\n¡Has ganado!")
        else:
            print("\nHas perdido.")
    else:
        print("\nEs un empate.")

if __name__ == "__main__":
    jugar_ajedrez()
