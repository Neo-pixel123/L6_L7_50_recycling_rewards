import pytest
from recycling_rewards import reward_points, collection_accepted, slot_status


# ---------- reward_points ----------

def test_below_minimum_weight():
    assert reward_points("paper", 3, False) == 0

def test_exactly_minimum_weight_gives_zero():
    # extra == 0 -> "extra <= 0" True at the boundary
    assert reward_points("plastic", 3, False) == 0

def test_unknown_material_raises():
    with pytest.raises(ValueError, match="unknown material"):
        reward_points("glass", 10, False)

def test_negative_weight_raises():
    with pytest.raises(ValueError, match="invalid weight"):
        reward_points("paper", -1, False)

def test_paper_with_bonus_lowers_minimum():
    # bonus True, not metal -> minimum 5 -> 4, extra = 6, rate 6
    assert reward_points("paper", 10, True) == 36

def test_metal_with_bonus_ignores_bonus():
    # bonus True but metal -> minimum stays 2, extra = 3, rate 12
    assert reward_points("metal", 5, True) == 36

def test_plastic_normal_rate():
    # no bonus, extra = 7 (<= 20), rate 6
    assert reward_points("plastic", 10, False) == 42

def test_metal_normal_rate():
    # extra = 8 (<= 20), rate 12
    assert reward_points("metal", 10, False) == 96

def test_paper_heavy_load_rate_boost():
    # extra = 25 (> 20), not metal -> rate = 6 + 4 = 10
    assert reward_points("paper", 30, False) == 250

def test_metal_heavy_load_rate_boost():
    # extra = 28 (> 20), metal -> rate = 12 + 4 + 2 = 18
    assert reward_points("metal", 30, False) == 504

def test_extra_exactly_20_no_boost():
    # extra = 20 -> "extra > 20" False at the boundary, rate 6
    assert reward_points("plastic", 23, False) == 120


# ---------- collection_accepted ----------

def test_collection_accepted():
    assert collection_accepted(20, 2, False) is True

def test_hazardous_light_accepted():
    assert collection_accepted(4, 1, True) is True

def test_hazardous_heavy_rejected():
    assert collection_accepted(6, 1, True) is False

def test_overweight_rejected():
    assert collection_accepted(60, 1, False) is False

def test_too_many_bags_rejected():
    assert collection_accepted(20, 4, False) is False


# ---------- slot_status ----------

def test_morning_holiday_open():
    # cutoff = 20 + 15 = 35
    assert slot_status(40, True, True) == "open"

def test_afternoon_no_holiday_open():
    # cutoff = 10
    assert slot_status(10, False, False) == "open"

def test_afternoon_late():
    # cutoff = 10, 5 >= -5
    assert slot_status(5, False, False) == "late"

def test_afternoon_holiday_late():
    # cutoff = 10 + 15 = 25, 12 >= 10
    assert slot_status(12, False, True) == "late"

def test_morning_missed():
    # cutoff = 20, 0 < 5
    assert slot_status(0, True, False) == "missed"
