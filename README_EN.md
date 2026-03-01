# SiliconFlow Image Generation v2.0 🎨

> [English](./README_EN.md) | [中文](./README_ZH.md)

Multilingual AI image generation tool with integrated prompt optimizer.

## ✨ Features

- 🎨 **Text-to-Image** - Generate images from text descriptions
- 🖼️ **Image-to-Image** - Generate variants from reference images  
- 📝 **Prompt Optimizer** - Auto-enhance prompts with professional techniques
- 🎭 **Style Control** - anime, cyberpunk, chinese, photorealistic...
- 💡 **Lighting Control** - golden, studio, neon, natural...
- 📐 **Composition** - wide, closeup, center...
- 🇨🇳 **Chinese Optimized** - Kolors model excels at Chinese text
- 💰 **Cost Effective** - 66% cheaper than OpenAI

## 🚀 Quick Start

### Configure API Key

```bash
export SILICONFLOW_API_KEY="sk-xxx"
```

Get your API key: https://cloud.siliconflow.cn

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```bash
# Text-to-Image
python scripts/siliconflow-image.py "A cute cat" -o cat.png

# Enable Prompt Optimization
python scripts/siliconflow-image.py "cat" -o cat.png --optimize

# Specify Style and Quality
python scripts/siliconflow-image.py "cat" -o cat.png --optimize --style anime --quality high

# Image-to-Image
python scripts/siliconflow-image.py "Convert to watercolor" -o output.png --ref input.png
```

## 🎛️ Arguments

| Argument | Description | Options |
|----------|-------------|---------|
| `--optimize` | Enable prompt optimization | |
| `--style` | Image style | anime, cyberpunk, chinese, fantasy, portrait, landscape, product |
| `--quality` | Quality level | high, photorealistic, illustration, 3d |
| `--lighting` | Lighting style | golden, studio, neon, natural, dramatic |
| `--composition` | Composition | wide, closeup, center, overhead |
| `--ref` | Reference image | file path |
| `--batch` | Batch size | 1-4 |

## 📦 Supported Models

| Model | Description |
|-------|-------------|
| **Kwai-Kolors/Kolors** | Kwai Kling - Best for Chinese |
| **Qwen/Qwen-Image** | Alibaba Qwen - High resolution |
| **Qwen/Qwen-Image-Edit** | For image editing |

## 📜 License

MIT License

---

For 中文 documentation, see [README_ZH.md](./README_ZH.md)
