import copy


class Board:
    def __init__(self, x):
        self.board_spaces = []
        for i in range(0, 8):
            row = []
            for j in range(0, 8):
                if (i + j) % 2 == 0:
                    row.append('   ')
                else :
                    row.append('□  ')
            self.board_spaces.append(row)
        self.sheep = [(1, 7), (3, 7), (5, 7), (7, 7)]
        self.wolf = (x, 0)
        self.directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        self.columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def show_board(self):
        print('  A  B  C  D  E  F  G  H')
        board = copy.deepcopy(self.board_spaces)
        for i in range(len(self.sheep)):
            board[self.sheep[i][1]][self.sheep[i][0]] = str(i) + 's '
        board[self.wolf[1]][self.wolf[0]] = 'W  '

        for i in range(7, -1, -1):
            row = str(i+1) + '  '
            for j in range(0, 8):
                row += board[i][j]
            print(row)
        print("\n")

    # 0-3 sheep id , 4 wolf id
    def move_player(self, x, y, player_id):
        if player_id == 4:
            self.wolf = (x, y)
            return
        self.sheep[player_id] = (x, y)

    def check_if_free(self, x, y):
        is_free = True
        is_free = is_free and not (self.wolf[0] == x and self.wolf[1] == y)
        for i in range(0, 4):
            is_free = is_free and not (self.sheep[i][0] == x and self.sheep[i][1] == y)
        return is_free

    def get_possible_moves(self, player_id):
        possible_directions = []
        if player_id == 4:
            player = self.wolf
            for d in self.directions:
                new_dir = (player[0] + d[0], player[1] + d[1])
                if 0 <= new_dir[0] < 8 and 0 <= new_dir[1] < 8 and self.check_if_free(new_dir[0], new_dir[1]):
                    possible_directions.append(new_dir)
        else:
            player = self.sheep[player_id]
            for d in [(1, -1), (-1, -1)]:
                new_dir = (player[0] + d[0], player[1] + d[1])
                if 0 <= new_dir[0] < 8 and 0 <= new_dir[1] < 8 and self.check_if_free(new_dir[0], new_dir[1]):
                    possible_directions.append(new_dir)
        return possible_directions

    def did_wolf_win(self):
        return self.wolf[1] == 7 or (self.wolf[1] >= self.sheep[0][1] and self.wolf[1] >= self.sheep[1][1] and
                                     self.wolf[1] >= self.sheep[2][1] and self.wolf[1] >= self.sheep[3][1])

    def did_sheep_win(self):
        return len(self.get_possible_moves(4)) == 0

    def evaluate_point(self):
        score = self.wolf[1]*10
        number_of_sheep_around = 0
        sheep_penalty = [0, -5, -18, -50, -1000]
        for d in self.directions:
            for sheep in self.sheep:
                if self.wolf[0] + d[0] == sheep[0] and self.wolf[1] + d[1] == sheep[1]:
                    number_of_sheep_around += 1
        score += sheep_penalty[number_of_sheep_around]
        if self.wolf[1] == 7:
            score = 1000
        return score


