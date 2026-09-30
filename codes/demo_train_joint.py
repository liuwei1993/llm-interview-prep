"""从 train_data.jsonl 联合训练：大小写 + 10 以内四则。

格式统一为 left=right\\n，只监督 '=' 右侧（含换行）。
推理：输入 left，拼上 '=' 后贪心生成直到 '\\n'。
"""

import json
from pathlib import Path

import torch
import torch.nn.functional as F
from safetensors.torch import save_file, load_file

from handcraft_mini_lm import MiniLM, vocab_size, max_seq_len

DATA_PATH = Path(__file__).with_name("train_data.jsonl")
WEIGHTS_PATH = Path(__file__).with_name("mini_lm_joint.safetensors")


def encode(s: str) -> torch.Tensor:
    return torch.tensor([ord(c) for c in s], dtype=torch.long)


def load_data(path: Path):
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    return rows


def example_to_xy(left: str, right: str):
    """只对答案（及结尾 \\n）算 loss。"""
    text = f"{left}={right}\n"
    ids = encode(text)
    x = ids[:-1]
    y = ids[1:].clone()
    y[: len(left)] = -100  # 屏蔽预测 left 内部字符与 '='
    return x, y


def make_batch(data, math_data, case_data, batch_size: int = 64):
    """一半 math、一半 case，避免被大小写任务带偏。"""
    half = batch_size // 2
    xs, ys = [], []
    for pool, n in ((math_data, half), (case_data, batch_size - half)):
        idxs = torch.randint(0, len(pool), (n,))
        for i in idxs.tolist():
            r = pool[i]
            x, y = example_to_xy(r["left"], r["right"])
            xs.append(x)
            ys.append(y)
    T = max(t.size(0) for t in xs)
    assert T <= max_seq_len
    x_pad = torch.zeros(batch_size, T, dtype=torch.long)
    y_pad = torch.full((batch_size, T), -100, dtype=torch.long)
    for i, (x, y) in enumerate(zip(xs, ys)):
        x_pad[i, : x.size(0)] = x
        y_pad[i, : y.size(0)] = y
    return x_pad, y_pad


@torch.no_grad()
def generate(model: MiniLM, left: str, max_new: int = 8) -> str:
    """输入 'cat' 或 '3+5'，输出 'CAT' 或 '8'。"""
    model.eval()
    ids = encode(left + "=").unsqueeze(0)
    for _ in range(max_new):
        logits, _ = model(ids[:, -max_seq_len:])
        next_id = logits[0, -1].argmax().item()
        ids = torch.cat([ids, torch.tensor([[next_id]])], dim=1)
        if next_id == ord("\n"):
            break
    out = "".join(chr(i) for i in ids[0, len(left) + 1 :].tolist())
    return out.rstrip("\n")


def main():
    if not DATA_PATH.exists():
        raise SystemExit(f"缺少 {DATA_PATH}，请先运行: python3 build_train_data.py")

    data = load_data(DATA_PATH)
    math_data = [r for r in data if r["task"] == "math"]
    case_data = [r for r in data if r["task"] == "case"]
    # 去重后的唯一算式（文件里 math 可能重复多份）
    uniq_math = {(r["left"], r["right"]) for r in math_data}
    print(
        f"加载 {len(data)} 条 | math文件行={len(math_data)} "
        f"唯一算式={len(uniq_math)} | case={len(case_data)}"
    )

    torch.manual_seed(0)
    model = MiniLM()
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3)

    case_demos = ["a", "z", "hi", "cat", "hello", "pytorch"]
    math_demos = ["3+5", "3-5", "4*3", "8/2", "0-7", "10*10", "9/3", "6/2"]

    print("训练前:")
    for w in case_demos:
        print(f"  {w} -> {generate(model, w)!r}")
    for e in math_demos:
        print(f"  {e} -> {generate(model, e)!r}")

    model.train()
    steps = 12000
    for step in range(steps):
        x, y = make_batch(data, math_data, case_data, 64)
        logits, _ = model(x)
        loss = F.cross_entropy(
            logits.view(-1, vocab_size), y.view(-1), ignore_index=-100
        )
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 2000 == 0 or step == steps - 1:
            print(f"step {step:5d}  loss={loss.item():.4f}")

    print("\n训练后 case:")
    for w in case_demos:
        print(f"  {w} -> {generate(model, w)!r}")
    print("训练后 math:")
    for e in math_demos:
        print(f"  {e} -> {generate(model, e)!r}")

    # 全量唯一算式准确率
    ok = 0
    for left, right in uniq_math:
        if generate(model, left) == right:
            ok += 1
    print(f"\nmath 全量准确率: {ok}/{len(uniq_math)} = {ok / len(uniq_math):.1%}")

    save_file(model.state_dict(), str(WEIGHTS_PATH))
    print(f"已保存: {WEIGHTS_PATH}")


if __name__ == "__main__":
    main()
