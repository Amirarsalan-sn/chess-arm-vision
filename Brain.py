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

    def get_best_action(self) -> str:
        pass

    def apply_action(self, action: str):
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

    def is_check(self):
        """
        checks whether the current side to move is in check.
        :return:
        """
        pass

    def set_fen(self, fen):
        pass

    def outcome(self):
        pass

    def close(self):
        """
        de-allocate the allocated resources
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

    def step(self, action: str) -> tuple[str, int, bool] or tuple[None, int, bool]:
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

        opponent_checked = self.is_check()

        move = self.engine.get_best_move()
        board_move = chess.Move.from_uci(move)
        en_passant = self.is_en_passant(move)
        self.board.push(board_move)
        self.engine.make_moves_from_current_position([move])

        if self.board.outcome() is not None:
            if self.board.outcome().result() == '1-0':
                return move, 1, en_passant
            elif self.board.outcome().result() == '0-1':
                return move, -1, en_passant
            else:
                return move, 0, en_passant

        player_checked = self.is_check()
        stat_code = 2

        if player_checked and opponent_checked:
            stat_code = 5
        elif player_checked:
            stat_code = 3
        elif opponent_checked:
            stat_code = 4

        return move, stat_code, en_passant

    def get_best_action(self) -> str:
        return self.engine.get_best_move()

    def apply_action(self, action: str):
        self.engine.make_moves_from_current_position([action])
        action = chess.Move.from_uci(action)
        self.board.push(action)

    def is_legal(self, action: str) -> bool:
        return chess.Move.from_uci(action) in self.board.legal_moves

    def is_en_passant(self, action: str) -> bool:
        if self.is_legal(action):
            return self.board.is_en_passant(chess.Move.from_uci(action))

        else:
            return False

    def is_check(self):
        return self.board.is_check()

    def outcome(self):
        outcome = self.board.outcome()
        if outcome is not None:
            return self.board.outcome().result()
        return self.board.outcome()

    def close(self):
        del self.engine
        print('stockfish released.')

    def set_fen(self, fen):
        self.engine.set_fen_position(fen)
        self.board.set_fen(fen)
