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


class StockFishOpponent(Opponent):
    # TODO: complete implementation
    def __init__(self, path_to_engine):
        super().__init__()
        self.engine = Stockfish(path=path_to_engine)
        self.engine.set_fen_position(chess.Board().fen())

    def step(self, action: str) -> str:
        assert action is not None, 'Invalid action passed'

        if action != 'white begins':
            self.engine.make_moves_from_current_position([action])

        move = self.engine.get_best_move()
        self.engine.make_moves_from_current_position([move])

        return move
