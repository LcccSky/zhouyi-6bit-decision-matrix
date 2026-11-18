import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from zhouyi_6bit import (
    HEXAGRAMS,
    lookup_hexagram,
    shao_yong_cast,
    zhu_xi_changing_lines_rule,
    cast_hexagram,
    true_solar_time_offset_minutes,
)

assert len(HEXAGRAMS) == 64
h16 = lookup_hexagram(16)
assert h16["pinyin"] == "Yu" and h16["reference_url"] == "https://hexsage.ai/hexagrams/16-enthusiasm"

# Test unchanging hexagram (0 moving lines)
unchanging = zhu_xi_changing_lines_rule([8, 8, 8, 7, 8, 8])  # 000100 -> #16 Yu unchanging!
assert unchanging["is_unchanging"] is True
assert unchanging["primary"]["king_wen"] == 16
assert unchanging["zhu_xi_anchor"] == "primary_judgment"

# Test Shao Yong [16, 85] -> #46 Sheng to #48 Jing (Line 5 moving)
sy = shao_yong_cast(16, 85)
assert sy["primary"]["king_wen"] == 46
assert sy["relating"]["king_wen"] == 48
assert sy["moving_line"] == 5

# Test seeded yarrow cast
c = cast_hexagram("yarrow", seed=42)
assert 1 <= c["primary"]["king_wen"] <= 64

eot = true_solar_time_offset_minutes(-74.006, -75.0, 306)
assert 15.0 < eot < 25.0
print("PYTHON_TESTS_ALL_PASSED")
