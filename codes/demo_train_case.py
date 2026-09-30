"""演示：极小 MiniLM 学会「小写 → 大写」。

真实输入输出（同长度映射，一次前向）：
  输入 cat  →  输出 CAT
不再使用 cat=CAT 续写再截取。

只监督「答案」一侧：标签就是大写串；pad 用 -100 忽略。
"""

import string
from pathlib import Path

import torch
import torch.nn.functional as F
from safetensors.torch import save_file, load_file

from handcraft_mini_lm import MiniLM, vocab_size, max_seq_len

WEIGHTS_PATH = Path(__file__).with_name("mini_lm_case.safetensors")


def encode(s: str) -> torch.Tensor:
    return torch.tensor([ord(c) for c in s], dtype=torch.long)


def make_batch(batch_size: int = 64):
    """x=小写, y=大写，逐位置对齐；只对真实字母算 loss（pad=-100）。"""
    xs, ys = [], []
    for _ in range(batch_size):
        n = torch.randint(1, 9, (1,)).item()  # 1~8
        lower = "".join(
            string.ascii_lowercase[i]
            for i in torch.randint(0, 26, (n,)).tolist()
        )
        xs.append(encode(lower))
        ys.append(encode(lower.upper()))
    T = max(x.size(0) for x in xs)
    x_pad = torch.zeros(batch_size, T, dtype=torch.long)
    y_pad = torch.full((batch_size, T), -100, dtype=torch.long)
    for i, (x, y) in enumerate(zip(xs, ys)):
        x_pad[i, : x.size(0)] = x
        y_pad[i, : y.size(0)] = y
    return x_pad, y_pad


@torch.no_grad()
def generate(model: MiniLM, lower: str) -> str:
    """输入 cat，一次前向直接得到 CAT。"""
    model.eval()
    ids = encode(lower).unsqueeze(0)
    logits, _ = model(ids)
    pred = logits.argmax(dim=-1)[0]
    return "".join(chr(i) for i in pred.tolist())


def main():
    torch.manual_seed(0)
    model = MiniLM()
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3)

    words = ["a", "z", "hi", "cat", "hello", "pytorch"]
    print("训练前（随机权重）:")
    for w in words:
        print(f"  {w} -> {generate(model, w)}")

    model.train()
    steps = 4000
    for step in range(steps):
        x, y = make_batch(64)
        logits, _ = model(x)
        # 只监督大写标签；pad 的 -100 被忽略
        loss = F.cross_entropy(
            logits.view(-1, vocab_size), y.view(-1), ignore_index=-100
        )
        opt.zero_grad()
        loss.backward()
        opt.step()
        if step % 1000 == 0 or step == steps - 1:
            print(f"step {step:4d}  loss={loss.item():.4f}")

    print("\n训练后:")
    for w in words:
        print(f"  {w} -> {generate(model, w)}")

    save_file(model.state_dict(), str(WEIGHTS_PATH))
    print(f"\n已保存: {WEIGHTS_PATH}  ({WEIGHTS_PATH.stat().st_size} bytes)")

    loaded = MiniLM()
    loaded.load_state_dict(load_file(str(WEIGHTS_PATH)))
    print("从 safetensors 加载后:")
    for w in words:
        print(f"  {w} -> {generate(loaded, w)}")


if __name__ == "__main__":
    main()
