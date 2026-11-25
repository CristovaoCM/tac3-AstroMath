import os
from source.modules.engine import engine
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    
    # Executa o motor de jogo    
    engine.run()