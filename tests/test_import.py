from ai_studio_blueprint_kit.memory_guard import (
    MemoryStatus,
    check_ram,
    check_vram,
    run_memory_check_notebook,
)


def test_imports() -> None:
    assert MemoryStatus is not None
    assert check_ram is not None
    assert check_vram is not None
    assert run_memory_check_notebook is not None
