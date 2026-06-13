# BlueAnt API Backend – Projekt Gruppe 6

Dieses Repository enthält den Backend-Prototyp für unser BlueAnt-Projekt im Modul **Management von IV-Projekten**.

Das Backend ruft Projektdaten aus dem BlueAnt-Demosystem ab, filtert das relevante **AI Portfolio**, bereitet die Daten auf und stellt sie dem Frontend über eine einfache API bereit.

Der wichtigste Endpoint für das Frontend ist:

```text
GET /api/projects
```

Lokal erreichbar unter:

```text
http://127.0.0.1:8000/api/projects
```

---

# 1. Ziel des Backends

Das Backend hat die Aufgabe, die Projektdaten aus BlueAnt so vorzubereiten, dass das Frontend und später die KI-Komponente damit arbeiten können.

Der Ablauf ist:

```text
BlueAnt API
→ Backend
→ Portfolio prüfen
→ Projekte laden
→ AI Portfolio filtern
→ KPI-Felder lesbar machen
→ HTML-Texte bereinigen
→ JSON für Frontend bereitstellen
```

Das Frontend muss dadurch nicht direkt mit der BlueAnt API kommunizieren.

Das ist wichtig, weil:

* der API-Key nicht im Frontend sichtbar sein soll
* die Rohdaten aus BlueAnt sehr technisch sind
* viele BlueAnt-Felder nur IDs enthalten
* die relevanten KPI-Felder erst im Backend verständlich gemappt werden
* das Frontend eine möglichst einfache und saubere Datenstruktur bekommen soll

---

# 2. Projektstruktur

Die aktuelle Backend-Struktur sieht ungefähr so aus:

```text
blueant-api-test/
│
├── app/
│   ├── config.py
│   ├── blueant_client.py
│   ├── transformer.py
│   └── main.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Erklärung der wichtigsten Dateien

### `app/config.py`

Liest die Konfigurationswerte aus der `.env` Datei.

Wichtige Werte:

```text
BLUEANT_BASE_URL
BLUEANT_API_KEY
BLUEANT_FROM_DATE
BLUEANT_TO_DATE
TARGET_PORTFOLIO_ID
```

### `app/blueant_client.py`

Enthält die Funktionen für die Kommunikation mit der BlueAnt API.

Aktuell werden unter anderem genutzt:

```text
fetch_projects()
fetch_portfolio(portfolio_id)
```

### `app/transformer.py`

Bereitet die BlueAnt-Rohdaten auf.

Hier passiert unter anderem:

* Filtern der Projekte auf das AI Portfolio
* Mapping der technischen Custom-Field-IDs auf lesbare KPI-Namen
* Entfernen von HTML-Tags aus BlueAnt-Textfeldern
* Erzeugen einer frontend-freundlichen JSON-Struktur

### `app/main.py`

Startpunkt der FastAPI-Anwendung.

Hier werden die API-Endpunkte definiert, zum Beispiel:

```text
GET /
GET /api/projects
GET /api/portfolio
```

---

# 3. Lokales Setup

## Schritt 1: Repository klonen

```powershell
git clone <REPO-URL>
cd <REPO-NAME>
```

## Schritt 2: Virtuelle Python-Umgebung erstellen

```powershell
python -m venv .venv
```

## Schritt 3: Virtuelle Umgebung aktivieren

Unter Windows PowerShell:

```powershell
.venv\Scripts\activate
```

Falls PowerShell die Aktivierung blockiert:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\activate
```

## Schritt 4: Requirements installieren

```powershell
pip install -r requirements.txt
```

## Schritt 5: `.env` Datei erstellen

Im Repository gibt es eine Datei:

```text
.env.example
```

Diese Datei kopieren und in `.env` umbenennen.

Beispiel:

```powershell
copy .env.example .env
```

Danach die `.env` Datei öffnen und die echten Werte eintragen.

Beispielstruktur:

```env
BLUEANT_BASE_URL=https://dashboard-examples.blueant.cloud
BLUEANT_API_KEY=HIER_DEN_API_KEY_EINTRAGEN

BLUEANT_FROM_DATE=2025-10-01
BLUEANT_TO_DATE=2026-10-31
TARGET_PORTFOLIO_ID=676698496
```

Wichtig:

