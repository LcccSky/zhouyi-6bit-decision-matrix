"""
zhouyi-6bit: Zero-dependency 6-Bit Combinatorial State Machine, 3-Coin vs 50-Stalk
Probability Simulator, Zhu Xi 7-Level Changing-Line Hierarchy, and True Solar Time Engine.

Reference Workbench & Documentation: https://hexsage.ai/
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union

__version__ = "1.1.0"

_DATA_PATH = Path(__file__).resolve().parent / "hexagrams_64_binary.json"
_RAW_DATA = json.loads(_DATA_PATH.read_text(encoding="utf-8"))
HEXAGRAMS: List[Dict[str, Any]] = _RAW_DATA["hexagrams"]

_BY_KING_WEN: Dict[int, Dict[str, Any]] = {h["king_wen"]: h for h in HEXAGRAMS}
_BY_BITS: Dict[str, Dict[str, Any]] = {h["bits_L1_to_L6"]: h for h in HEXAGRAMS}

TRIGRAMS: Dict[int, tuple[str, str]] = {
    1: ("Qian", "111"),
    2: ("Dui", "110"),
    3: ("Li", "101"),
    4: ("Zhen", "100"),
    5: ("Xun", "011"),
    6: ("Kan", "010"),
    7: ("Gen", "001"),
    8: ("Kun", "000"),
}

PROBABILITY_3COIN: Dict[int, float] = {6: 2 / 16, 7: 6 / 16, 8: 6 / 16, 9: 2 / 16}
PROBABILITY_50STALK: Dict[int, float] = {6: 1 / 16, 7: 5 / 16, 8: 7 / 16, 9: 3 / 16}


def lookup_hexagram(key: Union[int, str]) -> Dict[str, Any]:
    """Lookup a King Wen hexagram by number (1..64) or 6-bit string L1..L6 ('000000'..'111111')."""
    if isinstance(key, int):
        if key not in _BY_KING_WEN:
            raise ValueError(f"King Wen index must be 1..64, got {key}")
        return dict(_BY_KING_WEN[key])
    s = str(key).strip()
    if len(s) == 6 and set(s) <= {"0", "1"}:
        return dict(_BY_BITS[s])
    if s.isdigit() and int(s) in _BY_KING_WEN:
        return dict(_BY_KING_WEN[int(s)])
    raise ValueError(f"Invalid hexagram key: {key!r}")


def three_coin_line(rng: random.Random = random) -> int:
    """Three independent Bernoulli coin throws -> {6: 2/16, 7: 6/16, 8: 6/16, 9: 2/16}."""
    return sum(3 if rng.random() < 0.5 else 2 for _ in range(3))


def yarrow_stalk_line(rng: random.Random = random) -> int:
    """Classical 49-active-stalk 3-change remainder protocol -> {6: 1/16, 7: 5/16, 8: 7/16, 9: 3/16}."""
    stalks = 49
    for _ in range(3):
        left = rng.randint(1, stalks - 1)
        right = stalks - left - 1
        rem_left = left % 4 or 4
        rem_right = right % 4 or 4
        stalks -= 1 + rem_left + rem_right
    return stalks // 4


def zhu_xi_changing_lines_rule(lines: Sequence[int]) -> Dict[str, Any]:
    """
    Apply Song-dynasty scholar Zhu Xi's (Yixue Qimeng) 7-case changing-line hierarchy
    to six bottom-to-top line values in {6, 7, 8, 9}.
    """
    if len(lines) != 6 or any(v not in (6, 7, 8, 9) for v in lines):
        raise ValueError("lines must be a 6-element sequence of values in {6, 7, 8, 9}")

    primary_bits = "".join("1" if v in (7, 9) else "0" for v in lines)
    relating_bits = "".join("0" if v == 9 else ("1" if v == 6 else ("1" if v == 7 else "0")) for v in lines)
    moving = [i + 1 for i, v in enumerate(lines) if v in (6, 9)]
    unchanging = [i + 1 for i, v in enumerate(lines) if v in (7, 8)]
    k = len(moving)

    primary_hex = lookup_hexagram(primary_bits)
    relating_hex = lookup_hexagram(relating_bits)

    if k == 0:
        anchor = "primary_judgment"
        rule = "0 moving lines (Unchanging Hexagram): read the Primary Hexagram Judgment & Image."
    elif k == 1:
        anchor = f"primary_line_{moving[0]}"
        rule = f"1 moving line: read Line {moving[0]} of Primary Hexagram #{primary_hex['king_wen']}."
    elif k == 2:
        anchor = f"primary_lines_{moving[0]}_{moving[1]}_upper_prevails"
        rule = f"2 moving lines: read Lines {moving[0]} and {moving[1]} of Primary Hexagram, with upper Line {moving[1]} prevailing."
    elif k == 3:
        anchor = "primary_and_relating_judgments"
        rule = "3 moving lines: weigh both Primary Judgment (foundation) and Relating Judgment (trajectory)."
    elif k == 4:
        anchor = f"relating_unchanging_lines_{unchanging[0]}_{unchanging[1]}_lower_prevails"
        rule = f"4 moving lines: read the two unchanging Lines {unchanging[0]} and {unchanging[1]} in Relating Hexagram #{relating_hex['king_wen']}, with lower Line {unchanging[0]} prevailing."
    elif k == 5:
        anchor = f"relating_unchanging_line_{unchanging[0]}"
        rule = f"5 moving lines: read the single unchanging Line {unchanging[0]} of Relating Hexagram #{relating_hex['king_wen']}."
    else:
        if primary_bits == "111111":
            anchor = "qian_all_nines_yong_jiu"
            rule = "6 moving lines in #1 Qian: read 'All Nines (Yong Jiu) — Flight of dragons without heads'."
        elif primary_bits == "000000":
            anchor = "kun_all_sixes_yong_liu"
            rule = "6 moving lines in #2 Kun: read 'All Sixes (Yong Liu) — Lasting perseverance'."
        else:
            anchor = "relating_judgment"
            rule = f"6 moving lines: read the Judgment of Relating Hexagram #{relating_hex['king_wen']}."

    return {
        "lines": list(lines),
        "moving_count": k,
        "is_unchanging": k == 0,
        "moving_lines": moving,
        "hamming_distance": k,
        "primary": primary_hex,
        "relating": relating_hex,
        "zhu_xi_anchor": anchor,
        "zhu_xi_rule": rule,
    }


def cast_hexagram(method: str = "yarrow", seed: Optional[int] = None) -> Dict[str, Any]:
    """Cast a full 6-line hexagram using 'yarrow' (1:5:7:3) or '3coin' (2:6:6:2) protocol."""
    rng = random.Random(seed) if seed is not None else random
    m = method.lower().strip()
    if m in ("yarrow", "50stalk", "stalks"):
        lines = [yarrow_stalk_line(rng) for _ in range(6)]
    elif m in ("3coin", "coins", "coin"):
        lines = [three_coin_line(rng) for _ in range(6)]
    else:
        raise ValueError("method must be 'yarrow' or '3coin'")
    res = zhu_xi_changing_lines_rule(lines)
    res["method"] = m
    return res


def shao_yong_cast(n1: int, n2: int) -> Dict[str, Any]:
    """Deterministic Shao Yong two-number modulo coordinate mapping on Q6."""
    upper_idx = ((n1 - 1) % 8) + 1
    lower_idx = ((n2 - 1) % 8) + 1
    moving_line = ((n1 + n2 - 1) % 6) + 1
    bits = list(TRIGRAMS[lower_idx][1] + TRIGRAMS[upper_idx][1])
    lines = [(9 if b == "1" else 6) if (idx + 1 == moving_line) else (7 if b == "1" else 8) for idx, b in enumerate(bits)]
    res = zhu_xi_changing_lines_rule(lines)
    res.update({
        "upper_trigram": TRIGRAMS[upper_idx][0],
        "lower_trigram": TRIGRAMS[lower_idx][0],
        "moving_line": moving_line,
        "primary_bits_L1_to_L6": res["primary"]["bits_L1_to_L6"],
        "resulting_bits_L1_to_L6": res["relating"]["bits_L1_to_L6"],
    })
    return res


def true_solar_time_offset_minutes(longitude_deg: float, std_meridian_deg: float, day_of_year: int) -> float:
    """Compute True Solar Time offset in minutes (longitude + Equation of Time)."""
    b_rad = math.radians(360.0 * (day_of_year - 81) / 365.0)
    eot = 9.87 * math.sin(2 * b_rad) - 7.53 * math.cos(b_rad) - 1.5 * math.sin(b_rad)
    return 4.0 * (longitude_deg - std_meridian_deg) + eot


__all__ = [
    "__version__",
    "HEXAGRAMS",
    "TRIGRAMS",
    "PROBABILITY_3COIN",
    "PROBABILITY_50STALK",
    "lookup_hexagram",
    "three_coin_line",
    "yarrow_stalk_line",
    "zhu_xi_changing_lines_rule",
    "cast_hexagram",
    "shao_yong_cast",
    "true_solar_time_offset_minutes",
]
