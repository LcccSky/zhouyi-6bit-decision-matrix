# Zhouyi 6-Bit Combinatorial State Matrix & True Solar Time Engine (`2^6 = 64`)

An open, zero-dependency **Python & TypeScript** reference specification mapping the classical 64 hexagrams of the *Zhouyi* (*I Ching* / Book of Changes) onto a **6-bit binary hypercube** ($Q_6 = \{0, 1\}^6$), paired with exact line-generation probability distributions (`1:3:3:1` vs `1:3:5:7`) and astronomical **Equation-of-Time True Solar Time** calibration.

## Live Interactive Workbenches & Reference Modules

- **Primary Research Workbench**: [HexSage Classical Zhouyi 6-Bit Workbench](https://hexsage.ai/) — browser-based 6-line state-transition sandbox with True Solar Time calibration (no login required).
- **Structured Consultation Protocol**: [Consult the I Ching Step-by-Step Framework](https://hexsage.ai/consult-the-i-ching) — Inquiry Scope Guardrail, six-round casting matrix, and bilingual line-by-line synthesis.
- **Binomial Coin Protocol (`1:3:3:1`)**: [Three-Coin I Ching Binomial Simulator](https://hexsage.ai/i-ching-coins) — symmetric Bernoulli trial distribution across values `{6, 7, 8, 9}`.
- **Classical Stalk Remainder Protocol (`1:3:5:7`)**: [50-Stalk Yarrow Remainder Method](https://hexsage.ai/yarrow-stalk-method) — asymmetric modulo-4 division state transitions.
- **64-State Canonical Reference**: [King Wen 64-Hexagram Binary Matrix](https://hexsage.ai/i-ching-hexagrams) — complete structural lookup across all 64 vertices of $Q_6$.
- **Developer Embeds**: [Free Embeddable Zhouyi Hexagram Widgets](https://hexsage.ai/widgets) — lightweight interactive cards for research blogs and documentation sites.

---

## 1. Combinatorial Geometry on the 6-Bit Hypercube ($Q_6$)

Each hexagram state is represented from bottom line ($L_1$) to top line ($L_6$) as a 6-bit vector $s \in \{0, 1\}^6$:

- `0` = Broken line (*Yin*)
- `1` = Solid line (*Yang*)

When $k \in \{0, \dots, 6\}$ lines are marked as **moving** (`6` Old Yin `0 -> 1`, or `9` Old Yang `1 -> 0`), the primary state $s$ transitions via bitwise XOR with mask $m \in \{0, 1\}^6$ ($s' = s \oplus m$), traversing a Hamming distance $d_H(s, s') = k$ across the $64 \times 64 = 4,096$ directed transition graph.

---

## 2. Exact Line Probability Distributions (`3-Coin` vs `50-Stalk`)

| Line Value | Classical Name | Transition Operator | 3-Coin Binomial (`P`) | 50-Stalk Yarrow (`P`) |
| :---: | :--- | :--- | :---: | :---: |
| `6` | Old Yin (*Lao Yin*) | Moving Yin (`0 -> 1`) | `2 / 16` (`12.50%`) | `1 / 16` (`6.25%`) |
| `7` | Young Yang (*Shao Yang*) | Stable Yang (`1 -> 1`) | `6 / 16` (`37.50%`) | `5 / 16` (`31.25%`) |
| `8` | Young Yin (*Shao Yin*) | Stable Yin (`0 -> 0`) | `6 / 16` (`37.50%`) | `7 / 16` (`43.75%`) |
| `9` | Old Yang (*Lao Yang*) | Moving Yang (`1 -> 0`) | `2 / 16` (`12.50%`) | `3 / 16` (`18.75%`) |

Notice that under the classical 50-stalk protocol (49 active stalks after setting aside the *Taiji* stalk), Old Yang (`9`, `18.75%`) occurs three times as frequently as Old Yin (`6`, `6.25%`), whereas total moving-line probability remains invariant at $P(6) + P(9) = 4/16 = 25.0\%$ under both protocols.

---

## 3. Shao Yong Deterministic Modulo Coordinate Mapping

Given two positive integers $(N_1, N_2)$:

- **Upper Trigram Index** ($1 \dots 8$): $U = ((N_1 - 1) \bmod 8) + 1$
- **Lower Trigram Index** ($1 \dots 8$): $L = ((N_2 - 1) \bmod 8) + 1$
- **Moving Line Coordinate** ($L_1 \dots L_6$): $M = ((N_1 + N_2 - 1) \bmod 6) + 1$

### Quickstart (Python & TypeScript)

```python
from zhouyi_6bit_engine import shao_yong_cast, true_solar_time_offset_minutes

state = shao_yong_cast(16, 85)
# {'upper_trigram': 'Kun', 'lower_trigram': 'Xun', 'moving_line': 5,
#  'primary_bits_L1_to_L6': '011000', 'resulting_bits_L1_to_L6': '011010'}

offset_min = true_solar_time_offset_minutes(longitude_deg=114.1694, std_meridian_deg=120.0, day_of_year=307)
```

```typescript
import { shaoYongCast, trueSolarTimeOffsetMinutes } from "./zhouyi_6bit_engine";

const transition = shaoYongCast(16, 85);
const solarOffset = trueSolarTimeOffsetMinutes(114.1694, 120.0, 307);
```

---

## 4. Astronomical True Solar Time Calibration

Standard civil timezones quantize longitude into $15^\circ$ bands, introducing up to $\pm 30+$ minutes of solar phase error combined with orbital eccentricity. True Solar Time applies both observer longitude $\lambda_{\text{local}}$ and the Equation of Time:

$$\Delta t_{\text{solar}}(\text{min}) = 4 \times (\lambda_{\text{local}} - \lambda_{\text{zone}}) + 9.87 \sin(2B) - 7.53 \cos(B) - 1.5 \sin(B)$$

where $B = \frac{360^\circ}{365}(d - 81)$ for day-of-year $d \in [1, 365]$.

---

## License

MIT License · Maintained by the HexSage Classical Systems Research Team ([hexsage.ai](https://hexsage.ai/) · [Consult the I Ching](https://hexsage.ai/consult-the-i-ching)).