Die Datei `.env` darf **nicht** in GitHub hochgeladen werden, weil sie den API-Key enthält.

---

# 4. Backend starten

Das Backend wird lokal mit Uvicorn gestartet:

```powershell
uvicorn app.main:app --reload
```

Wenn alles funktioniert, sollte im Terminal ungefähr stehen:

```text
Uvicorn running on http://127.0.0.1:8000
```

Danach kann man im Browser testen:

```text
http://127.0.0.1:8000
```

Die automatische FastAPI-Dokumentation ist hier erreichbar:

```text
http://127.0.0.1:8000/docs
```

---

# 5. Wichtige Endpoints

## 5.1 Root Endpoint

```text
GET /
```

Beispiel:

```text
http://127.0.0.1:8000/
```

Dieser Endpoint dient nur zum kurzen Test, ob das Backend läuft.

---

## 5.2 Portfolio Endpoint

```text
GET /api/portfolio
```

Beispiel:

```text
http://127.0.0.1:8000/api/portfolio
```

Dieser Endpoint ruft die Portfolio-Informationen aus BlueAnt ab.

Aktuell wird das Portfolio verwendet:

```text
Portfolio ID: 676698496
Name: AI Portfolio
```

Das Portfolio enthält aktuell 5 Projekte.

---

## 5.3 Wichtigster Endpoint für das Frontend

```text
GET /api/projects
```

Beispiel:

```text
http://127.0.0.1:8000/api/projects
```

Dieser Endpoint ist der wichtigste Endpoint für das Frontend.

Er liefert:

* Portfolio-Metadaten
* Liste der Projekte im AI Portfolio
* Projektdaten
* bereinigte Textfelder
* lesbare KPI-Felder

---

# 6. Aufbau der `/api/projects` Response

Die Response sieht grundsätzlich so aus:

```json
{
  "portfolio": {
    "id": 676698496,
    "number": "111",
    "name": "AI Portfolio",
    "date_from": "2025-10-01",
    "date_to": "2026-10-31",
    "active": true,
    "project_count": 5
  },
  "total_projects": 48,
  "ki_portfolio_projects": 5,
  "projects": [
    {
      "id": 831186338,
      "number": "01014",
      "name": "Werk2-Maschinenverlagerung",
      "status_id": 11,
      "portfolio_ids": [676698496],
      "start": "2026-03-01",
      "end": "2026-07-31",
      "planning_type": "CLASSIC",
      "billing_type": "Quote",
      "subject": "...",
      "problem": "...",
      "objective": "...",
      "status_text": "...",
      "conclusion": "...",
      "overall_risk": {
        "overallRiskId": 146740685,
        "riskAssessment": "..."
      },
      "kpis": {
        "project_budget_eur": 95000,
        "planned_costs_eur": 43609.83,
        "actual_costs_eur": 65000,
        "planned_effort_until_today_pt": 310,
        "planned_effort_total_pt": 310,
        "actual_effort_pt": 200,
        "planned_completion_percent": 100,
        "actual_completion_percent": 0
      }
    }
  ]
}
```

---

# 7. Erklärung für das Frontend-Team

## 7.1 `portfolio`

Das Feld `portfolio` enthält allgemeine Informationen zum analysierten Portfolio.

Wichtige Felder:

| Feld            | Bedeutung                           |
| --------------- | ----------------------------------- |
| `id`            | Technische Portfolio-ID aus BlueAnt |
| `number`        | Portfolio-Nummer                    |
| `name`          | Name des Portfolios                 |
| `date_from`     | Startdatum des Portfolio-Zeitraums  |
| `date_to`       | Enddatum des Portfolio-Zeitraums    |
| `active`        | Gibt an, ob das Portfolio aktiv ist |
| `project_count` | Anzahl der Projekte im Portfolio    |

Empfehlung für Frontend:

Diese Daten können im Header oder auf einer Übersichtsseite angezeigt werden.

Beispiel:

```text
AI Portfolio
Zeitraum: 01.10.2025 – 31.10.2026
Anzahl Projekte: 5
```

---

## 7.2 `total_projects`

Dieses Feld zeigt, wie viele Projekte insgesamt aus der BlueAnt API geladen wurden.

Beispiel:

```json
"total_projects": 48
```

Dieses Feld ist eher zur Kontrolle gedacht.

