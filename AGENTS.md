# AGENTS.md — ChartCraft

> Edit this file when conventions change. All agentic agents operating in this
> repository MUST follow the guidelines below.

---

## Project Overview

**ChartCraft** is a Python dashboard framework (zero runtime dependencies — stdlib only)
that generates interactive, ECharts-powered dashboards. The public API lives in
`chartcraft/__init__.py`. Users instantiate an `App`, register `@app.page()` handlers
returning `Dashboard` objects, and call `app.run()`.

| | |
|---|---|
| Language | Python 3.11+ |
| Package manager | pip |
| Build system | setuptools + pyproject.toml |
| Runtime deps | Zero (stdlib only) |
| Optional deps | sqlalchemy, pandas, playwright |
| Frontend | ECharts 5.5.0 (CDN), vanilla JS, inline CSS in HTML templates |
| Linter | ruff (error-level only) |

---

## Build / Lint / Test Commands

### Build distribution
```bash
pip install --upgrade build twine
python -m build
twine check dist/*
```

### Install from wheel (for local smoke tests)
```bash
pip install dist/*.whl
```

### Lint (CI rules — errors only, no style enforcement)
```bash
pip install ruff
ruff check chartcraft/ --select E9,F63,F7,F82 --output-format github
```

### Run a single smoke test
```bash
python - <<'EOF'
import chartcraft as cc

assert hasattr(cc, "App")
assert hasattr(cc, "Dashboard")
assert hasattr(cc, "Bar")
assert hasattr(cc, "Line")

html = cc.quick_dashboard(
    title="Test",
    charts=[cc.Bar({"A": 1, "B": 2}, title="Test Chart")],
    theme="midnight",
)
assert "ChartCraft" in html
print("OK")
EOF
```

### Run a single pytest (if tests exist)
```bash
pytest tests/test_foo.py::test_bar -v
```

### Full dev workflow
```bash
# 1. Lint
ruff check chartcraft/ --select E9,F63,F7,F82

# 2. Build
python -m build

# 3. Install
pip install dist/*.whl

# 4. Smoke test
python - <<'EOF'
import chartcraft as cc
...
EOF
```

---

## Code Style Guidelines

### Imports

```python
from __future__ import annotations   # REQUIRED — first line of every .py file

import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union
```

- All files MUST begin with `from __future__ import annotations`.
- Use `from typing import ...` style (NOT the PEP 585 built-in generics like `list[str]` in type aliases — the codebase uses `List[str]`, `Dict[str, Any]`, etc.).
- Import third-party packages lazily (inside functions) when they are optional dependencies, e.g.:

```python
def query_df(self, sql: str, params=None):
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas is required for query_df(). pip install pandas")
    return pd.read_sql(...)
```

### Formatting

- **4 spaces** for indentation (no tabs).
- **No line length limit** enforced by CI (only structural errors checked).
- Use **alphabetical import ordering** within each group (stdlib → typing → local).
- Separate import groups with a single blank line.

### Type Annotations

- Use `Optional[X]` instead of `X | None` in type annotations (PEP 585 not adopted).
- Use `Union[A, B]` instead of `A | B`.
- Return types on all public methods.
- `-> dict` for `to_spec()` and similar serialization methods.

### Naming Conventions

| Thing | Convention | Example |
|---|---|---|
| Classes | PascalCase | `class Dashboard:` |
| Functions / variables | snake_case | `def get_theme(` |
| Module-level constants | SCREAMING_SNAKE | `FILTER_TYPES = {...}` |
| Type aliases | PascalCase | `DataSource = Union[...]` |
| Private helpers | `_leading_underscore` | `def _uid():` |

### Dataclasses (Core Models)

Models use `@dataclass` throughout. Key patterns:

```python
from dataclasses import dataclass, field

def _uid() -> str:
    return str(uuid.uuid4())[:8]

@dataclass
class MyChart(_BaseChart):
    title: str = ""
    my_list: List[str] = field(default_factory=list)
    my_dict: Dict[str, Any] = field(default_factory=dict)
```

- NEVER use mutable literals as default values — use `field(default_factory=...)`.
- Use `__post_init__(self)` for validation and setting `chart_type`.
- Always call `super().__post_init__()` if overriding in subclasses (or set `chart_type` directly).

### Error Handling

