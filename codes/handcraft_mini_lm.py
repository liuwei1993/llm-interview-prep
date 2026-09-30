"""手搓最小因果语言模型：1 层 Transformer，d_model=16。"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F


# ---------- 超参 ----------
vocab_size = 256
max_seq_len = 32
d_model = 16
n_layer = 2
n_head = 4
n_inner = 64  # 4 * d_model
dropout = 0.0
assert d_model % n_head == 0


class CausalSelfAttention(nn.Module):
    def __init__(self):
        super().__init__()
        self.n_head = n_head
        self.head_dim = d_model // n_head
        self.qkv = nn.Linear(d_model, 3 * d_model)
        self.proj = nn.Linear(d_model, d_model)
        self.drop = nn.Dropout(dropout)
        # 下三角因果 mask，注册为 buffer 以便随设备移动
        mask = torch.tril(torch.ones(max_seq_len, max_seq_len))
        self.register_buffer("mask", mask.view(1, 1, max_seq_len, max_seq_len))

    def forward(self, x):
        B, T, C = x.shape
        qkv = self.qkv(x)  # (B, T, 3C)
        q, k, v = qkv.split(d_model, dim=-1)
        # (B, n_head, T, head_dim)
        q = q.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        k = k.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        v = v.view(B, T, self.n_head, self.head_dim).transpose(1, 2)

        att = (q @ k.transpose(-2, -1)) / math.sqrt(self.head_dim)
        att = att.masked_fill(self.mask[:, :, :T, :T] == 0, float("-inf"))
        att = F.softmax(att, dim=-1)
        att = self.drop(att)

        y = att @ v  # (B, n_head, T, head_dim)
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        return self.drop(self.proj(y))


class Block(nn.Module):
    def __init__(self):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = CausalSelfAttention()
        self.ln2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, n_inner),
            nn.GELU(),
            nn.Linear(n_inner, d_model),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.ffn(self.ln2(x))
        return x


class MiniLM(nn.Module):
    def __init__(self):
        super().__init__()
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(max_seq_len, d_model)
        self.drop = nn.Dropout(dropout)
        self.blocks = nn.ModuleList([Block() for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d_model)
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        assert T <= max_seq_len, f"序列长度 {T} 超过 max_seq_len={max_seq_len}"

        pos = torch.arange(T, device=idx.device)
        x = self.drop(self.tok_emb(idx) + self.pos_emb(pos))
        for block in self.blocks:
            x = block(x)
        logits = self.lm_head(self.ln_f(x))  # (B, T, vocab)

        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, vocab_size), targets.view(-1))
        return logits, loss


if __name__ == "__main__":
    torch.manual_seed(0)
    model = MiniLM()
    n_params = sum(p.numel() for p in model.parameters())
    print("结构:\n", model)
    print(f"\n总参数量: {n_params}")

    batch_size, seq_len = 2, 16
    input_ids = torch.randint(0, vocab_size, (batch_size, seq_len))
    # 语言建模：预测下一个 token，这里用同一段随机序列演示
    logits, loss = model(input_ids, targets=input_ids)

    print(f"输入形状: {input_ids.shape}")
    print(f"logits 形状: {logits.shape}")  # (2, 16, 256)
    print(f"loss: {loss.item():.4f}")
