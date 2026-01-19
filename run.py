#Program który na podstawie pliku points.txt:
#Optymalizuje punkty z pliku points.txt i generuje plik konkurs-352890-dane.txt
#Tworzy obraz PNG z krzywymi spline i zapisuje go jako konkurs-352890.png
#Tworzy podsumowanie danych w pliku konkurs-352890-podsumowanie.txt

from point_optimiser import PointOptimiser
from image_creator import ImageCreator
from summary import SummaryGenerator

_optimiser = PointOptimiser()
_optimiser.optimise()
_creator = ImageCreator()
_creator.run()
_summary = SummaryGenerator()
_summary.generate()