Für die eigentliche Anzeige sollte das Frontend nicht alle Projekte verwenden, sondern nur:

```json
"projects"
```

---

## 7.3 `ki_portfolio_projects`

Dieses Feld zeigt, wie viele Projekte nach dem Filtern im AI Portfolio übrig bleiben.

Beispiel:

```json
"ki_portfolio_projects": 5
```

Das ist die Anzahl der Projekte, die für unser Projekt relevant sind.

---

## 7.4 `projects`

Das Feld `projects` ist die wichtigste Datenquelle für das Frontend.

Hier befindet sich die Liste der Projekte, die angezeigt und analysiert werden sollen.

Das Frontend sollte über diese Liste iterieren.

Beispiel in JavaScript:

```javascript
projects.forEach(project => {
  console.log(project.name);
  console.log(project.kpis.actual_costs_eur);
});
```

---

# 8. Wichtige Projektfelder für das Frontend

Jedes Projekt enthält diese wichtigen Felder:

| Feld           | Bedeutung                                |
| -------------- | ---------------------------------------- |
| `id`           | Technische BlueAnt-Projekt-ID            |
| `number`       | Projektnummer                            |
| `name`         | Projektname                              |
| `status_id`    | Technische Status-ID aus BlueAnt         |
| `start`        | Startdatum                               |
| `end`          | Enddatum                                 |
| `subject`      | Gegenstand / Beschreibung des Projekts   |
| `problem`      | Problem- oder Risikobeschreibung         |
| `objective`    | Zielbeschreibung                         |
| `status_text`  | Aktueller Statusbericht                  |
| `conclusion`   | Abschluss-/Datumsinformation aus BlueAnt |
| `overall_risk` | Risikoinformationen aus BlueAnt          |
| `kpis`         | Aufbereitete Kennzahlen                  |

Für die erste Frontend-Version sind besonders wichtig:

```text
name
number
start
end
status_text
problem
overall_risk
kpis
```

---

# 9. KPI-Felder

Die KPI-Felder wurden vom Auftraggeber als individuelle BlueAnt-Felder bereitgestellt und im Backend auf lesbare Namen gemappt.

Das Frontend sollte **nicht** mit den technischen BlueAnt Custom Field IDs arbeiten.

Das Frontend soll stattdessen ausschließlich das Feld `kpis` verwenden.

## KPI-Struktur

```json
"kpis": {
  "project_budget_eur": 95000,
  "planned_costs_eur": 43609.83,
  "actual_costs_eur": 65000,
  "planned_effort_until_today_pt": 310,
  "planned_effort_total_pt": 310,
  "actual_effort_pt": 200,
  "planned_completion_percent": 100,
  "actual_completion_percent": 0
}
```

## Erklärung der KPI-Felder

| Feld                            | Bedeutung                            | Einheit |
| ------------------------------- | ------------------------------------ | ------- |
| `project_budget_eur`            | Projektbudget                        | Euro    |
| `planned_costs_eur`             | Plankosten                           | Euro    |
| `actual_costs_eur`              | IST-Kosten                           | Euro    |
| `planned_effort_until_today_pt` | Plan-Aufwand bis heute               | PT      |
| `planned_effort_total_pt`       | Plan-Aufwand für den Projektzeitraum | PT      |
| `actual_effort_pt`              | Ist-Aufwand                          | PT      |
| `planned_completion_percent`    | Plan-Fertigstellung                  | Prozent |
| `actual_completion_percent`     | Ist-Fertigstellung                   | Prozent |

Hinweis:

```text
PT = Personentage
```

---

# 10. Vorschlag für erste Frontend-Ansichten

Das Frontend-Team kann mit diesen einfachen Ansichten starten.

## 10.1 Portfolio-Übersicht

Anzeigen:

* Name des Portfolios
* Zeitraum
* Anzahl der Projekte
* Anzahl kritischer Projekte später optional

Mögliche Darstellung:

```text
AI Portfolio
Zeitraum: 2025-10-01 bis 2026-10-31
Projekte: 5
```

---

## 10.2 Projektliste

Eine Tabelle oder Kartenansicht mit:

* Projektnummer
* Projektname
* Startdatum
* Enddatum
* Status-ID
* Ist-Fertigstellung
* Ist-Kosten
* Ist-Aufwand

