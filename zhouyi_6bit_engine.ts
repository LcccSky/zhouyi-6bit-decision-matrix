/**
 * Zhouyi 6-Bit Combinatorial State Machine & Equation-of-Time Solar Calibration
 * Zero-dependency TypeScript reference implementation for https://hexsage.ai/
 */

export interface ShaoYongTransition {
  upperTrigram: string;
  lowerTrigram: string;
  movingLine: number;
  primaryBitsL1ToL6: string;
  resultingBitsL1ToL6: string;
  hammingDistance: number;
}

export const TRIGRAMS: Record<number, { name: string; bits: string }> = {
  1: { name: "Qian", bits: "111" },
  2: { name: "Dui", bits: "110" },
  3: { name: "Li", bits: "101" },
  4: { name: "Zhen", bits: "100" },
  5: { name: "Xun", bits: "011" },
  6: { name: "Kan", bits: "010" },
  7: { name: "Gen", bits: "001" },
  8: { name: "Kun", bits: "000" },
};

/**
 * Deterministic Shao Yong two-number modulo coordinate mapping on the Q6 hypercube.
 */
export function shaoYongCast(n1: number, n2: number): ShaoYongTransition {
  const upperIdx = (((n1 - 1) % 8) + 8) % 8 + 1;
  const lowerIdx = (((n2 - 1) % 8) + 8) % 8 + 1;
  const movingLine = (((n1 + n2 - 1) % 6) + 6) % 6 + 1;

  const bits = (TRIGRAMS[lowerIdx].bits + TRIGRAMS[upperIdx].bits).split("");
  const nextBits = [...bits];
  nextBits[movingLine - 1] = bits[movingLine - 1] === "1" ? "0" : "1";

  return {
    upperTrigram: TRIGRAMS[upperIdx].name,
    lowerTrigram: TRIGRAMS[lowerIdx].name,
    movingLine,
    primaryBitsL1ToL6: bits.join(""),
    resultingBitsL1ToL6: nextBits.join(""),
    hammingDistance: 1,
  };
}

/**
 * Three independent Bernoulli coin trials -> {6: 2/16, 7: 6/16, 8: 6/16, 9: 2/16}.
 */
export function threeCoinLine(rng: () => number = Math.random): 6 | 7 | 8 | 9 {
  let sum = 0;
  for (let i = 0; i < 3; i++) {
    sum += rng() < 0.5 ? 3 : 2;
  }
  return sum as 6 | 7 | 8 | 9;
}

/**
 * Classical 49-active-stalk 3-change remainder protocol -> {6: 1/16, 7: 5/16, 8: 7/16, 9: 3/16}.
 */
export function yarrowStalkLine(rng: () => number = Math.random): 6 | 7 | 8 | 9 {
  let stalks = 49;
  for (let change = 0; change < 3; change++) {
    const left = Math.floor(rng() * (stalks - 1)) + 1;
    const right = stalks - left - 1;
    const remLeft = left % 4 === 0 ? 4 : left % 4;
    const remRight = right % 4 === 0 ? 4 : right % 4;
    stalks -= 1 + remLeft + remRight;
  }
  return (stalks / 4) as 6 | 7 | 8 | 9;
}

/**
 * Compute True Solar Time offset in minutes (observer longitude + Equation of Time).
 */
export function trueSolarTimeOffsetMinutes(
  longitudeDeg: number,
  stdMeridianDeg: number,
  dayOfYear: number
): number {
  const bRad = ((360.0 * (dayOfYear - 81)) / 365.0) * (Math.PI / 180.0);
  const eot =
    9.87 * Math.sin(2 * bRad) - 7.53 * Math.cos(bRad) - 1.5 * Math.sin(bRad);
  return 4.0 * (longitudeDeg - stdMeridianDeg) + eot;
}
