from __future__ import annotations

from unittest.mock import mock_open, patch

import pytest

from ai_studio_blueprint_kit.memory_guard import (
    MemoryStatus,
    check_ram,
    check_vram,
)


def test_check_ram_returns_valid_memory_status() -> None:
    ram = check_ram()
    assert isinstance(ram, MemoryStatus)
    assert ram.total_gb > 0
    assert ram.free_gb >= 0
    assert ram.effective_available_gb >= 0
    assert 0.0 <= ram.used_fraction <= 1.0


def test_check_ram_from_mock_proc_meminfo() -> None:
    meminfo_content = (
        "MemTotal:       16384000 kB\n"
        "MemFree:         4096000 kB\n"
        "MemAvailable:    8192000 kB\n"
    )

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=meminfo_content)):
            ram = check_ram()
            assert round(ram.total_gb) == 16
            assert round(ram.available_gb) == 8
            assert round(ram.free_gb) == 4


def test_check_ram_windows_host_fallback() -> None:
    mock_status = MemoryStatus(free_gb=8.0, total_gb=16.0, available_gb=8.0)
    with patch("os.path.exists", return_value=False):
        with patch("sys.platform", "win32"):
            with patch(
                "ai_studio_blueprint_kit.memory_guard.core._check_host_ram_windows",
                return_value=mock_status,
            ):
                ram = check_ram()
                assert ram == mock_status
                assert ram.total_gb == 16.0
                assert ram.available_gb == 8.0


def test_check_ram_raises_runtime_error_when_all_fail() -> None:
    with patch("os.path.exists", return_value=False):
        with patch("sys.platform", "unknown_os"):
            with patch("os.name", "unknown_os"):
                with patch.dict("sys.modules", {"psutil": None}):
                    with pytest.raises(RuntimeError, match="Unable to determine system RAM"):
                        check_ram()


def test_check_vram_falls_back_to_windows_host() -> None:
    mock_vram = MemoryStatus(free_gb=6.0, total_gb=8.0, available_gb=6.0)
    with patch(
        "ai_studio_blueprint_kit.memory_guard.core._check_vram_nvidia_smi_used_total",
        return_value=None,
    ):
        with patch(
            "ai_studio_blueprint_kit.memory_guard.core._check_vram_torch",
            return_value=None,
        ):
            with patch(
                "ai_studio_blueprint_kit.memory_guard.core._check_vram_pynvml",
                return_value=None,
            ):
                with patch(
                    "ai_studio_blueprint_kit.memory_guard.core._check_vram_nvidia_smi",
                    return_value=None,
                ):
                    with patch(
                        "ai_studio_blueprint_kit.memory_guard.core._check_host_vram_windows",
                        return_value=mock_vram,
                    ):
                        vram = check_vram()
                        assert vram == mock_vram
                        assert vram.total_gb == 8.0
