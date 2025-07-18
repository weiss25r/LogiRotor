import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.courier import Courier
courier = Courier()
courier.run_simulation()
print("Simulazione completata e grafico salvato con successo")