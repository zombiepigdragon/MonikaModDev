default persistent.tetris_difficulty = 6

init python in mas_tetris:
    import random, copy

    ticks = -1
    BOARD_SIZE = (12, 20) #Logical size of board
    TILE_SIZE = (32, 32) #Physical size of tile
    BOARD_RENDER_SIZE = (BOARD_SIZE[0] * TILE_SIZE[0], BOARD_SIZE[1] * TILE_SIZE[1])

    class TetrisGameMaster(renpy.Displayable):
        def __init__(self, board_image, piece_images, **kwargs):
            # Pass additional properties on to the renpy.Displayable
            # constructor.
            super(TetrisGameMaster, self).__init__(**kwargs)

            game = TetrisGame(len(piece_images), (12, 20))
            self.game = game

            #Let the boards do their setup too
            self.player_board = TetrisBoardRenderer(game.boards[0], board_image, piece_images)
            self.monika_board = TetrisBoardRenderer(game.boards[1], board_image, piece_images)

            self.ai = BasicTetrisAI(game, 1, 7)

            self.game.start()
        
        def render(self, width, height, st, at):
            global ticks
            ticks = int(at * 1000)
            self.game.update()
            self.ai.run()
            render = renpy.Render(width, height)
            p_board_render = self.player_board.render(0, 0, st, at)
            m_board_render = self.monika_board.render(0, 0, st, at)
            render.blit(p_board_render, ((width / 10) * 2 - (BOARD_RENDER_SIZE[0] / 2), height / 2 - (BOARD_RENDER_SIZE[1] / 2)))
            render.blit(m_board_render, ((width / 10) * 8 - (BOARD_RENDER_SIZE[0] / 2), height / 2 - (BOARD_RENDER_SIZE[1] / 2)))
            renpy.redraw(self, 0)
            return render
        
        def event(self, ev, x, y, st):
            import pygame
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_w:
                    self.game.handle_event(Actions.HARD_DROP, 0)
                elif ev.key == pygame.K_s:
                    self.game.handle_event(Actions.MOVE_DOWN, 0)
                elif ev.key == pygame.K_a:
                    self.game.handle_event(Actions.MOVE_LEFT, 0)
                elif ev.key == pygame.K_d:
                    self.game.handle_event(Actions.MOVE_RIGHT, 0)
                elif ev.key == pygame.K_q:
                    self.game.handle_event(Actions.ROTATE_CCW, 0)
                elif ev.key == pygame.K_e:
                    self.game.handle_event(Actions.ROTATE_CW, 0)
            if self.player_board.game_over:
                return True
            elif self.monika_board.game_over:
                return False
            else:
                raise renpy.IgnoreEvent()

    class TetrisBoardRenderer(renpy.Displayable):
        def __init__(self, board, board_image, piece_images, **kwargs):
            # Pass additional properties on to the renpy.Displayable
            # constructor.
            super(TetrisBoardRenderer, self).__init__(**kwargs)

            self.board = board

            self.board_render = renpy.render(board_image, 0, 0, 0, 0)
            self.piece_renders = []
            for piece in piece_images:
                self.piece_renders.append(renpy.render(piece, 0, 0, 0, 0))

            self.game_over = False

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            render.blit(self.board_render, (0, 0))
            for y, row in enumerate(self.board.grid):
                for x, value in enumerate(row):
                    if value > 0:
                        tile = self.piece_renders[value - 1]
                        render.blit(tile, (x * 32, y * 32))
            piece = self.board.current_piece
            value = piece.color
            for point in piece.get_world_pattern():
                tile = self.piece_renders[value - 1]
                render.blit(tile, (point.x * 32, point.y * 32))
            self.game_over = self.board.game_over
            return render
        
        def event(self, ev, x, y, st, player=False):
            return None
            

    #The actual Tetris implementation, based on https://github.com/zombiepigdragon/Tetris-VS-Ai

    class Translation:
        def __str__(self):
            return "(" + str(self.x) + ", " + str(self.y) + ")"

        def __repr__(self):
            return "Translation(" + str(self.x) + ", " + str(self.y) + ")"

        def __eq__(self, other):
            return self.x == other.x and self.y == other.y

        def __init__(self, x, y, combined=None):
            self.x = x
            self.y = y
            if combined is not None:
                if len(combined) != 2:
                    raise ValueError()
                else:
                    self.x = combined[0]
                    self.y = combined[1]

    class Point(Translation):
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0

        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, value):
            value = int(value)
            if value >= Point.min_x and value < Point.max_x:
                self._x = value
            else:
                raise ValueError()

        @property
        def y(self):
            return self._y

        @y.setter
        def y(self, value):
            value = int(value)
            if value >= Point.min_y and value < Point.max_y:
                self._y = value
            else:
                raise ValueError()

        def __repr__(self):
            return "Point(" + str(self.x) + ", " + str(self.y) + ")"

        def __init__(self, x, y, combined=None):
            self.x = x
            self.y = y
            if combined is not None:
                if len(combined) != 2:
                    raise ValueError()
                else:
                    self.x = combined[0]
                    self.y = combined[1]
                    

    class Actions:
        MOVE_DOWN = 1
        MOVE_LEFT = 2
        MOVE_RIGHT = 3
        HARD_DROP = 4
        ROTATE_CW = 5
        ROTATE_CCW = 6
        LEN = 6 #This should be an enum but it's not available so len is required for random

    class TetrisGame:
        def __init__(self, color_count, board_size):
            boards = []
            Point.max_x, Point.max_y = board_size
            for _ in range(2):
                b = TetrisBoard(board_size, color_count)
                boards.append(b)
            self.boards = boards

        def start(self):
            self.score = 0
            self.current_time = 0
            self.level = 0
            for b in self.boards:
                b.time_since_last_move_down = 0
                b.cleared_lines = 0
                b.set_next_piece()
                b.last_down_time = -1

        def update(self):
            self.level = self.calculate_level()
            drop_time = self.get_drop_time(self.level)
            for b in self.boards:
                b.move_piece_down_if_time(drop_time, b.current_piece)
                b.clear_lines()

        def calculate_level(self):
            total_lines = 0
            for b in self.boards:
                total_lines += b.cleared_lines
            level = int(total_lines / 10) + 1
            if self.level != level:
                print("New level:", level)
            return level

        def get_drop_time(self, level):
            return int(1000 / level)

        def handle_event(self, event, board_index):
            board = self.boards[board_index]
            piece = board.current_piece
            try:
                if event is Actions.MOVE_DOWN:
                    board.move_piece_down(piece)
                elif event is Actions.MOVE_LEFT:
                    board.transform_piece(Translation(-1, 0), piece)
                elif event is Actions.MOVE_RIGHT:
                    board.transform_piece(Translation(1, 0), piece)
                elif event is Actions.HARD_DROP:
                    board.hard_drop_piece(piece)
                elif event is Actions.ROTATE_CW:
                    board.rotate_piece(1, piece)
                elif event is Actions.ROTATE_CCW:
                    board.rotate_piece(-1, piece)
            except PieceCantMoveException:
                return False
            except PieceOutOfBoundsException:
                return False
            return True #No error occured

    class TetrisBoard:
        def __init__(self, size, color_count):
            self.width, self.height = size
            #Make a width by height grid of 0s
            self.grid = [[0 for x in range(self.width)] for y in range(self.height)]
            self.color_count = color_count
            self.cleared_lines = 0
            self.game_over = False

        def set_next_piece(self):
            pattern = random.choice(TetrisPiece.Patterns)
            color = random.randrange(1, self.color_count)
            position = Point(int(self.width / 2), 0)
            p = TetrisPiece(pattern, position, color)
            try:
                self.transform_piece(Translation(0, 0), p)
            except PieceCantMoveException:
                self.game_over = True
            self.current_piece = p
            self.last_down_time = ticks

        def merge_piece(self, piece):
            piece_pattern = piece.get_world_pattern()
            for point in piece_pattern:
                self.grid[point.y][point.x] = piece.color
            self.last_piece_position = piece.position
            self.set_next_piece()

        def move_piece_down_if_time(self, threshold, piece):
            if ticks - self.last_down_time > threshold:
                self.move_piece_down(piece)

        def move_piece_down(self, piece):
            try:
                self.transform_piece(Translation(0, 1), piece)
            except PieceCantMoveException:
                self.merge_piece(piece)
            except PieceOutOfBoundsException:
                self.merge_piece(piece)
            self.last_down_time = ticks

        def hard_drop_piece(self, piece):
            can_lower = True
            while can_lower:
                try:
                    self.transform_piece(Translation(0, 1), piece)
                except PieceCantMoveException:
                    can_lower = False
                except PieceOutOfBoundsException:
                    can_lower = False
            self.merge_piece(piece)

        def transform_piece(self, distance, piece):
            #Check if transform valid
            try:
                pattern = piece.get_world_pattern()
            except ValueError:
                raise PieceOutOfBoundsException()
            for point in pattern:
                try:
                    new_point = Point(point.x + distance.x, point.y + distance.y)
                except ValueError:
                    raise PieceOutOfBoundsException()
                if self.grid[new_point.y][new_point.x] != 0:
                    raise PieceCantMoveException()
            piece.position = Point(piece.position.x + distance.x, piece.position.y + distance.y)

        def rotate_piece(self, direction, piece):
            assert(direction == 1 or direction == -1)
            try:
                pattern = piece.get_rotated_pattern(direction)
                w_pattern = piece.get_world_pattern(pattern)
                for point in w_pattern:
                    if self.grid[point.y][point.x] != 0:
                        raise PieceCantMoveException()
            except ValueError:
                raise PieceCantMoveException()
            piece.pattern = pattern

        def clear_lines(self):
            for index, row in enumerate(self.grid):
                for value in row:
                    if value == 0:
                        break
                else:
                    del self.grid[index]
                    self.grid.insert(0, [0 for x in range(self.width)])
                    self.cleared_lines += 1

        def count_gaps(self):
            rotated = list(zip(*self.grid)) #Turn the board -90 degrees
            gaps = 0
            for row in rotated:
                seen_piece = False
                for column in row:
                    if column == 0:
                        if seen_piece:
                            gaps += 1
                    else:
                        seen_piece = True
            return gaps

        def count_rows(self):
            count = 0
            for index, row in enumerate(reversed(self.grid)):
                for column in row:
                    if column != 0:
                        count = index
            return count

        def copy(self):
            return copy.deepcopy(self)

    class TetrisPiece:

        Patterns = (
            [(-1, 0), (0, 0), (1, 0), (2, 0)],  #I
            [(0, 1), (0, 0), (1, 0), (2, 0)],   #J
            [(0, 1), (0, 0), (-1, 0), (-2, 0)], #L
            [(0, 0), (1, 0), (0, 1), (1, 1)],   #O
            [(-1, 0), (0, 0), (0, 1), (1, 1)],  #S
            [(-1, 0), (0, 0), (1, 0), (0, 1)],  #T
            [(-1, 0), (0, 0), (0, 1), (1, 1)]   #Z
        )

        for pattern in Patterns:
            for index, pos in enumerate(pattern):
                pattern[index] = Translation(pos[0], pos[1])
        del index, pos, pattern

        def __init__(self, pattern, position, color):
            self.pattern = pattern
            self.position = position
            assert(color > 0)
            self.color = color
        
        def get_world_pattern(self, pattern=None):
            if pattern == None:
                pattern = self.pattern
            w_pattern = copy.copy(pattern)
            for index, point in enumerate(w_pattern):
                w_pattern[index] = Point(point.x + self.position.x, point.y + self.position.y)
            return w_pattern

        def get_rotated_pattern(self, direction):
            pattern = copy.copy(self.pattern)
            for index, old_point in enumerate(pattern):
                new_point = Translation(-direction * old_point.y, direction * old_point.x)
                pattern[index] = new_point
            return pattern

        def copy(self):
            return copy.deepcopy(self)

    class PieceCantMoveException(Exception):
        pass

    class PieceOutOfBoundsException(Exception):
        pass


    class BasicTetrisAI:
        def __init__(self, game, board_index, difficulty):
            self.game = game
            self.board_index = board_index
            self.board = game.boards[board_index]
            self.last_time = -1
            print(difficulty)
            self.difficulty = difficulty
            self.success = True
            self.next_move = None
            self.set_next_move_time()
            self.moves_remaining_before_mistake = self.calculate_mistake_moves(difficulty)

        def set_next_move_time(self):
            raw_time = 1000 / self.difficulty
            offset = raw_time / 10
            min_time = int(raw_time - offset)
            max_time = int(raw_time + offset)
            self.next_move_time = random.randrange(min_time, max_time)

        def run(self):
            if ticks - self.last_time > self.next_move_time:
                self.last_time = ticks
                self.set_next_move_time()
                if self.success:
                    self.set_next_move()
                if self.next_move is not None:
                    move = self.next_move.move
                    if (self.moves_remaining_before_mistake == 0):
                        move = random.randint(1, Actions.LEN)
                        self.moves_remaining_before_mistake = self.calculate_mistake_moves(self.difficulty)
                    else: 
                        self.moves_remaining_before_mistake -= 1
                    self.success = self.game.handle_event(move, 1)
                else:
                    self.success = True
                    return None

        def set_next_move(self):
            if self.next_move is None:
                outcomes = self.PotientialOutcome.get_possible_outcomes(self.board)
                lowest_gap_count = min([outcome.gaps for outcome in outcomes])
                outcomes = [outcome for outcome in outcomes if outcome.gaps == lowest_gap_count]
                lowest_height = min([outcome.height for outcome in outcomes])
                outcomes = [outcome for outcome in outcomes if outcome.height == lowest_height]
                lowest_piece_y = max([outcome.final_position.y for outcome in outcomes])
                outcomes = [outcome for outcome in outcomes if outcome.final_position.y == lowest_piece_y]
                moves = [BasicTetrisAI.Move(outcome.rotations_needed, outcome.translations_needed) for outcome in outcomes]
                least_moves = min([len(move) for move in moves])
                moves = [move for move in moves if len(move) == least_moves]
                self.next_move = moves[0]
            else:
                self.next_move = self.next_move.next_move

        def calculate_mistake_moves(self, difficulty):
            if difficulty <= 0:
                return -1
            if difficulty > 10:
                difficulty = 10
            a = 15 #Probably there's a better way 
            b = 20
            minimum = difficulty + b
            maximum = a * difficulty * difficulty + b * difficulty + difficulty
            moves = random.randint(minimum, maximum)
            print(moves, "before mistake")
            return moves

        class PotientialOutcome():

            @staticmethod
            def get_possible_outcomes(board):
                rotated_pieces = []
                rotated_pieces.append(board.current_piece.copy())
                for i in range(3):
                    p = rotated_pieces[i]
                    rotated_pieces.append(TetrisPiece(p.get_rotated_pattern(1), p.position, p.color))
                possible_outcomes = []
                for r_index, r_piece in enumerate(rotated_pieces):
                    for x in range(board.width):
                        p = r_piece.copy()
                        p.position = Translation(x, 0)
                        valid = True
                        for point in p.pattern:
                            def move_into_valid_y(pattern):
                                for point in pattern:
                                    point.y += 1
                                for point in pattern:
                                    if point.y < 0:
                                        move_into_valid_y(pattern)
                                        break
                            w_point = Translation(point.x + p.position.x, point.y + p.position.y)
                            if w_point.x < 0 or w_point.x >= board.width:
                                valid = False
                            if w_point.y < 0:
                                move_into_valid_y(p.pattern)
                        if not valid:
                            continue
                        b = board.copy()
                        b.hard_drop_piece(p)
                        if b.game_over:
                            continue
                        move = BasicTetrisAI.PotientialOutcome(
                            b.count_gaps(), b.count_rows(), r_index, 
                            Translation(-(board.current_piece.position.x - p.position.x), 0), p.position)
                        possible_outcomes.append(move)
                return possible_outcomes

            def __init__(self, gaps, height, rotations_needed, translations_needed, final_position):
                self.gaps = gaps
                self.height = height
                self.rotations_needed = rotations_needed
                self.translations_needed = translations_needed
                self.final_position = final_position

            def __repr__(self):
                return "Outcome(gaps: " + str(self.gaps) + ", height: " + str(self.height) + ", rotations_needed: " + \
                str(self.rotations_needed) + ", translations_needed: " + str(self.translations_needed) + \
                ", final_position: " + str(self.final_position) + ")"

        class Move:
            def __init__(self, roatations_needed, translations_needed):
                if translations_needed.y > 0:
                    self.move = Actions.MOVE_DOWN
                    translations_needed.y -= 1
                elif roatations_needed < 0:
                    self.move = Actions.ROTATE_CCW
                    roatations_needed += 1
                elif roatations_needed > 0:
                    self.move = Actions.ROTATE_CW
                    roatations_needed -= 1
                elif translations_needed.x > 0:
                    self.move = Actions.MOVE_RIGHT
                    translations_needed.x -= 1
                elif translations_needed.x < 0:
                    self.move = Actions.MOVE_LEFT
                    translations_needed.x += 1
                else:
                    self.move = Actions.HARD_DROP
                    self.next_move = None
                    return
                self.next_move = BasicTetrisAI.Move(roatations_needed, translations_needed)

            def __repr__(self):
                return "Move(" + str(self.move) + ((", " + repr(self.next_move) + ")") if self.next_move is not None else ")")

            def __len__(self):
                return 1 if self.move == Actions.HARD_DROP else len(self.next_move) + 1

