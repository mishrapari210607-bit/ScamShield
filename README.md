# ScamShield

ScamShield is a small web app for checking suspicious messages. It uses a
transparent, rule-based heuristic and is intended as a warning aid, not as a
guarantee that a message is safe or fraudulent.

## Project structure

```text
ScamShield/
├── backend/       FastAPI API and detection engine
├── frontend/      HTML, CSS, and JavaScript interface
├── tests/         Automated tests
├── .gitignore
└── requirements.txt
```

## Setup

Use Python 3.10 or newer. From the project root, create and activate a virtual
environment, then install the dependencies:

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run

Start the API and web app from the project root:

```bash
uvicorn backend.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). The API documentation is
available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

To run the tests:

```bash
python -m unittest discover -s tests -v
```

## How the check works

The detector looks for common warning signs such as urgent language, requests
for passwords or one-time codes, suspicious payment demands, and links. It
does not open links, contact external services, or verify a sender's identity.
Avoid sharing sensitive personal information when checking a message.
