# Generuje proste podsumowanie po optymalizacji: liczy rekordy i elementy
# Czyta dane z pliku i zapisuje wynik do pliku podsumowania


class SummaryGenerator:
    # Tworzy krótkie podsumowanie: liczy rekordy i łączną liczbę elementów
    def __init__(self, points_file: str = "konkurs-352890-dane.txt", out_file: str = "konkurs-352890-podsumowanie.txt"):
        self.points_file = points_file
        self.out_file = out_file

    def _find_bracket_content(self, s, start_pos):
        # Zwraca zawartość pierwszych nawiasów [] od podanej pozycji
        i = s.find('[', start_pos)
        if i == -1:
            return None, -1
        j = i + 1
        depth = 1
        while j < len(s) and depth > 0:
            if s[j] == '[':
                depth += 1
            elif s[j] == ']':
                depth -= 1
            j += 1
        if depth != 0:
            return None, -11
        return s[i+1:j-1], j

    def _split_items(self, list_text):
        # Dzieli tekst po przecinkach i usuwa puste wpisy
        parts = list_text.split(',')
        items = [p.strip() for p in parts if p.strip() != '']
        return items

    def _parse_and_count(self, text):
        # Szuka rekordów i zlicza elementy x, y, t, u w każdym z nich
        pos = 0
        records = 0
        total_t = 0
        total_sizes = 0
        while True:
            x_idx = text.find('x:=', pos)
            if x_idx == -1:
                break
            x_content, p = self._find_bracket_content(text, x_idx)
            if x_content is None:
                break
            x_items = self._split_items(x_content)

            y_idx = text.find('y:=', p)
            if y_idx == -1:
                break
            y_content, p2 = self._find_bracket_content(text, y_idx)
            if y_content is None:
                break
            y_items = self._split_items(y_content)

            t_idx = text.find('t:=', p2)
            if t_idx == -1:
                break
            t_content, p3 = self._find_bracket_content(text, t_idx)
            if t_content is None:
                break
            t_items = self._split_items(t_content)

            u_idx = text.find('u:=', p3)
            if u_idx == -1:
                break
            u_content, p4 = self._find_bracket_content(text, u_idx)
            if u_content is None:
                break
            u_items = self._split_items(u_content)

            records += 1
            total_t += len(t_items)
            total_sizes += len(x_items) + len(y_items) + len(t_items) + len(u_items)

            pos = p4

        used_nifs3 = records
        return used_nifs3, total_t, total_sizes

    def generate(self):
        text = ''
        try:
            f = open(self.points_file, 'r', encoding='utf-8', errors='ignore')
            text = f.read()
            f.close()
        except Exception:
            text = ''
        used_nifs3, total_t, total_sizes = self._parse_and_count(text)
        if used_nifs3 == 0 and text.strip() != '':
            try:
                f = open(self.points_file, 'r', encoding='utf-16', errors='ignore')
                text = f.read()
                f.close()
                used_nifs3, total_t, total_sizes = self._parse_and_count(text)
            except Exception:
                pass
        try:
            out = open(self.out_file, 'w', encoding='utf-8')
            out.write(f"{used_nifs3}, {total_t}, {total_sizes}")
            out.close()
        except Exception:
            pass


# Utworzenie obiektu i wygenerowanie podsumowania
_summary = SummaryGenerator()
_summary.generate()