label mas_tetris_start:
    m "You want to play Tetris?"
    m "Okay!"

label mas_tetris_loop:
    # $ disable_esc()
    # $ mas_MUMURaiseShield()
    $ HKBHideButtons()
    python:
        tetris_board_bg = Image("mod_assets/tetris/grid.png")
        t_piece_1 = Image("mod_assets/tetris/piece1.png")
        t_piece_2 = Image("mod_assets/tetris/piece2.png")
        t_piece_3 = Image("mod_assets/tetris/piece3.png")
        t_piece_4 = Image("mod_assets/tetris/piece4.png")
        t_piece_5 = Image("mod_assets/tetris/piece5.png")
        t_piece_6 = Image("mod_assets/tetris/piece6.png")
        pieces = [
            t_piece_1,
            t_piece_2,
            t_piece_3,
            t_piece_4,
            t_piece_5,
            t_piece_6
        ]
    $ ui.add(mas_tetris.TetrisGameMaster(tetris_board_bg, pieces))
    $ monika_won = ui.interact()

label mas_tetris_done:
    $ enable_esc()
    $ mas_MUMUDropShield()
    $ HKBShowButtons()
    if monika_won:
        m "I win~"
    else:
        m "You win! Congratulations!"
    m "Play again?"
    menu:
        "Play again?"
        "Yes.":
            jump mas_tetris_loop
        "No.":
            if monika_won:
                m "I'll go a little easier on you next time, [player]."
                $ persistent.tetris_difficulty -= 1
            else:
                m "I'll go a little harder on you next time, [player]."
                $ persistent.tetris_difficulty += 1
    return