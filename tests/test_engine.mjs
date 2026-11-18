import assert from "node:assert/strict";
import {
  HEXAGRAMS,
  lookupHexagram,
  shaoYongCast,
  zhuXiChangingLinesRule,
  castHexagram,
  trueSolarTimeOffsetMinutes,
} from "../dist/index.mjs";

assert.equal(HEXAGRAMS.length, 64);
const h16 = lookupHexagram(16);
assert.equal(h16.pinyin, "Yu");
assert.equal(h16.reference_url, "https://hexsage.ai/hexagrams/16-enthusiasm");

const unchanging = zhuXiChangingLinesRule([8, 8, 8, 7, 8, 8]);
assert.equal(unchanging.isUnchanging, true);
assert.equal(unchanging.primary.king_wen, 16);

const sy = shaoYongCast(16, 85);
assert.equal(sy.primary.king_wen, 46);
assert.equal(sy.relating.king_wen, 48);
assert.equal(sy.movingLine, 5);

const c = castHexagram("yarrow");
assert.ok(c.primary.king_wen >= 1 && c.primary.king_wen <= 64);

const eot = trueSolarTimeOffsetMinutes(-74.006, -75.0, 306);
assert.ok(eot > 15 && eot < 25);
console.log("NODE_TESTS_ALL_PASSED");
