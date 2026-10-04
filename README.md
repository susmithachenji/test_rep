# expandtesting.com — Playwright UI & REST API test suite

[![tests](https://github.com/susmithachenji/test_rep/actions/workflows/tests.yml/badge.svg)](https://github.com/susmithachenji/test_rep/actions/workflows/tests.yml)

Automation tests for [practice.expandtesting.com](https://practice.expandtesting.com/) built with
**pytest + Playwright (sync API) + requests**. 28 test cases: 15 marked `ui`, 14 marked `api`
(the cars showroom test carries both markers).

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
```

Optional: copy `.env.example` to `.env` and change the values there.

## Run

```powershell
pytest                        # everything + HTML report at reports/report.html
pytest -m smoke               # 4 fast tests (health-check, cars API, login, logout)
pytest -m ui                  # browser tests only
pytest -m api                 # REST API tests only
pytest -m "ui and smoke"      # any marker expression works
pytest tests/api -v           # single folder, verbose
pytest --headed               # watch the browser work
pytest -k "login"             # by keyword
HEADLESS=false pytest         # run with a visible window
```

Failing UI tests drop a full-page screenshot into `reports/artifacts/<test name>.png`.

## Layout

```
config.py                  base URLs, credentials, timeouts (env overridable)
conftest.py                browser / context / page and API client fixtures
clients/
  site_api_client.py       public endpoints (health-check, /api/cars, status codes)
  notes_client.py          Notes REST API (x-auth-token, notes CRUD)
pages/                     page objects, one class per demo page
tests/ui/                  Playwright tests
tests/api/                 requests-based tests
```

## UI tests (tests/ui)

| Test | What it covers |
| --- | --- |
| `test_login.py` | valid login → `/secure` welcome heading; invalid username / invalid password flash messages; logout |
| `test_form_widgets.py` | add/remove elements, web inputs display + clear, checkbox states and toggling, dropdown (simple + country) |
| `test_dynamic_content.py` | randomised Task Manager table (column order, Chrome CPU label vs cell), sortable table asc/desc, dynamic controls remove/add + enable/disable (5 s async delay) |
| `test_browser_features.py` | JS alert/confirm/prompt dialog handling, HTTP status code pages 200/301/404/500, notification flash message |
| `test_cars_showroom.py` | cars showroom UI cross-checked against the `/api/cars` payload |

## API tests (tests/api)

| Test | What it covers |
| --- | --- |
| `test_site_api.py` | Notes API health-check, `/api/cars` schema, HTTP status code pages over raw HTTP |
| `test_notes_api.py` | register → login → token → profile, wrong password 401, note create/read/list, validation errors (short title/description), PATCH completion + PUT update, delete → 404, bad note id, auth guards (missing/invalid token) |

## Run in the cloud (GitHub Actions)

`.github/workflows/tests.yml` runs on every push to `main`, on every pull request, nightly
(`17 6 * * *` UTC) and on demand via **Actions → tests → Run workflow**.

The job matrix runs the suite three ways:

| Runner | Python |
| --- | --- |
| `ubuntu-latest` | 3.13 |
| `ubuntu-latest` | 3.12 |
| `windows-latest` | 3.13 (matches local development) |

Each job installs the pinned `requirements.txt`, installs Chromium
(`playwright install --with-deps` on Linux), runs `pytest -ra --junitxml=reports/junit.xml`,
writes a small markdown summary into the job summary, and uploads
`reports/report.html` plus any failure screenshots as a **pytest-report-...** artifact
(kept 14 days). No secrets are needed — everything hits the public demo site.

First push:

```powershell
git add -A
git commit -m "Playwright + REST API test suite with GitHub Actions"
git push -u origin main
```

Download the HTML report locally after a cloud run:

```powershell
gh run download --name pytest-report-ubuntu-latest-py3.13
```

## Notes

* Web UI credentials come from the site: `practice` / `SuperSecretPassword!`.
* Every API test creates its own Notes account (`playtest.<uuid>@example.com`) and deletes it
  in fixture teardown, so runs are repeatable and isolated.
* Ad requests are blocked in the browser context for speed and stability; `wait_until="networkidle"`
  is avoided because of the third-party trackers.