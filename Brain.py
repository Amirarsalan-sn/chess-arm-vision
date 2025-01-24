from stockfish import Stockfish
import chess


class Opponent:
    def __init__(self):
        pass

    def step(self, action: str) -> str:
        """
        VERY IMPORTANT TO CONSIDER THAT ACTIONS ARE IN UCI FORM AND THE RETURNED ACTION MUST ALSO BE IN UCI FORM.
        :param action:
        :return:
        """
        pass

    def is_legal(self, action: str) -> bool:
        """
        Checks whether the action is valid or not.
        :param action:
        :return:
        """
        pass

    def is_en_passant(self, action: str) -> bool:
        """
        Checks whether an action is en passant or not.
        :param action:
        :return:
        """
        pass


class StockFishOpponent(Opponent):
    # TODO: complete implementation
    def __init__(self, path_to_engine):
        super().__init__()
        self.engine = Stockfish(path=path_to_engine)
        self.engine.set_fen_position(chess.Board().fen())
        self.board = chess.Board()

    def step(self, action: str) -> tuple[str, int] or tuple[None, int]:
        assert action is not None, 'Invalid action passed'

        if action != 'white begins':
            self.engine.make_moves_from_current_position([action])
            board_move = chess.Move.from_uci(action)
            self.board.push(board_move)

        if self.board.outcome() is not None:
            if self.board.outcome().result() == '1-0':
                return None, 1
            elif self.board.outcome().result() == '0-1':
                return None, -1
            else:
                return None, 0

        move = self.engine.get_best_move()
        board_move = chess.Move.from_uci(move)
        self.board.push(board_move)
        self.engine.make_moves_from_current_position([move])

        if self.board.outcome() is not None:
            if self.board.outcome().result() == '1-0':
                return move, 1
            elif self.board.outcome().result() == '0-1':
                return move, -1
            else:
                return move, 0

        return move, 2

    def is_legal(self, action: str) -> bool:
        return chess.Move.from_uci(action) in self.board.legal_moves

    def is_en_passant(self, action: str) -> bool:
        if self.is_legal(action):
            return self.board.is_en_passant(chess.Move.from_uci(action))
        else:
            return False
