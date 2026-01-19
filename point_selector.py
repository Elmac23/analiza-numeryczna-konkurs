#Program pozwalający nam na manualne tworzenie punktów do naszego NIFS3
#Gdy skończymy dodawać punkty, program automatycznie doda je do pliku "points.txt"
import matplotlib.pyplot as plt
from nifs3 import NIFS3, compute
import numpy as np
from math import sqrt

BACKGROUND_IMAGE = "background.png"
SAMPLE_COUNT = 600

class PointSelector:
    # Prosty edytor punktów: dodaje/usuwa punkty, pokazuje krzywą, zapisuje dane
    def __init__(self, bg_path):
        # Ustaw ścieżkę do tła i przygotuj listę punktów
        self.bg_path = bg_path
        self.control_pts = []

    def render_curve(self, pts):
        # Rysuje przybliżoną krzywą na podstawie punktów kontrolnych
        if len(pts) < 2: 
            return
        
        coords_x = [pt[0] for pt in pts]
        coords_y = [pt[1] for pt in pts]
        
        # Oblicz parametry t wedlug długości odcinkow
        cumulative_dist = [0] * len(coords_x)
        total_length = 0
        for idx in range(1, len(coords_x)):
            segment_len = sqrt((coords_x[idx] - coords_x[idx-1])**2 + (coords_y[idx] - coords_y[idx-1])**2)
            cumulative_dist[idx] = cumulative_dist[idx-1] + segment_len
            total_length += segment_len
        
        param_t = [cumulative_dist[idx] / total_length for idx in range(len(coords_x))]
        param_u = np.linspace(0, 1, SAMPLE_COUNT)

        # Oblicz współczynniki i wartości spline
        coeff_ax, coeff_bx, coeff_cx, coeff_dx = NIFS3(param_t, coords_x)
        coeff_ay, coeff_by, coeff_cy, coeff_dy = NIFS3(param_t, coords_y)

        curve_x = [compute(u, param_t, coeff_ax, coeff_bx, coeff_cx, coeff_dx) for u in param_u]
        curve_y = [compute(u, param_t, coeff_ay, coeff_by, coeff_cy, coeff_dy) for u in param_u]
        plt.plot(curve_x, curve_y, linewidth=1, color='blue')

    def handle_mouse_click(self, event):
        # Obsługa kliknięć: LPM dodaje punkt, PPM usuwa ostatni punkt
        if event.button is plt.MouseButton.LEFT and event.xdata is not None and event.ydata is not None:
            click_x, click_y = event.xdata, event.ydata
            self.control_pts.append((click_x, click_y))
            self.refresh_display()

        if event.button is plt.MouseButton.RIGHT and event.xdata is not None and event.ydata is not None:
            if len(self.control_pts) > 0:
                self.control_pts.pop()
                self.refresh_display()

    def handle_keypress(self, event):
        # Obsługa klawiszy: "c" czyści plik z punktami
        if event.key == 'c':
            self.reset_output_file()
    
    def reset_output_file(self):
        # Wyczyść plik points.txt
        with open("points.txt", "w", encoding='utf-16') as output_file:
            output_file.write("")
        print("Plik points.txt został wyczyszczony!")

    def refresh_display(self):
        # Odśwież widok
        self.canvas_fig.canvas.toolbar.push_current()
        plt.cla()
        self.canvas_fig.canvas.toolbar.back()
        bg_image = plt.imread(self.bg_path)
        plt.imshow(bg_image)
        plt.title('LPM - Dodanie punktu, PPM - Usunięcie ostatniego punktu, C - Wyczyść points.txt')
        for idx, pt in enumerate(self.control_pts):
            plt.scatter(pt[0], pt[1], color='blue', s=1)
            plt.text(pt[0], pt[1], str(idx), fontsize=5)
        self.render_curve(self.control_pts)
        plt.draw()

    def run_editor(self):
        # Uruchom interfejs do wybierania punktów
        bg_image = plt.imread(self.bg_path)
        self.canvas_fig, self.canvas_ax = plt.subplots()
        self.canvas_ax.imshow(bg_image)
        self.canvas_ax.set_title('LPM - Dodanie punktu, PPM - Usunięcie ostatniego punktu, C - Wyczyść points.txt')

        click_handler = self.canvas_fig.canvas.mpl_connect('button_press_event', self.handle_mouse_click)
        self.canvas_fig.canvas.mpl_connect('key_press_event', self.handle_keypress)
        plt.show()
        self.canvas_fig.canvas.mpl_disconnect(click_handler)

    def save_to_file(self):
        # Zapisuje aktualne punkty i parametry do pliku points.txt
        if len(self.control_pts) == 0:
            return
        
        coords_x = [pt[0] for pt in self.control_pts]
        coords_y = [pt[1] for pt in self.control_pts]
        
        # Oblicz parametry t oraz listę u do zapisu
        cumulative_dist = [0] * len(coords_x)
        total_length = 0
        for idx in range(1, len(coords_x)):
            segment_len = sqrt((coords_x[idx] - coords_x[idx-1])**2 + (coords_y[idx] - coords_y[idx-1])**2)
            cumulative_dist[idx] = cumulative_dist[idx-1] + segment_len
            total_length += segment_len
        
        param_t = [cumulative_dist[idx] / total_length for idx in range(len(coords_x))]
        param_u = np.linspace(0, 1, SAMPLE_COUNT)
        
        with open("points.txt", "a", encoding='utf-16') as output_file:
            output_file.write("x:= " + str([float(val) for val in coords_x]) + ", ")
            output_file.write("y:= " + str([float(val) for val in coords_y]) + ", ")
            output_file.write("t:= " + str([float(val) for val in param_t]) + ", ")
            output_file.write("u:= " + str([float(val) for val in param_u]) + "\r\n")

editor = PointSelector(BACKGROUND_IMAGE)
editor.run_editor()
editor.save_to_file()
