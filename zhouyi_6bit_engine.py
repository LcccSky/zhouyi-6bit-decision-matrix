#!/usr/bin/env python3
"""
Zhouyi 6-Bit Combinatorial State Machine & Equation-of-Time Solar Calibration
Interactive reference implementation for https://hexsage.ai/
"""
import math
import random

TRIGRAMS = {
    1: ("Qian", "111"),
    2: ("Dui", "110"),
    3: ("Li", "101"),
    4: ("Zhen", "100"),
    5: ("Xun", "011"),
    6: ("Kan", "010"),
    7: ("Gen", "001"),
    8: ("Kun", "000"),
}


def shao_yong_cast(n1: int, n2: int) -> dict:
    """Deterministic Shao Yong two-number modulo coordinate mapping."""
    upper_idx = ((n1 - 1) % 8) + 1
    lower_idx = ((n2 - 1) % 8) + 1
    moving_line = ((n1 + n2 - 1) % 6) + 1
    bits = list(TRIGRAMS[lower_idx][1] + TRIGRAMS[upper_idx][1])
    next_bits = bits[:]
    next_bits[moving_line - 1] = "0" if bits[moving_line - 1] == "1" else "1"
    return {
        "upper_trigram": TRIGRAMS[upper_idx][0],
        "lower_trigram": TRIGRAMS[lower_idx][0],
        "moving_line": moving_line,
        "primary_bits_L1_to_L6": "".join(bits),
        "resulting_bits_L1_to_L6": "".join(next_bits),
    }


def three_coin_line(rng: random.Random = random) -> int:
    """Three independent Bernoulli trials -> {6: 2/16, 7: 6/16, 8: 6/16, 9: 2/16}."""
    return sum(3 if rng.random() < 0.5 else 2 for _ in range(3))


def yarrow_stalk_line(rng: random.Random = random) -> int:
    """49-active-stalk 3-change remainder protocol -> {6: 1/16, 7: 5/16, 8: 7/16, 9: 3/16}."""
    stalks = 49
    for _ in range(3):
        left = rng.randint(1, stalks - 1)
        right = stalks - left - 1
        rem_left = left % 4 or 4
        rem_right = right % 4 or 4
        stalks -= 1 + rem_left + rem_right
    return stalks // 4


def true_solar_time_offset_minutes(longitude_deg: float, std_meridian_deg: float, day_of_year: int) -> float:
    """Compute True Solar Time offset in minutes (longitude + Equation of Time)."""
    b_rad = math.radians(360.0 * (day_of_year - 81) / 365.0)
    eot = 9.87 * math.sin(2 * b_rad) - 7.53 * math.cos(b_rad) - 1.5 * math.sin(b_rad)
    return 4.0 * (longitude_deg - std_meridian_deg) + eot


if __name__ == "__main__":
    print("Shao Yong [16, 85]:", shao_yong_cast(16, 85))
    print("True Solar Time offset (NYC -74.006, EST -75.0, day 306):",
          round(true_solar_time_offset_minutes(-74.006, -75.0, 306), 2), "min")
