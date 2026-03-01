# SiliconFlow 图像生成 v2.0 🎨

> [English](./README_EN.md) | [中文](./README_ZH.md)

多语言 AI 图像生成工具，集成提示词优化器。

## ✨ 功能特性

- 🎨 **文生图** - 根据文字描述生成图像
- 🖼️ **图生图** - 基于参考图生成变体
- 📝 **提示词优化** - 自动增强提示词效果
- 🎭 **风格控制** - anime, cyberpunk, chinese, photorealistic...
- 💡 **光照控制** - golden, studio, neon, natural...
- 📐 **构图建议** - wide, closeup, center...
- 🇨🇳 **中文优化** - Kolors 模型对中文支持优秀
- 💰 **高性价比** - 比 OpenAI 便宜 66%

## 🚀 快速开始

### 配置 API Key

```bash
export SILICONFLOW_API_KEY="sk-xxx"
```

获取 API Key: https://cloud.siliconflow.cn

### 安装

```bash
pip install -r requirements.txt
```

### 基本用法

```bash
# 文生图
python scripts/siliconflow-image.py "一只可爱的猫" -o cat.png

# 启用提示词优化
python scripts/siliconflow-image.py "猫" -o cat.png --optimize

# 指定风格和质量
python scripts/siliconflow-image.py "猫" -o cat.png --optimize --style anime --quality high

# 图生图
python scripts/siliconflow-image.py "变成水彩画" -o output.png --ref input.png
```

## 🎛️ 参数说明

| 参数 | 说明 | 选项 |
|------|------|------|
| `--optimize` | 启用提示词优化 | |
| `--style` | 图像风格 | anime, cyberpunk, chinese, fantasy, portrait, landscape, product |
| `--quality` | 质量级别 | high, photorealistic, illustration, 3d |
| `--lighting` | 光照风格 | golden, studio, neon, natural, dramatic |
| `--composition` | 构图方式 | wide, closeup, center, overhead |
| `--ref` | 参考图片 | 文件路径 |
| `--batch` | 批量数量 | 1-4 |

## 📦 支持的模型

| 模型 | 说明 |
|------|------|
| **Kwai-Kolors/Kolors** | 快手可灵 - 中文最佳 |
| **Qwen/Qwen-Image** | 阿里千问 - 高分辨率 |
| **Qwen/Qwen-Image-Edit** | 用于图像编辑 |

## 📜 许可证

MIT License

---

英文文档见 [README_EN.md](./README_EN.md)
