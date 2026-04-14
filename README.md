# AI-Studio-Blueprint-Kit

`AI-Studio-Blueprint-Kit` is a public Python package and source repository for reusable utilities that support AI Studio blueprint development.

This repository is intentionally structured for growth. It starts with the `memory_guard` module and can later include additional modules under the same top-level package.

## Current module

### `ai_studio_blueprint_kit.memory_guard`

A notebook-oriented RAM and VRAM resource guard designed for local AI and ML workflows.

Main capabilities:
- checks Linux or WSL RAM availability from `/proc/meminfo`
- attempts NVIDIA VRAM detection through `nvidia-smi`, `torch`, or `pynvml`
- renders rich notebook warnings and pass/fail status with IPython HTML and Markdown when available
- shuts down the active Jupyter kernel when total hardware is insufficient

## Installation

Base install:

```bash
pip install ai-studio-blueprint-kit
```

With notebook UI dependencies:

```bash
pip install "ai-studio-blueprint-kit[notebook]"
```

With GPU helper dependency:

```bash
pip install "ai-studio-blueprint-kit[gpu]"
```

With Torch fallback support:

```bash
pip install "ai-studio-blueprint-kit[torch]"
```

## Usage

```python
from ai_studio_blueprint_kit.memory_guard import run_memory_check_notebook

run_memory_check_notebook(
    min_total_ram_gb=16.0,
    min_total_vram_gb=8.0,
)
```

Lower-level usage:

```python
from ai_studio_blueprint_kit.memory_guard import check_ram, check_vram

ram = check_ram()
vram = check_vram()

print(ram)
print(vram)
```

## Repository layout

```text
AI-Studio-Blueprint-Kit/
├── .github/
│   └── workflows/
├── src/
│   └── ai_studio_blueprint_kit/
│       ├── __init__.py
│       └── memory_guard/
│           ├── __init__.py
│           └── core.py
├── tests/
├── LICENSE
├── MANIFEST.in
├── README.md
└── pyproject.toml
```

## Adding future modules

New modules should be added under:

```text
src/ai_studio_blueprint_kit/
```

Examples:

```text
src/ai_studio_blueprint_kit/data_checks/
src/ai_studio_blueprint_kit/model_utils/
src/ai_studio_blueprint_kit/notebook_ui/
```

This keeps the public import surface consistent:

```python
from ai_studio_blueprint_kit.memory_guard import run_memory_check_notebook
```

## Development

Create a virtual environment and install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Build package distributions:

```bash
python -m build
```

Validate distributions:

```bash
python -m twine check dist/*
```

## Publishing

Recommended release flow:

1. publish the repository publicly on GitHub
2. test on TestPyPI first
3. configure PyPI Trusted Publishing for GitHub Actions
4. push a version tag such as `v0.1.0`

## Notes

- The current RAM check is Linux and WSL oriented because it reads `/proc/meminfo`.
- VRAM detection is primarily intended for NVIDIA environments.
- Notebook rendering is optional and is only used when IPython is available.
- Kernel shutdown on hard failure is intentional in the current `memory_guard` behavior.

## License

MIT
