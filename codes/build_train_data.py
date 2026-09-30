"""生成联合训练集：大小写转换 + 10 以内四则（整除、含负数）。

每条: {"task", "left", "right", "text"}
  text 形如  cat=CAT\\n  或  3-5=-2\\n
保存: train_data.jsonl
"""

import json
import random
import string
from pathlib import Path

OUT = Path(__file__).with_name("train_data.jsonl")
OPS = 0, 10  # 操作数闭区间


def math_examples():
    lo, hi = OPS
    rows = []
    for a in range(lo, hi + 1):
        for b in range(lo, hi + 1):
            rows.append(("math", f"{a}+{b}", str(a + b)))
            rows.append(("math", f"{a}-{b}", str(a - b)))
            rows.append(("math", f"{a}*{b}", str(a * b)))
            if b != 0 and a % b == 0:
                rows.append(("math", f"{a}/{b}", str(a // b)))
    return rows


def case_examples(n_random: int = 3000, seed: int = 0):
    rng = random.Random(seed)
    rows = []
    # 全部单字母
    for ch in string.ascii_lowercase:
        rows.append(("case", ch, ch.upper()))
    # 随机 1~8 字母
    for _ in range(n_random):
        n = rng.randint(1, 8)
        lower = "".join(rng.choice(string.ascii_lowercase) for _ in range(n))
        rows.append(("case", lower, lower.upper()))
    return rows


def main():
    math_rows = math_examples()
    # 四则只有约 400 条，复制多份避免被 case 淹没
    math_rows = math_rows * 10
    case_rows = case_examples(n_random=2000)

    rows = []
    for task, left, right in math_rows + case_rows:
        text = f"{left}={right}\n"
        rows.append({"task": task, "left": left, "right": right, "text": text})

    random.Random(0).shuffle(rows)
    with OUT.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    n_math = sum(1 for r in rows if r["task"] == "math")
    n_case = sum(1 for r in rows if r["task"] == "case")
    print(f"已写入 {OUT}")
    print(f"合计 {len(rows)} 条 (math={n_math}, case={n_case})")
    print("样例:")
    for r in rows[:5]:
        print(f"  {r['text']!r}")


if __name__ == "__main__":
    main()
