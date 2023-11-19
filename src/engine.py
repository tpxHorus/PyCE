import chess
import numpy as np

def safemethod(func):
  def wrapper(*args, **kwargs):
    try:
      func(*args, **kwargs)
      return True
    finally:
      return False
  return wrapper


def relativer(turn, color):
  return -1 if (turn ^ color) else 1


PIECE_VALUES = np.array([None, 100, 290, 330, 450, 850, 99999])

PAWN_PST = np.array([
      0,   0,   0,   0,   0,   0,  0,   0,
     98, 134,  61,  95,  68, 126, 34, -11,
     -6,   7,  26,  31,  65,  56, 25, -20,
    -14,  13,   6,  21,  23,  12, 17, -23,
    -27,  -2,  -5,  12,  17,   6, 10, -25,
    -26,  -4,  -4, -10,   3,   3, 33, -12,
    -35,  -1, -20, -23, -15,  24, 38, -22,
      0,   0,   0,   0,   0,   0,  0,   0,
])

KNIGHT_PST = np.array([
    -167, -89, -34, -49,  61, -97, -15, -107,
     -73, -41,  72,  36,  23,  62,   7,  -17,
     -47,  60,  37,  65,  84, 129,  73,   44,
      -9,  17,  19,  53,  37,  69,  18,   22,
     -13,   4,  16,  13,  28,  19,  21,   -8,
     -23,  -9,  12,  10,  19,  17,  25,  -16,
     -29, -53, -12,  -3,  -1,  18, -14,  -19,
    -105, -21, -58, -33, -17, -28, -19,  -23,
])

BISHOP_PST = np.array([
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
     -4,   5,  19,  50,  37,  37,   7,  -2,
     -6,  13,  13,  26,  34,  12,  10,   4,
      0,  15,  15,  15,  14,  27,  18,  10,
      4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -14, -21, -13, -12, -39, -21,
])

ROOK_PST = np.array([
     32,  42,  32,  51, 63,  9,  31,  43,
     27,  32,  58,  62, 80, 67,  26,  44,
     -5,  19,  26,  36, 17, 45,  61,  16,
    -24, -11,   7,  26, 24, 35,  -8, -20,
    -36, -26, -12,  -1,  9, -7,   6, -23,
    -45, -25, -16, -17,  3,  0,  -5, -33,
    -44, -16, -20,  -9, -1, 11,  -6, -71,
    -19, -13,   1,  17, 16,  7, -37, -26,
])


QUEEN_PST = np.array([
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
     -1, -18,  -9,  10, -15, -25, -31, -50,
])

KING_PST = np.array([
    -65,  23,  16, -15, -56, -34,   2,  13,
     29,  -1, -20,  -7,  -8,  -4, -38, -29,
     -9,  24,   2, -16, -20,   6,  22, -22,
    -17, -20, -12, -27, -30, -25, -14, -36,
    -49,  -1, -27, -39, -46, -44, -33, -51,
    -14, -14, -22, -46, -44, -30, -15, -27,
      1,   7,  -8, -64, -43, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14,
])

PST = [
  None,
  PAWN_PST,
  KNIGHT_PST,
  BISHOP_PST,
  ROOK_PST, 
  QUEEN_PST,
  KING_PST
]

MAX_DEPTH = 20

class Engine:
  def __init__(self, pos: str | None = chess.STARTING_FEN) -> None:
    self.set_position(pos)
  
  @safemethod
  def set_position(self, pos: str) -> bool:
    if pos == 'startpos':
      pos = chess.STARTING_FEN
    self.pos = chess.Board(pos)
    self.transposition_table = {}
    
  def play_moves(self, moves: list[str]):
    for move in moves:
      self.play_move(move)
  
  @safemethod
  def play_move(self, move: str):
    self.pos.push_uci(move)
  
  async def go(self):
    evaluation = self.evaluate()
    for depth in range(MAX_DEPTH):
      for move in self.pos.legal_moves:
        delta = self.eval_delta(move)
        self.pos.push(move)
        print(f"{move.uci()} on depth {depth+1}: {self.negamax(depth, -evaluation-delta)} (eval delta: {delta})")
        self.pos.pop()

  def negamax(self, depth, evaluation):
    if depth == 0 or self.pos.is_game_over():
      return -evaluation

    value = -float('inf')
    for move in self.pos.legal_moves:
      delta = self.eval_delta(move)
      self.pos.push(move)
      value = max(value, -self.negamax(depth-1, -evaluation-delta))
      self.pos.pop()
    
    return value
  
  def evaluate(self):
    material = 0
    mobility = 0

    for piece_type in chess.PIECE_TYPES:
      for color in chess.COLORS:
        bits = self.pos.pieces_mask(piece_type, color)
        if color:
          bits = chess.flip_vertical(bits)
        material += bits.bit_count() * PIECE_VALUES[piece_type] * relativer(self.pos.turn, color)
        bits = np.unpackbits(np.array([bits], dtype=np.uint64).view(np.uint8))
        mobility += PST[piece_type][bits.astype(bool)].sum() * relativer(self.pos.turn, color)

    return material + mobility
  

  def eval_delta(self, move: chess.Move):
    from_sq = move.from_square
    to_sq = move.to_square
    
    if self.pos.turn:
      from_sq = chess.square_mirror(from_sq)
      to_sq = chess.square_mirror(to_sq)

    piece_type = self.pos.piece_type_at(move.from_square)
    delta = PST[piece_type][to_sq] - PST[piece_type][from_sq]

    if self.pos.is_castling(move):
      if self.pos.is_queenside_castling(move):
        to_sq -= 3
        from_sq -= 2
      return delta + PST[chess.ROOK][to_sq+1] - PST[chess.ROOK][from_sq+1]

    if self.pos.is_capture(move):
      if self.pos.is_en_passant(move):
        return delta + PIECE_VALUES[self.pos.piece_type_at(move.to_square + (-8 if self.pos.turn else 8))]
      delta += PIECE_VALUES[self.pos.piece_type_at(move.to_square)]

    if move.promotion is not None:
      delta += PIECE_VALUES[move.promotion] - 100

    return delta