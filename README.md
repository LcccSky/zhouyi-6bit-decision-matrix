# Zhouyi 6-Bit Combinatorial State Matrix & Solar Calibration (`2^6 = 64`)

An open educational reference dataset and calculation specification mapping the classical 64 hexagrams of the *Zhouyi* (*I Ching* / Book of Changes) onto a **6-bit binary hypercube** ($L_1 \dots L_6 \in \{0, 1\}^6$), paired with classical line-generation probability distributions and Equation-of-Time True Solar Time calibration.

- **Interactive Browser Sandbox (No Login)**: [https://hexsage.ai/](https://hexsage.ai/)
- **Step-by-Step Classical Consultation Guide**: [https://hexsage.ai/consult-the-i-ching](https://hexsage.ai/consult-the-i-ching)
- **Three-Coin Binomial Simulator (`1:3:3:1`)**: [https://hexsage.ai/i-ching-coins](https://hexsage.ai/i-ching-coins)
- **50-Stalk Yarrow Remainder Protocol (`1:3:5:7`)**: [https://hexsage.ai/yarrow-stalk-method](https://hexsage.ai/yarrow-stalk-method)
- **Complete King Wen 64-Hexagram Reference**: [https://hexsage.ai/i-ching-hexagrams](https://hexsage.ai/i-ching-hexagrams)
- **Free Embeddable Hexagram Widgets**: [https://hexsage.ai/widgets](https://hexsage.ai/widgets)

## 1. Probability Distributions Across Classical Protocols

| Line Value | Classical Name | State Role | 3-Coin Binomial (`P`) | 50-Stalk Yarrow (`P`) |
| :---: | :--- | :--- | :---: | :---: |
| `6` | Old Yin (*Lao Yin*) | Moving Yin (`0 -> 1`) | `2 / 16` (`12.50%`) | `1 / 16` (`6.25%`) |
| `7` | Young Yang (*Shao Yang*) | Stable Yang (`1 -> 1`) | `6 / 16` (`37.50%`) | `5 / 16` (`31.25%`) |
| `8` | Young Yin (*Shao Yin*) | Stable Yin (`0 -> 0`) | `6 / 16` (`37.50%`) | `7 / 16` (`43.75%`) |
| `9` | Old Yang (*Lao Yang*) | Moving Yang (`1 -> 0`) | `2 / 16` (`12.50%`) | `3 / 16` (`18.75%`) |

## 2. Shao Yong Two-Number Modulo Coordinate

Given upper integer $N_1 \ge 1$ and lower integer $N_2 \ge 1$:
- Upper Trigram index: $U = ((N_1 - 1) \bmod 8) + 1$
- Lower Trigram index: $L = ((N_2 - 1) \bmod 8) + 1$
- Moving Line coordinate ($L_1 \dots L_6$): $M = ((N_1 + N_2 - 1) \bmod 6) + 1$

## 3. Equation of Time (True Solar Time) Offset

$$\Delta t_{\text{solar}}(\text{min}) = 4 \times (\lambda_{\text{local}} - \lambda_{\text{zone}}) + 9.87 \sin(2B) - 7.53 \cos(B) - 1.5 \sin(B)$$

where $B = \frac{360^\circ}{365}(d - 81)$ for day-of-year $d$.

## License

MIT License · Maintained by the HexSage Classical Systems Research Team ([hexsage.ai](https://hexsage.ai/)).
