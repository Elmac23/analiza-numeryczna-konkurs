# Optymalizuje punkty na krzywych: usuwa duplikaty i współliniowe
# Czyta z "points.txt" i zapisuje wynik do "konkurs-352890-dane.txt"
from nifs3 import NIFS3, compute


class PointOptimiser:
    # Odpowiada za optymalizację listy parametrów u i zapis wyniku
    def __init__(self, input_path: str = "points.txt", output_path: str = "konkurs-352890-dane.txt"):
        self.input_path = input_path
        self.output_path = output_path

    def optimise(self):
        with open(self.input_path, encoding='utf-16') as input_file, open(self.output_path, "w", encoding='utf-16') as output_file:
            for raw_line in input_file:
                parsed_line = raw_line.split("[")
                if len(parsed_line) < 4:
                    continue
                parsed_line = [list(map(float, segment[:segment.find(']')].split(','))) for segment in parsed_line if "]" in segment]
                coords_x, coords_y, param_t, param_u = parsed_line

                filtered_u = []
                rendered_pixels = set()
                coeff_ax, coeff_bx, coeff_cx, coeff_dx = NIFS3(param_t, coords_x)
                coeff_ay, coeff_by, coeff_cy, coeff_dy = NIFS3(param_t, coords_y)
                for u_val in param_u:
                    #Liczymy punkt na krzywej
                    pos_x = compute(u_val, param_t, coeff_ax, coeff_bx, coeff_cx, coeff_dx)
                    pos_y = compute(u_val, param_t, coeff_ay, coeff_by, coeff_cy, coeff_dy)
                    if pos_x == None or pos_y == None:
                        continue
                    pixel_coord = (round(pos_x), round(pos_y))
                    # Usuwamy duplikaty pikseli
                    if pixel_coord not in rendered_pixels:
                        rendered_pixels.add(pixel_coord)
                        filtered_u.append(u_val)
                # Usuwamy punkty współliniowe
                collinear_pixels = set()
                for p1_x, p1_y in rendered_pixels:
                    for p2_x, p2_y in rendered_pixels:
                        if p1_x == p2_x and p1_y == p2_y:
                            continue
                        if p1_x > p2_x:
                            continue
                        if p1_x == p2_x:
                            min_y, max_y = min(p1_y, p2_y), max(p1_y, p2_y)
                            for mid_y in range(min_y + 1, max_y):
                                mid_pixel = (p1_x, mid_y)
                                if mid_pixel not in rendered_pixels:
                                    break
                                collinear_pixels.add(mid_pixel)
                        else:
                            slope = (p2_y - p1_y) / (p2_x - p1_x)
                            current_mid = (p1_x + 1, p1_y + slope)
                            while current_mid < (p2_x, p2_y):
                                next_mid = (round(current_mid[0] + 1), round(current_mid[1] + slope))
                                if current_mid in rendered_pixels and next_mid in rendered_pixels:
                                    collinear_pixels.add(current_mid)
                                else:
                                    break
                                current_mid = next_mid

                optimised_u = []
                final_pixels = set()
                for u_val in filtered_u:
                    pos_x = compute(u_val, param_t, coeff_ax, coeff_bx, coeff_cx, coeff_dx)
                    pos_y = compute(u_val, param_t, coeff_ay, coeff_by, coeff_cy, coeff_dy)
                    if pos_x == None or pos_y == None:
                        continue
                    pixel_coord = (int(pos_x), int(pos_y))
                    if pixel_coord not in collinear_pixels:
                        final_pixels.add(pixel_coord)
                        optimised_u.append(u_val)

                output_file.write("x:= " + str([float(val) for val in coords_x]) + ", ")
                output_file.write("y:= " + str([float(val) for val in coords_y]) + ", ")
                output_file.write("t:= " + str([float(val) for val in param_t]) + ", ")
                output_file.write("u:= " + str([float(val) for val in optimised_u]) + "\r\n")


# Utworzenie obiektu i wykonanie optymalizacji
_optimiser = PointOptimiser()
_optimiser.optimise()