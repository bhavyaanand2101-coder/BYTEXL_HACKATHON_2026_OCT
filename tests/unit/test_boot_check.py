from scripts.boot_check import run_boot_check

def test_boot_check_passes():
    config_hash, targets_hash = run_boot_check()
    assert len(config_hash) == 16
    assert len(targets_hash) == 16
