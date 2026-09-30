from transformers import GPT2Config, GPT2LMHeadModel
import torch

# 创建一个极小的 GPT-2 配置
mini_config = GPT2Config(
    vocab_size=1000,        # 极小词表
    n_positions=64,         # 极短序列长度
    n_embd=64,              # 极小嵌入维度
    n_layer=2,              # 仅2层
    n_head=2,               # 2个注意力头
    n_inner=128,            # 极小前馈网络维度
    activation_function="gelu",
    resid_pdrop=0.1,
    embd_pdrop=0.1,
    attn_pdrop=0.1,
)

print("模型配置:")
print(mini_config)

# 从配置创建模型（不会下载预训练权重）
model = GPT2LMHeadModel(mini_config)

print("\n模型结构:")
print(model)
print("\n总参数量:", sum(p.numel() for p in model.parameters()))

# 创建随机输入 (模拟token IDs)
batch_size = 2
seq_length = 16
input_ids = torch.randint(0, 1000, (batch_size, seq_length))

print(f"\n输入形状: {input_ids.shape}")

# 前向传播
with torch.no_grad():
    outputs = model(input_ids, labels=input_ids)  # shape=b*20*4096

print(f"输出logits形状: {outputs.logits.shape}")
print(f"损失: {outputs.loss.item():.4f}")
