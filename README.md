# Projekt NIFS3 - Analiza Numeryczna

System do interpolacji krzywych przy użyciu naturalnych funkcji sklejanych trzeciego stopnia (kubicznych spline'ów).

## 📚 Dokumentacja

**Pełna dokumentacja projektu znajduje się w pliku [`dokumentacja.html`](./dokumentacja.html)**

Aby otworzyć dokumentację, wystarczy otworzyć plik `dokumentacja.html` w przeglądarce internetowej.

## 🚀 Szybki Start

### Wymagania
- Python 3.6+
- matplotlib
- numpy

### Instalacja
```bash
pip install matplotlib numpy
```

### Podstawowe Użycie

1. **Tworzenie krzywych** - Uruchom edytor punktów:
```bash
python point_selector.py
```

2. **Generowanie obrazu** - Po utworzeniu punktów:
```bash
python run.py
```

## 📖 Co Znajdziesz w Dokumentacji

Dokumentacja HTML zawiera:

- ✅ **Teorię matematyczną** - szczegółowe wyjaśnienie algorytmu NIFS3
- ✅ **Opis algorytmu** - implementacja krok po kroku
- ✅ **Dokumentację modułów** - pełny opis wszystkich funkcji
- ✅ **Instrukcję użycia** - kompletny przewodnik
- ✅ **Diagramy przepływu** - architektura systemu
- ✅ **Przykłady kodu** - z komentarzami

## 📁 Struktura Projektu

```
├── nifs3.py                  # Algorytm NIFS3
├── point_selector.py         # Edytor punktów
├── point_optimiser.py        # Optymalizator
├── image_creator.py          # Generator obrazów
├── summary.py                # Generator statystyk
├── run.py                    # Główny skrypt
├── dokumentacja.html         # 📚 PEŁNA DOKUMENTACJA
├── algorytm-momenty-NIFS3.pdf    # Dokumentacja algorytmu
└── twierdzenie-NIFS3.pdf         # Teoria matematyczna
```

## 🎯 Kluczowe Cechy

- **Matematycznie precyzyjny** algorytm NIFS3
- **Gładkie krzywe** z ciągłością C²
- **Optymalizacja punktów** (redukcja 30-70%)
- **Interaktywny edytor** punktów kontrolnych
- **Profesjonalna dokumentacja** w HTML

## 📝 Licencja

Projekt stworzony w ramach konkursu z analizy numerycznej.

---

**💡 Tip:** Zacznij od przeczytania `dokumentacja.html` aby zrozumieć teorię i praktyczne aspekty projektu!
