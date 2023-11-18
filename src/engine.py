import chess

def noexceptmethod(func):
  def wrapper(*args, **kwargs):
    try:
      func(*args, **kwargs)
      return True
    finally:
      return False
  return wrapper


class Engine:
  def __init__(self, pos: str | None = chess.STARTING_FEN) -> None:
    self.set_position(pos)
  
  @noexceptmethod
  def set_position(self, pos: str) -> bool:
    if pos == 'startpos':
      pos = chess.STARTING_FEN
    self.current_pos = chess.Board(pos)
    
  def play_moves(self, moves: list[str]):
    for move in moves:
      self.play_move(move)
  
  @noexceptmethod
  def play_move(self, move: str):
      self.current_pos.push_uci(move)
    
  async def go(self):
    pass