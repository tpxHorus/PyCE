import chess
import asyncio

from src.engine import Engine
from src.config import *


class UCI:
  def __init__(self, engine: Engine) -> None:
    self.engine = engine
  
  async def loop(self):
    while True:
      command, options = input().split(maxsplit=1)
      if command == 'uci':
        print(f"id name {ENGINE_NAME} {'.'.join(map(str, ENGINE_VERSION))}\n"
              f"id author {' '.join(ENGINE_AUTHORS)}\n"
              "uciok\n")
        
      if command == 'position' and options:
        pos, _, moves = options.partition(' moves ')
        print(pos, moves)
        self.engine.set_position(pos)
        if len(moves) > 0:
          self.engine.play_moves(moves.split())
          
      if command == 'go':
        asyncio.run(self.engine.go())
        
      if command == 'quit':
        break
        