- Wrap user-callable operations (`data_fn`, `query`, `_normalise`) in try/except that returns a safe error payload (never raise from these paths).
- Use `raise ImportError(...)` with a clear install hint for optional dependency errors.
- Use `raise ValueError(...)` for invalid argument combinations with a descriptive message.
- Never swallow exceptions silently without an error payload.

```python
# Good — error passthrough in resolve
try:
    return self.data_fn(filters or {})
except Exception as e:
    return f"Error: {e}"

# Good — ImportError for optional deps
except ImportError:
    raise ImportError("sqlalchemy is required for non-SQLite. pip install chartcraft[sql]")
```

### Serialization (`to_spec()`)

Every model has a `to_spec(self, filters: dict = None) -> dict` method that returns a JSON-safe dict. Rules:

- Return only JSON-serializable Python types (no `None` where `null` is wrong, no `bytes`).
- `to_spec()` is the bridge between Python models and the frontend — keep it stable.
- Private `_` prefix on helper methods that are not part of the public serialization contract.
- `Dashboard.to_spec()` calls `to_spec()` on all child components recursively.

### Code Generation / HTML

- HTML templates live in `chartcraft/static/` and `chartcraft/builder/`.
- Template substitution uses `{{PLACEHOLDER}}` patterns replaced via `str.replace()`.
- ECharts is loaded from CDN (`https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js`).
- No build step for frontend assets — keep them self-contained.

### Folder Structure

```
chartcraft/
├── __init__.py           # Public API (re-exports everything)
├── presets.py            # High-level page/chart builders
├── core/
│   ├── models.py         # All chart/data models (dataclasses)
│   ├── theme.py          # Theme registry and CSS generation
│   ├── colors.py         # Color utilities
│   └── serializer.py     # JSON serialization helpers
├── server/
│   ├── app_server.py     # AppServer (ThreadingHTTPServer)
│   ├── handler.py        # HTTP request handler
│   ├── parser.py         # Dashboard parsing
│   ├── codegen.py        # HTML/JS code generation
│   ├── query_api.py      # SQL query REST API
│   ├── projects.py       # Project management
│   └── sse.py            # Server-Sent Events
├── connectors/
│   ├── sql.py            # SQLConnector (SQLite + SQLAlchemy)
│   ├── csv_connector.py
│   └── api.py
├── builder/              # Visual builder UI
│   ├── builder.html
│   └── components/
│       └── color_picker.js
└── static/
    └── viewer.html       # Dashboard viewer template
```

### Logging and Output

- Use `print(f"  [ChartCraft] ...")` for user-facing server output (not `logging`).
- Prefix user-facing output with arrows: `->`, `◆`, `[Exported]`.
- Never log sensitive data or connection strings.

### Testing Guidelines

- Smoke tests use inline Python EOF blocks (see Commands section above).
- If adding pytest tests, place them in a `tests/` directory.
- Test file naming: `test_<module>.py`.
- Each model should have a `to_spec()` round-trip test.
- Test optional connectors only when the relevant extra is installed.

### Performance Considerations

- All I/O is lazy — connectors and data functions run only when a page is accessed.
- `ThreadingHTTPServer` handles concurrent requests.
- Avoid computing theme CSS or ECharts options in hot paths — they are cached on `AppServer`.
- Heavy optional imports (pandas, sqlalchemy) must remain inside functions.

### Git Conventions

- Commit message format: imperative mood, 72 chars max first line.
  - `feat: add Sankey chart type`
  - `fix: handle empty data in Heatmap._normalise`
  - `docs: update quick start example`
- Keep commits focused — one logical change per commit.
- Never commit `dist/`, `.ruff_cache/`, or `__pycache__/`.
- The `.gitignore` covers standard Python output directories.

### Adding a New Chart Type

1. Add a new `@dataclass` class in `chartcraft/core/models.py` inheriting from `_BaseChart`.
2. Set `chart_type` in `__post_init__`.
3. Implement `_chart_options(self) -> dict` for ECharts config.
4. Override `_normalise(self, raw)` if the data format differs from the standard `{labels, datasets}` structure.
5. Re-export from `chartcraft/__init__.py` and add to `__all__`.
6. Add to the smoke test in `.github/workflows/ci.yml` (`install-test` job).
7. Run lint and smoke test locally.
