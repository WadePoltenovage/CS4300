import pytest
from task7 import calculate_array_stats

def test_calculate_array_stats_reproducible():
    # The expected values are for a known seed (42) and the default size (100)
    expected_mean = 0.47018074337820936
    expected_std_dev = 0.29599822663249037

    mean, std_dev = calculate_array_stats()

    assert mean == pytest.approx(expected_mean)
    assert std_dev == pytest.approx(expected_std_dev)

def test_calculate_array_stats_different_size():
    size = 50
    expected_mean = 0.44592390439226115
    expected_std_dev = 0.2859797785370301

    mean, std_dev = calculate_array_stats(size=size)

    assert mean == pytest.approx(expected_mean)
    assert std_dev == pytest.approx(expected_std_dev)