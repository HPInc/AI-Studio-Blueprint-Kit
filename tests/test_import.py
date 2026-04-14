def test_top_level_import() -> None:
    import ai_studio_blueprint_kit

    assert ai_studio_blueprint_kit.__version__ == "0.1.0"


def test_memory_guard_imports() -> None:
    from ai_studio_blueprint_kit.memory_guard import MemoryStatus, check_ram, check_vram, run_memory_check_notebook

    assert MemoryStatus is not None
    assert check_ram is not None
    assert check_vram is not None
    assert run_memory_check_notebook is not None
