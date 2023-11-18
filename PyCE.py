import asyncio
from src.engine import Engine
from src.uci    import UCI

if __name__ == '__main__':
  engine = Engine()
  uci = UCI(engine)
  asyncio.run(uci.loop())