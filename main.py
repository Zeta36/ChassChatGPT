import chess
import random
import openai

openai.api_key = 'sk-xxxx'

def imprimir_tablero(tablero):
    letras = '  a b c d e f g h'
    numeros = '87654321'
    for i in range(8):
        fila = [str(tablero.piece_at((7-i)*8 + j)) if tablero.piece_at((7-i)*8 + j) is not None else '.' for j in range(8)]
        print(f'{numeros[i]} {" ".join(fila)}')
    print(letras)

def obtener_movimiento_gpt(tablero):
    movimientos = " ".join([str(mov) for mov in tablero.move_stack])
    movimientos_legales = ", ".join([tablero.san(m) for m in tablero.legal_moves])
    color_jugador = "blancas" if tablero.turn == chess.WHITE else "negras"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"Eres un asistente de ajedrez jugando como las {color_jugador}. Analiza el estado actual del juego da una breve descripción sobre el estado del juego en general, analiza cada uno de tus movimientos posibles así como la posible respuesta de tu rival. Para seleccionar tu siguiente movimiento debes maximizar siempre el valor tus piezas comparando tu estado actual y el valor tras tu movimiento y el valor esperado tras la posible respuesta del rival. Debes tener en cuenta todos tus movimientos y maximizar el valor de tus piezas al mismo tiempo que desarrollas la mejor estrategia posible. Por favor, proporciona el movimiento sugerido en una nueva línea al final de tu mensaje en formato SAN (por ejemplo, 'd6'). Por ejemplo, si el estado actual del juego es '1.e4 e5 2.Nf3 Nc6 3.Bb5 a6', podrías responder con: Las blancas tienen una ligera ventaja debido a un mejor control del centro. El valor de mis piezas actuales es 29, tras mi movimiento será 29 y tras el mejor movimiento del adversario será de 28. Movimiento sugerido (igual al que maximiza): d6"},
            {"role": "user", "content": f"El estado actual del tablero es: {movimientos}. Los posibles movimientos legales son: {movimientos_legales}. Analiza el estado actual del juego da una breve descripción sobre el estado del juego en general, analiza cada uno de tus movimientos posibles así como la posible respuesta de tu rival. Para seleccionar tu siguiente movimiento debes maximizar siempre el valor tus piezas comparando tu estado actual y el valor tras tu movimiento y el valor esperado tras la posible respuesta del rival. Debes tener en cuenta todos tus movimientos y maximizar el valor de tus piezas al mismo tiempo que desarrollas la mejor estrategia posible. Por favor, proporciona el movimiento sugerido en una nueva línea al final de tu mensaje en formato SAN (por ejemplo, 'd6'). Por ejemplo, si el estado actual del juego es '1.e4 e5 2.Nf3 Nc6 3.Bb5 a6', podrías responder con: Las blancas tienen una ligera ventaja debido a un mejor control del centro. El valor de mis piezas actuales es 35, tras mi movimiento será 35 y tras el mejor movimiento del adversario será de 32. Movimiento sugerido (que debe ser el que maximiza tras el estudio): d6. Recuerda el formato del movimiento sugerido, como: Nc6, no uses el número de movimiento ni puntos: no es útil, por ejemplo, '1...Nc6', tampoco: `Nc6` ni 'Nc6' ni Nc6. (no uses comillas ni puntos), solo queremos el movimiento. Solamente: Nc6"}
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
            movimiento = tablero.parse_san(obtener_movimiento_gpt(tablero))
            if movimiento in tablero.legal_moves:
                tablero.push(movimiento)
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
