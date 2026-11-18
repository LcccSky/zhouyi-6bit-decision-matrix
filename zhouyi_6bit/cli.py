"""Command-line interface for zhouyi-6bit."""
import argparse
import json
from . import cast_hexagram, lookup_hexagram, shao_yong_cast


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="zhouyi-6bit",
        description="Zhouyi (I Ching) 6-Bit Combinatorial State Machine & Yarrow/3-Coin Simulator (https://hexsage.ai/)",
    )
    parser.add_argument("--method", choices=["yarrow", "3coin"], default="yarrow", help="Line probability protocol")
    parser.add_argument("--seed", type=int, default=None, help="Optional deterministic PRNG seed")
    parser.add_argument("--shao-yong", nargs=2, type=int, metavar=("N1", "N2"), help="Cast via Shao Yong two-number coordinates")
    parser.add_argument("--hex", type=str, default=None, help="Lookup King Wen hexagram (1..64 or 6-bit string)")
    args = parser.parse_args()

    if args.hex:
        out = lookup_hexagram(args.hex)
    elif args.shao_yong:
        out = shao_yong_cast(args.shao_yong[0], args.shao_yong[1])
    else:
        out = cast_hexagram(method=args.method, seed=args.seed)

    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