Beispielspalten:

```text
Nummer | Name | Start | Ende | Fertigstellung Ist | Kosten Ist | Aufwand Ist
```

Datenquellen:

```text
project.number
project.name
project.start
project.end
project.kpis.actual_completion_percent
project.kpis.actual_costs_eur
project.kpis.actual_effort_pt
```

---

## 10.3 Projekt-Detailansicht

Wenn ein Projekt angeklickt wird, könnten angezeigt werden:

* Projektname
* Gegenstand (`subject`)
* Problem (`problem`)
* Ziel (`objective`)
* Statusbericht (`status_text`)
* Risiko (`overall_risk`)
* KPIs (`kpis`)

---

## 10.4 KPI-Karten

Für jedes Projekt oder für das gesamte Portfolio können KPI-Karten angezeigt werden.

Beispiele:

```text
Projektbudget
Plankosten
IST-Kosten
Plan-Aufwand
Ist-Aufwand
Plan-Fertigstellung
Ist-Fertigstellung
```

---

## 10.5 Einfache Ampel-Logik im Frontend

Falls das Frontend eine einfache farbliche Markierung bauen möchte, kann es zunächst mit einfachen Regeln arbeiten.

Beispiel:

```text
Wenn actual_costs_eur > planned_costs_eur → Kosten kritisch
Wenn actual_effort_pt > planned_effort_total_pt → Aufwand kritisch
Wenn actual_completion_percent < planned_completion_percent → Fortschritt kritisch
```

Das ist nur eine einfache erste Logik und ersetzt später nicht die KI-Auswertung.

---

# 11. Beispiel: Daten im Frontend abrufen

Beispiel mit JavaScript `fetch`:

```javascript
async function loadProjects() {
  const response = await fetch("http://127.0.0.1:8000/api/projects");
  const data = await response.json();

  console.log(data.portfolio.name);
  console.log(data.projects);

  return data;
}

loadProjects();
```

Beispiel: Projektname und Ist-Kosten anzeigen:

```javascript
async function showProjectCosts() {
  const response = await fetch("http://127.0.0.1:8000/api/projects");
  const data = await response.json();

  data.projects.forEach(project => {
    console.log(project.name);
    console.log(project.kpis.actual_costs_eur);
  });
}

showProjectCosts();
```

---

# 12. CORS

Im Backend wurde CORS aktiviert, damit ein lokales Frontend auf das Backend zugreifen kann.

Aktuell erlaubte lokale Frontend-URLs:

```text
http://localhost:5173
http://127.0.0.1:5173
http://localhost:3000
http://127.0.0.1:3000
```

Das ist wichtig, wenn das Frontend z. B. mit Vite, React oder einem anderen lokalen Entwicklungsserver läuft.

Wenn das Frontend einen anderen Port verwendet, muss dieser in `app/main.py` ergänzt werden.

Beispiel:

