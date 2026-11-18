export interface HexagramRecord {
  king_wen: number;
  unicode: string;
  pinyin: string;
  english: string;
  upper_trigram: string;
  lower_trigram: string;
  bits_L1_to_L6: string;
  shao_yong_decimal: number;
  nuclear_bits_L1_to_L6: string;
  opposite_bits_L1_to_L6: string;
  inverted_bits_L1_to_L6: string;
  reference_url: string;
}

export type LineValue = 6 | 7 | 8 | 9;

export interface ZhuXiReadingResult {
  lines: LineValue[];
  movingCount: number;
  isUnchanging: boolean;
  movingLines: number[];
  hammingDistance: number;
  primary: HexagramRecord;
  relating: HexagramRecord;
  zhuXiAnchor: string;
  zhuXiRule: string;
}

export interface ShaoYongTransition extends ZhuXiReadingResult {
  upperTrigram: string;
  lowerTrigram: string;
  movingLine: number;
  primaryBitsL1ToL6: string;
  resultingBitsL1ToL6: string;
}

export declare const HEXAGRAMS: HexagramRecord[];
export declare const TRIGRAMS: Record<number, { name: string; bits: string }>;
export declare const PROBABILITY_3COIN: Record<LineValue, number>;
export declare const PROBABILITY_50STALK: Record<LineValue, number>;

export declare function lookupHexagram(key: number | string): HexagramRecord;
export declare function threeCoinLine(rng?: () => number): LineValue;
export declare function yarrowStalkLine(rng?: () => number): LineValue;
export declare function zhuXiChangingLinesRule(lines: LineValue[]): ZhuXiReadingResult;
export declare function castHexagram(method?: "yarrow" | "3coin", rng?: () => number): ZhuXiReadingResult & { method: string };
export declare function shaoYongCast(n1: number, n2: number): ShaoYongTransition;
export declare function trueSolarTimeOffsetMinutes(longitudeDeg: number, stdMeridianDeg: number, dayOfYear: number): number;
