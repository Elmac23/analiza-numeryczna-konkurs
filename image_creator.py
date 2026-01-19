# Tworzy obraz PNG z krzywymi spline na podstawie danych z pliku
# Czyta punkty, rysuje krzywe i zapisuje wynikowy obraz

import matplotlib.pyplot as plt
from nifs3 import NIFS3, compute


class ImageCreator:
    # Rysuje krzywe i tworzy obraz PNG
    def __init__(self, input_path: str = "konkurs-352890-dane.txt", output_path: str = "konkurs-352890.png",
                 canvas_width: float = 1732.0, canvas_height: float = 363.0,
                 color_palette=None, line_width: float = 0.75):
        # Ustaw ścieżki, rozmiar płótna i paletę kolorów
        self.input_path = input_path
        self.output_path = output_path
        self.canvas_width = float(canvas_width)
        self.canvas_height = float(canvas_height)
        self.color_palette = color_palette or [
            "#14e914", '#003737', '#FF6B6B', "#4915D6", "#E6289D", '#FFA07A', "#DF5900", '#F7DC6F', '#BB8FCE', '#85C1E2'
        ]
        self.line_width = float(line_width)
        self.fig = None
        self.ax = None

    def _setup_canvas(self):
        # Przygotuj płótno bez osi i marginesów
        self.fig = plt.figure()
        self.fig.set_size_inches(self.canvas_width / self.canvas_height, 1, forward=False)
        self.ax = plt.Axes(self.fig, [0., 0., 1., 1.])
        self.ax.set_axis_off()
        self.fig.add_axes(self.ax)
        plt.xlim(0, self.canvas_width)
        plt.ylim(self.canvas_height, 0)
        plt.gca().set_aspect('equal')

    def _draw_curves(self):
        # Wczytaj dane z pliku i narysuj wszystkie krzywe
        curve_index = 0
        with open(self.input_path, encoding='utf-16') as data_file:
            for raw_line in data_file:
                parsed_line = raw_line.split("[")
                if len(parsed_line) < 4:
                    continue
                parsed_line = [list(map(float, segment[:segment.find(']')].split(','))) for segment in parsed_line if "]" in segment]
                coords_x, coords_y, param_t, param_u = parsed_line

                coeff_ax, coeff_bx, coeff_cx, coeff_dx = NIFS3(param_t, coords_x)
                coeff_ay, coeff_by, coeff_cy, coeff_dy = NIFS3(param_t, coords_y)

                spline_x = [compute(u_val, param_t, coeff_ax, coeff_bx, coeff_cx, coeff_dx) for u_val in param_u]
                spline_y = [compute(u_val, param_t, coeff_ay, coeff_by, coeff_cy, coeff_dy) for u_val in param_u]

                current_color = self.color_palette[curve_index % len(self.color_palette)]
                plt.plot(spline_x, spline_y, linewidth=self.line_width, color=current_color)
                curve_index += 1

    def save(self):
        # Zapisz aktualny obraz do PNG
        plt.savefig(self.output_path, dpi=self.canvas_height, format="png", pil_kwargs={"quality": 100})

    def show(self):
        # Pokaż obraz w podglądzie
        plt.show()

    def run(self):
        self._setup_canvas()
        self._draw_curves()
        self.save()
        self.show()


# Utworzenie obiektu i uruchomienie procesu rysowania
_creator = ImageCreator()
_creator.run()