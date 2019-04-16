init python:
    class mas_TetrisGame(renpy.Displayable):
        def __init__(self, board_image, piece_images, **kwargs):
            # Pass additional properties on to the renpy.Displayable
            # constructor.
            super(mas_TetrisGame, self).__init__(**kwargs)

            self.player_board = mas_TetrisBoard(board_image, piece_images)
            self.monika_board = mas_TetrisBoard(board_image, piece_images)
        
        def event(self, ev, x, y, st):
            self.monika_board.event(ev, x, y, st)
            self.player_board.event(ev, x, y, st)
            if self.player_board.game_over:
                return True
            elif self.monika_board.game_over:
                return False
            else:
                raise renpy.IgnoreEvent()

    class mas_TetrisBoardRenderer(renpy.Displayable):
        def __init__(self, board_image, piece_images, **kwargs):
            # Pass additional properties on to the renpy.Displayable
            # constructor.
            super(mas_TetrisBoard, self).__init__(**kwargs)

            self.board_render = renpy.render(board_image)
            self.piece_renders = []
            for piece in piece_images:
                piece_renders.append(renpy.render(piece))

            self.game_over = False

        def render(self, width, height, st, at):
            for x, row in enumerate(self.board.grid):
                for y, value in enumerate(row):
                    pass
        
        def event(self, ev, x, y, st):
            pass