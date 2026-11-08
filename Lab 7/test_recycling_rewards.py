import math
from hypothesis import given, strategies as st
from recycling_rewards import parse_collection, weight_average, net_points

# Number-like tokens: ints, floats (incl. nan / inf / negatives) and junk text
number_token = st.one_of(
    st.integers().map(str),
    st.floats().map(str),
    st.text(max_size=5),
)


# ---------- parse_collection ----------

@given(st.text() | st.none())
def test_parse_collection_no_crash(s):
    try:
        parse_collection(s)
    except Exception as e:
        assert False, f"parse_collection crashed with: {e!r}"


@given(st.builds(lambda m, w: f"{m}:{w}", st.text(), number_token))
def test_parse_collection_valid_output(s):
    try:
        result = parse_collection(s)
    except Exception as e:
        assert False, f"parse_collection crashed with: {e!r}"
    if result is not None:
        material, kg = result
        assert material != "", f"empty material accepted for {s!r}"
        assert math.isfinite(kg) and kg >= 0, f"invalid weight {kg!r} for {s!r}"


# ---------- weight_average ----------

@given(st.text() | st.none())
def test_weight_average_no_crash(s):
    try:
        weight_average(s)
    except Exception as e:
        assert False, f"weight_average crashed with: {e!r}"


@given(st.lists(number_token).map(",".join))
def test_weight_average_valid_output(s):
    try:
        result = weight_average(s)
    except Exception as e:
        assert False, f"weight_average crashed with: {e!r}"
    if result is not None:
        assert math.isfinite(result) and result >= 0, f"invalid average {result!r} for {s!r}"


@given(st.lists(st.integers(min_value=0, max_value=10**6), min_size=1))
def test_weight_average_is_correct(weights):
    s = ",".join(map(str, weights))
    expected = sum(weights) / len(weights)
    result = weight_average(s)
    assert result is not None and math.isclose(result, expected), \
        f"average of {weights} should be {expected}, got {result!r}"


# ---------- net_points ----------

@given(st.text() | st.none())
def test_net_points_no_crash(s):
    try:
        net_points(s)
    except Exception as e:
        assert False, f"net_points crashed with: {e!r}"


@given(st.builds(lambda p, q: f"{p}|{q}", number_token, number_token))
def test_net_points_valid_output(s):
    try:
        result = net_points(s)
    except Exception as e:
        assert False, f"net_points crashed with: {e!r}"
    if result is not None:
        assert math.isfinite(result) and result >= 0, f"invalid net points {result!r} for {s!r}"


@given(st.integers(min_value=0, max_value=10**6), st.integers(min_value=0, max_value=10**6))
def test_net_points_is_correct(points, penalty):
    result = net_points(f"{points}|{penalty}")
    assert result == max(points * 2 - penalty, 0)
