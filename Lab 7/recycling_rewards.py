import math


def _to_weight(token):
    """Convert a string to a finite, non-negative number; raise ValueError otherwise."""
    value = float(token)
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"invalid number: {token!r}")
    return value


def parse_collection(text):
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    material = parts[0].strip()
    if not material:
        return None
    try:
        kg = _to_weight(parts[1])
    except (ValueError, OverflowError):
        return None
    return material.title(), kg


def weight_average(weights_csv):
    if not isinstance(weights_csv, str) or not weights_csv.strip():
        return None
    try:
        values = [_to_weight(r) for r in weights_csv.split(',')]
    except (ValueError, OverflowError):
        return None
    n = len(values)
    # true division (not //), dividing first so large values can't overflow to inf
    return math.fsum(v / n for v in values)


def net_points(text):
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    try:
        points = _to_weight(parts[0])
        penalty = _to_weight(parts[1])
    except (ValueError, OverflowError):
        return None
    total = points * 2 - penalty
    if not math.isfinite(total):
        return None
    return max(total, 0)


def main():
    print("==== Running parse_collection ====")
    user_input = input("Enter material:weight in kg (e.g. paper:12): ")
    result = parse_collection(user_input)
    print("Material and Weight:", result if result is not None else "Invalid input")

    print("\n==== Running weight_average ====")
    user_input = input("Enter weights in kg as CSV (e.g. 5,12,20): ")
    result = weight_average(user_input)
    print("Average Weight:", result if result is not None else "Invalid input")

    print("\n==== Running net_points ====")
    user_input = input("Enter points|penalty (e.g. 80|10): ")
    result = net_points(user_input)
    print("Net Points:", result if result is not None else "Invalid input")

if __name__ == "__main__":
    main()
