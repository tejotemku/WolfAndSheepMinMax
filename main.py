from zadanie3.board import Board
import random


def minimax(board: Board, max_turn, depth: int, _debug=False):
    if depth == 0:
        if _debug:
            minimax_s = ''
            if max_turn:
                minimax_s = 'Max'
            else:
                minimax_s = 'Min'
            print(f'Depth - {depth}, Score - {board.evaluate_point()}, {minimax_s}')
            # board.show_board()
            # print('\n')
        return board.evaluate_point()

    # wolf's turn
    if max_turn:
        best_score = -10000
        for wolf_move in board.get_possible_moves(4):
            last_position_wolf = board.wolf
            board.wolf = wolf_move
            best_score = max(best_score, minimax(board, not max_turn, depth-1, _debug))
            board.wolf = last_position_wolf
        if _debug:
            minimax_s = ''
            if max_turn:
                minimax_s = 'Max'
            else:
                minimax_s = 'Min'
            print(f'Depth - {depth}, Score - {best_score}, {minimax_s}')
            # board.show_board()
            # print('\n')
        return best_score

    # sheep turn
    else:
        best_score = 10000
        for sh in range(0, 4):
            for sheep_move in board.get_possible_moves(sh):
                last_position_sheep = list(board.sheep)
                board.sheep[sh] = sheep_move
                best_score = min(best_score, minimax(board, not max_turn, depth-1, _debug))
                board.sheep = last_position_sheep
        if _debug:
            minimax_s = ''
            if max_turn:
                minimax_s = 'Max'
            else:
                minimax_s = 'Min'
            print(f'Depth - {depth}, Score - {best_score}, {minimax_s}')
            # board.show_board()
            # print('\n')
        return best_score


def find_best_move_for_wolf(board: Board, depth: int, show_boards=True, _debug=False):
    best_move = [(0, 0), -100000]
    for wolf_move in board.get_possible_moves(4):
        last_position_wolf = board.wolf
        board.wolf = wolf_move
        new_move = [wolf_move, minimax(board, False, depth-1, _debug)]
        if new_move[1] > best_move[1]:
            best_move = new_move
        board.wolf = last_position_wolf
    board.wolf = best_move[0]
    if show_boards:
        print(f'>>> Wolf has moved to {str(board.columns[best_move[0][0]])}:{best_move[0][1] + 1}')


def find_best_move_for_sheep(board: Board, depth: int, show_boards=True, _debug=False):
    best_move = [(0, 0), 100000, 0]
    for sh in range(0, 4):
        for sheep_move in board.get_possible_moves(sh):
            last_position_sheep = list(board.sheep)
            board.sheep[sh] = sheep_move
            new_move = [sheep_move, minimax(board, True, depth-1, _debug), sh]
            if new_move[1] < best_move [1]:
                best_move = new_move
            board.sheep = last_position_sheep
    board.sheep[best_move[2]] = best_move[0]
    if show_boards:
        print(f'>>> Sheep number {best_move[2]} has moved to {str(board.columns[best_move[0][0]])}:{best_move[0][1] + 1}')


def game_ai_wolf(x, depth, show_boards=True, _debug=False):
    board = Board(x)
    board.show_board()
    game_is_running = True
    turns = 0

    while game_is_running:

        # wolf's turn
        find_best_move_for_wolf(board, depth, show_boards, _debug)
        if show_boards:
            board.show_board()
        turns += 1
        if board.did_wolf_win():
            if show_boards:
                print(f'--------Wolf has won! In {turns} turns--------')
            return turns, 'W'

        # sheep turn
        sheep_random_moves = []
        for sh in range(0, 4):
            for sheep_move in board.get_possible_moves(sh):
                sheep_random_moves.append([sh, sheep_move])
        chosen_move = random.choice(sheep_random_moves)
        board.sheep[chosen_move[0]] = chosen_move[1]

        if show_boards:
            print(f'>>> Sheep number {chosen_move[0]} has moved to {str(board.columns[chosen_move[1][0]])}:{chosen_move[1][1] + 1}')
            board.show_board()
        turns += 1
        if board.did_sheep_win():
            if show_boards:
                print(f'--------Sheep has won! In {turns} turns--------')
            return turns, 'S'


def game_ai_sheep(x, depth, show_boards=True, _debug=False):
    board = Board(x)
    board.show_board()
    game_is_running = True
    turns = 0

    while game_is_running:

        # wolf turn
        wolf_random_moves = []
        for m in board.get_possible_moves(4):
            wolf_random_moves.append(m)
        chosen_move = random.choice(wolf_random_moves)
        board.wolf = chosen_move
        if show_boards:
            print(f'>>> Wolf has moved to {str(board.columns[chosen_move[0]])}:{chosen_move[1] + 1}')
            board.show_board()
        turns += 1
        if board.did_wolf_win():
            if show_boards:
                print(f'--------Wolf has won! In {turns} turns--------')
            return turns, 'W'

        # sheep turn
        find_best_move_for_sheep(board, depth, show_boards, _debug)
        if show_boards:
            board.show_board()
        turns += 1
        if board.did_sheep_win():
            if show_boards:
                print(f'--------Sheep has won! In {turns} turns--------')
            return turns, 'S'


def game_ai_vs_ai(x, depth, show_boards=True, _debug=False):
    board = Board(x)
    board.show_board()
    game_is_running = True
    turns = 0

    while game_is_running:
        if show_boards:
            print(f'\n\n>--------------wolf {turns//2} turn--------------<\n\n')

        # wolf's turn
        find_best_move_for_wolf(board, depth, show_boards, _debug)
        if show_boards:
            board.show_board()
        turns += 1
        if board.did_wolf_win():
            if show_boards:
                print(f'--------Wolf has won! In {turns} turns--------')
            return turns, 'W'

        if show_boards:
            print(f'\n\n>--------------sheep {turns//2} turn --------------<\n\n')

        # sheep turn
        find_best_move_for_sheep(board, depth, show_boards,_debug)
        if show_boards:
            board.show_board()
        turns += 1
        if board.did_sheep_win():
            if show_boards:
                print(f'--------Sheep has won! In {turns} turns--------')
            return turns, 'S'


def tournament(mode, replays: int, show_boards=True, _debug=False):
    modes = {
        'aiVSai': game_ai_vs_ai,
        'wolfAi': game_ai_wolf,
        'sheepAi': game_ai_sheep
    }

    for dep in range(2, 9):
        avg = 0
        i = 0
        wolf_wins = 0
        sheep_wins = 0
        for start in (0, 2, 4, 6):
            for j in range(0, replays):
                i += 1
                results = modes.get(mode)(start, dep, show_boards, _debug)
                avg += results[0]
                if results[1] == 'W':
                    wolf_wins += 1
                else:
                    sheep_wins += 1
        avg /= i
        print(f'Depth - {dep}, Average turns - {avg}, Wolf wins - {wolf_wins}, Sheep wins - {sheep_wins}')


# tournament('sheepAi', replays=20, show_boards=False, _debug=False)
game_ai_sheep(2, 5)