```python
allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

---

# 13. Was das Frontend-Team nicht ändern muss

Das Frontend-Team muss normalerweise nicht ändern:

```text
app/config.py
app/blueant_client.py
app/transformer.py
```

Diese Dateien gehören zum Backend.

Das Frontend-Team sollte hauptsächlich nur wissen:

```text
Backend starten
Endpoint /api/projects aufrufen
Response-Felder verwenden
```

---

# 14. Was das Frontend-Team eventuell anpassen muss

## 14.1 Backend-URL

Wenn das Backend lokal läuft, ist die URL:

```text
http://127.0.0.1:8000/api/projects
```

Wenn das Backend später in Docker oder auf einem anderen Port läuft, muss die URL im Frontend angepasst werden.

Beispiele:

```text
http://localhost:8000/api/projects
http://backend:8000/api/projects
```

Der zweite Fall kann relevant werden, wenn Frontend und Backend später gemeinsam in Docker Compose laufen.

---

## 14.2 CORS-Port

Falls das Frontend auf einem anderen Port läuft, muss dieser Port im Backend bei CORS eingetragen werden.

Beispiele für mögliche Frontend-Ports:

```text
5173
3000
4200
8080
```

Falls z. B. Angular mit Port 4200 verwendet wird, müsste in `app/main.py` ergänzt werden:

```python
"http://localhost:4200",
"http://127.0.0.1:4200",
```

---

## 14.3 Feldnamen im Frontend

Das Frontend sollte mit den aktuellen Feldnamen arbeiten.

Wichtig:

```text
project.kpis.actual_costs_eur
project.kpis.planned_costs_eur
project.kpis.actual_effort_pt
project.kpis.planned_effort_total_pt
project.kpis.actual_completion_percent
project.kpis.planned_completion_percent
```

Nicht verwenden:

```text
BlueAnt Custom Field IDs
```

Also nicht direkt mit IDs wie `838167179` oder `832985595` arbeiten.

Diese IDs wurden bereits im Backend gemappt.

---

# 15. Bekannte offene Punkte

Aktuell ist der Backend-Stand gut genug für die erste Frontend-Entwicklung.

Trotzdem gibt es noch offene Erweiterungen:

## 15.1 Status-ID Mapping

Aktuell liefert das Backend:

```json
"status_id": 11
```

Noch offen ist ein lesbarer Statusname, zum Beispiel:

```json
"status_name": "In Bearbeitung"
```

Dafür müsste später ein BlueAnt-Masterdata-Endpoint geprüft werden, vermutlich in Richtung:

```text
/masterdata/projects/statuses
```

## 15.2 Meilensteine / Planning Entries

Für eine vollständige Projektanalyse sind Meilensteine wichtig.

Dafür muss später vermutlich dieser Endpoint geprüft werden:

```text
/projects/{project_id}/planningentries
```

Dieser Teil ist aktuell noch nicht im normalen `/api/projects` Endpoint enthalten.

## 15.3 KI-Analyse

Aktuell liefert das Backend nur die aufbereiteten Projektdaten.

Die KI-Auswertung selbst ist noch nicht implementiert.

Möglicher späterer Ablauf:

```text
/api/projects
→ KI-Modell bekommt Projektdaten
→ KI erzeugt Analyse
→ Frontend zeigt Analyse an
```

Als kostenlose lokale KI-Lösung wurde Ollama als mögliche Option vorgeschlagen.

## 15.4 Docker

Das Backend läuft aktuell lokal über Uvicorn.

Docker ist noch nicht umgesetzt.

Für die finale Abgabe könnte später ein Docker-Setup ergänzt werden.

---

# 16. Aktueller Stand

Aktuell umgesetzt:

```text
✅ Verbindung zur BlueAnt API
✅ Konfiguration über .env
✅ Portfolio-Endpoint geprüft
✅ AI Portfolio mit ID 676698496 validiert
✅ Projekte aus BlueAnt geladen
✅ AI Portfolio Projekte gefiltert
✅ KPI-Custom-Fields gemappt
✅ HTML-Tags aus Textfeldern entfernt
✅ Clean JSON Response für Frontend erstellt
✅ CORS für lokale Frontend-Entwicklung aktiviert
```

Aktuell wichtigste Backend-URL:

```text
http://127.0.0.1:8000/api/projects
```

---

# 17. Empfehlung für das Frontend-Team

Das Frontend-Team sollte zuerst eine sehr einfache Oberfläche bauen.

Empfohlene Reihenfolge:

```text
1. Backend lokal starten
2. /api/projects im Browser testen
3. Mit fetch() die Daten im Frontend laden
4. Portfolio-Name und Anzahl Projekte anzeigen
5. Projektliste anzeigen
6. KPI-Werte pro Projekt anzeigen
7. Projekt-Detailansicht ergänzen
8. Später KI-Auswertung integrieren
```

Bitte zuerst keine komplexe Oberfläche bauen.

Wichtig ist zuerst, dass die Daten korrekt aus dem Backend geladen und verständlich angezeigt werden.

---

# 18. Kurze Zusammenfassung

Das Backend stellt dem Frontend aktuell einen sauberen Endpoint bereit:

```text
GET /api/projects
```

Dieser Endpoint liefert die relevanten Projekte aus dem **AI Portfolio** inklusive bereinigter Texte und lesbarer KPI-Werte.

Das Frontend-Team muss nicht direkt mit der BlueAnt API oder den technischen Custom-Field-IDs arbeiten.

Für die erste Frontend-Version reicht es, diesen Endpoint aufzurufen und die Felder aus `portfolio`, `projects` und `kpis` anzuzeigen.
