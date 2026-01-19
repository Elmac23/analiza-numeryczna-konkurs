# Pomocnicze funkcje do obliczeń NIFS3 i interpolacji
# Wyznaczają współczynniki spline i liczą wartości dla zadanych parametrów

def NIFS3(param_t, data_values):
    # Liczy współczynniki a, b, c, d dla kolejnych odcinków spline
    segment_count = len(data_values) - 1
    intervals = [param_t[idx] - param_t[idx-1] for idx in range(1, segment_count+1)]
    delta_k = [0 for idx in range(segment_count)]
    diagonal = [1 for idx in range(segment_count+1)]
    upper_diag = [0 for idx in range(segment_count)]
    solution_q = [0 for idx in range(segment_count+1)]
    
    for idx in range(1, segment_count):
        delta_k[idx] = (3 / intervals[idx]) * (data_values[idx + 1] - data_values[idx]) - (3 / intervals[idx - 1]) * (data_values[idx] - data_values[idx - 1])
    
    for idx in range(1, segment_count):
        diagonal[idx] = 2 * (param_t[idx + 1] - param_t[idx - 1]) - intervals[idx - 1] * upper_diag[idx - 1]
        upper_diag[idx] = intervals[idx] / diagonal[idx]
        solution_q[idx] = (delta_k[idx] - intervals[idx - 1] * solution_q[idx - 1]) / diagonal[idx]
    
    coeff_c = [0 for idx in range(segment_count+1)]
    coeff_b = [0 for idx in range(segment_count)]
    coeff_d = [0 for idx in range(segment_count)]
    coeff_a = [0 for idx in range(segment_count)]

    for seg_idx in range(segment_count - 1, -1, -1):
        coeff_a[seg_idx] = data_values[seg_idx]
        coeff_c[seg_idx] = solution_q[seg_idx] - upper_diag[seg_idx] * coeff_c[seg_idx + 1]
        coeff_b[seg_idx] = (data_values[seg_idx + 1] - data_values[seg_idx]) / intervals[seg_idx] - intervals[seg_idx] * (coeff_c[seg_idx + 1] + 2 * coeff_c[seg_idx]) / 3
        coeff_d[seg_idx] = (coeff_c[seg_idx + 1] - coeff_c[seg_idx]) / (3 * intervals[seg_idx])
    
    return coeff_a, coeff_b, coeff_c, coeff_d

def compute(param_value, knot_points, coeff_a, coeff_b, coeff_c, coeff_d):
    # Zwraca wartość spline dla parametru u lub None poza zakresem
    for segment_idx in range(len(knot_points) - 1):
        if knot_points[segment_idx] <= param_value < knot_points[segment_idx + 1]:
            time_delta = param_value - knot_points[segment_idx]
            return coeff_a[segment_idx] + coeff_b[segment_idx] * time_delta + coeff_c[segment_idx] * time_delta**2 + coeff_d[segment_idx] * time_delta**3
    return None