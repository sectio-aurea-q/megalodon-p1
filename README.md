<div align="center">

# 🦢 BLACK SWAN

### Die deutsche Programmiersprache

**Programmiere auf Deutsch. Transpiliert zu Python. Läuft im Browser.**

[![Live Demo](https://img.shields.io/badge/▶_Live_Demo-black?style=for-the-badge&logo=github&logoColor=white)](https://SANDQEEN1111.github.io/black-swan/)
[![License: MIT](https://img.shields.io/badge/License-MIT-f43f5e?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/v16-OMEGA-38bdf8?style=for-the-badge)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-willkommen-2dd4bf?style=for-the-badge)]()

<br>

<!-- Screenshot einfügen: -->
<!-- ![Black Swan IDE](screenshots/hero.png) -->

**Black Swan** ist eine vollständige Programmierumgebung, in der du auf Deutsch programmierst. Jeder Befehl, jede Funktion, jede Fehlermeldung — alles auf Deutsch. Dein Code transpiliert 1:1 zu Python. Wer Black Swan beherrscht, kann Python.

[Live Demo →](https://SANDQEEN1111.github.io/black-swan/) · [Dokumentation](#-syntax) · [Mitmachen](#-mitmachen)

</div>

---

## Was ist das?

```python
# Das ist Black Swan:
für i in bereich(1, 11):
    wenn i % 2 == 0:
        drucke(zeichenkette(i) + " ist gerade")
    sonst:
        drucke(zeichenkette(i) + " ist ungerade")
```

```python
# Das ist das äquivalente Python:
for i in range(1, 11):
    if i % 2 == 0:
        print(str(i) + " ist gerade")
    else:
        print(str(i) + " ist ungerade")
```

Kein Englisch. Keine Fremdwörter. **Echtes Programmieren auf Deutsch** — mit voller IDE, Live-Canvas, Animationen, 3D, Physik, KI und mehr.

---

## ✨ 12 Features — Null Abhängigkeiten

| Feature | Beschreibung | Beispiel |
|---------|-------------|----------|
| 🐢 **Schildkröte** | Turtle-Grafik wie Logo | `schildkröte.vorwärts(100)` |
| 🔄 **Animation** | 60fps Render-Loop | `funktion zeichne():` |
| 🖱 **Maus-Interaktion** | Mausposition & Klicks | `maus_x, maus_y, maus_gedrückt` |
| 🔊 **Sound** | Synthesizer & Noten | `spiele_note("C4", 0.5)` |
| 🤖 **KI-Assistent** | Code-Generierung per Beschreibung | „Zeichne ein Sonnensystem" |
| 🎤 **Spracheingabe** | Deutsch sprechen → Code | Spracherkennung → Code |
| 🧊 **3D-Szenen** | Three.js mit deutscher API | `würfel_3d(0, 1, 0, 2, "#f00")` |
| 🌐 **WebGL Shader** | GLSL Fragment-Shader | `shader(glsl_code)` |
| ⚛️ **Physik-Engine** | Schwerkraft, Kollision, Reibung | `schwerkraft(0.5)` |
| 🎭 **Partikel-System** | Explosionen, Regen, Effekte | `partikel_explosion(x, y)` |
| 🎮 **Game Engine** | Tastatur, Spielobjekte, Kollision | `taste("links")` |
| 👥 **Multiplayer** | Geteilter Zustand zwischen Spielern | `mehrspieler_senden("pos", x)` |

Plus: **KI-Training** (k-NN), **Webcam-Tracking**, **Live-Debugger**, **KI-Tutor**, **Python-Ansicht**.

---

## 🚀 Sofort starten

### Option 1: Browser (keine Installation)

**[→ Live Demo öffnen](https://SANDQEEN1111.github.io/black-swan/)**

### Option 2: Lokal

```bash
git clone https://github.com/SANDQEEN1111/black-swan.git
cd black-swan
# Einfach index.html im Browser öffnen — fertig!
```

### Option 3: In eigenem React-Projekt

```bash
npm create vite@latest mein-projekt -- --template react
cd mein-projekt
cp pfad/zu/black-swan-v16.jsx src/BlackSwan.jsx
# In App.jsx importieren:
# import BlackSwan from './BlackSwan'
npm run dev
```

---

## 📖 Syntax

### Grundlagen

| Black Swan | Python | Bedeutung |
|-----------|--------|-----------|
| `wenn` | `if` | Bedingung |
| `sonst_wenn` | `elif` | Weitere Bedingung |
| `sonst` | `else` | Sonst |
| `für ... in` | `for ... in` | Schleife |
| `solange` | `while` | Solange-Schleife |
| `funktion` | `def` | Funktion definieren |
| `zurückgeben` | `return` | Rückgabe |
| `klasse` | `class` | Klasse definieren |
| `wahr / falsch` | `True / False` | Boolean |
| `und / oder / nicht` | `and / or / not` | Logik |
| `nichts` | `None` | Nichts |
| `versuche / ausnahme` | `try / except` | Fehlerbehandlung |

### Eingebaute Funktionen

| Black Swan | Python | Beispiel |
|-----------|--------|---------|
| `drucke()` | `print()` | `drucke("Hallo Welt")` |
| `bereich()` | `range()` | `bereich(0, 10)` |
| `länge()` | `len()` | `länge(meine_liste)` |
| `zeichenkette()` | `str()` | `zeichenkette(42)` |
| `ganzzahl()` | `int()` | `ganzzahl("42")` |
| `liste()` | `list()` | `liste("abc") → ["a","b","c"]` |
| `sortiert()` | `sorted()` | `sortiert([3,1,2])` |
| `summe()` | `sum()` | `summe([1,2,3])` |

### Methoden (18 Übersetzungen)

```python
text = "Hallo Welt"
text.ersetzen("Welt", "Deutschland")    # .replace()
text.teilen(" ")                         # .split()
text.großbuchstaben()                    # .upper()
text.kleinbuchstaben()                   # .lower()
text.beginnt_mit("Hallo")               # .startswith()
text.endet_mit("Welt")                  # .endswith()

zahlen = [3, 1, 4, 1, 5]
zahlen.anhängen(9)                       # .append()
zahlen.sortieren()                       # .sort()
zahlen.umkehren()                        # .reverse()
zahlen.einfügen(2, 99)                  # .insert()
zahlen.entfernen(1)                      # .remove()
```

---

## 🎨 Beispiele

### Schildkröte: Koch-Schneeflocke

```python
funktion koch(länge, tiefe):
    wenn tiefe == 0:
        schildkröte.vorwärts(länge)
        zurückgeben nichts
    koch(länge / 3, tiefe - 1)
    schildkröte.links(60)
    koch(länge / 3, tiefe - 1)
    schildkröte.rechts(120)
    koch(länge / 3, tiefe - 1)
    schildkröte.links(60)
    koch(länge / 3, tiefe - 1)

schildkröte.farbe("#38bdf8")
für i in bereich(0, 3):
    koch(250, 4)
    schildkröte.rechts(120)
```

### Physik-Simulation

```python
schwerkraft(0.4)
boden = körper(0, 380, 400, 20, {"fest": wahr, "farbe": "#1a1a2e"})

für i in bereich(0, 8):
    körper(50 + i * 40, 50, 20, 20, {"farbe": "hsl(" + zeichenkette(i * 45) + ",80%,60%)"})

funktion zeichne():
    fülle("#0a0a14")
    physik_schritt()
    alle_körper_zeichnen()
```

### 3D-Szene

```python
funktion zeichne():
    szene_3d("#0a0a14")
    licht_3d(5, 5, 5)
    ebene_3d(0, -1, 0, 20, 20, "#1a1a2e")
    
    für i in bereich(0, 5):
        winkel = rahmen * 0.02 + i * 1.26
        x = 3 * kosinus(winkel)
        z = 3 * sinus(winkel)
        kugel_3d(x, 0, z, 0.5, "hsl(" + zeichenkette(i * 72) + ",70%,55%)")
    
    drehen_3d(0, 0.5, 0)
```

### KI-Training

```python
ki = ki_erstellen()

# Trainiere: [Temperatur, Regen?] → Aktivität
ki_lernen(ki, "Schwimmen", [30, 0])
ki_lernen(ki, "Schwimmen", [28, 0])
ki_lernen(ki, "Lesen", [5, 1])
ki_lernen(ki, "Lesen", [8, 1])
ki_lernen(ki, "Wandern", [20, 0])

drucke(ki_vorhersagen(ki, [27, 0]))  # → "Schwimmen"
drucke(ki_vorhersagen(ki, [6, 1]))   # → "Lesen"
drucke("Genauigkeit: " + zeichenkette(ki_genauigkeit(ki)) + "%")
```

---

## 🏗 Architektur

```
Black Swan Code (Deutsch)
        │
        ├─── Syntax-Highlighting (Regex, Umlaut-aware)
        │
        ├─── JS-Compiler (compileGerman → JavaScript)
        │    └── Indentation-basiert, wie Python
        │
        ├─── Python-Transpiler (deToEn → Python)
        │    └── Unicode Word Boundary: (?<![äöüÄÖÜß])
        │
        └─── Runtimes
             ├── Core: 25 Funktionen (bereich, länge, ...)
             ├── Schildkröte: Turtle-Grafik
             ├── Sound: Web Audio API
             ├── Physik: AABB-Kollision + Schwerkraft
             ├── Partikel: GPU-freundlich, Auto-Cleanup
             ├── Game: Tastatur + Spielobjekte
             ├── 3D: Three.js Wrapper
             ├── Shader: WebGL Fragment-Shader
             ├── KI: k-Nearest Neighbors
             └── Multiplayer: Shared Storage
```

**Technisches Highlight:** JavaScript-Regex erkennt deutsche Umlaute (ü, ö, ä, ß) nicht als Wortzeichen. Black Swan nutzt Unicode-aware Word Boundaries mit negativem Lookahead/Lookbehind — `(?<![a-zA-ZäöüÄÖÜß_0-9])` — um Wörter wie `überklasse` korrekt zu übersetzen.

---

## 🤝 Mitmachen

Beiträge sind willkommen! Besonders:

- 🌍 **Neue Sprachen** — Französisch? Spanisch? Türkisch?
- 📚 **Tutorial-Beispiele** — Zeig was Black Swan kann
- 🐛 **Bug Reports** — Etwas gefunden? Bitte melden
- 🎮 **Gallery-Spiele** — Baue ein Spiel und teile es

```bash
# Fork → Branch → Änderung → Pull Request
git checkout -b mein-feature
# Änderungen machen...
git commit -m "feat: Neues Feature hinzugefügt"
git push origin mein-feature
```

---

## 📊 Vergleich

| Feature | Black Swan | Hedy | DDP | Scratch |
|---------|:---------:|:----:|:---:|:-------:|
| Deutsche Syntax | ✅ Komplett | ✅ | ✅ | ❌ |
| Transpiliert zu Python | ✅ | ❌ | ✅ | ❌ |
| Inline IDE | ✅ | ✅ | ❌ | ✅ |
| Live Canvas | ✅ | ❌ | ❌ | ✅ |
| 3D-Grafik | ✅ | ❌ | ❌ | ❌ |
| Physik-Engine | ✅ | ❌ | ❌ | ❌ |
| Shader | ✅ | ❌ | ❌ | ❌ |
| KI-Training | ✅ | ❌ | ❌ | ❌ |
| Multiplayer | ✅ | ❌ | ❌ | ❌ |
| Game Engine | ✅ | ❌ | ❌ | ✅ |
| Spracheingabe | ✅ | ❌ | ❌ | ❌ |
| Sound/Musik | ✅ | ❌ | ❌ | ✅ |

---

## 📄 Lizenz

MIT — Frei nutzbar, auch kommerziell.

---

<div align="center">

**Gebaut mit 🖤 und viel ☕**

*Programmieren sollte keine Sprachbarriere haben.*

[Live Demo](https://SANDQEEN1111.github.io/black-swan/) · [Issues](https://github.com/SANDQEEN1111/black-swan/issues) · [Discussions](https://github.com/SANDQEEN1111/black-swan/discussions)

</div>
