# SiliconFlow Image Generation v2.0 🎨

> AI 图像生成 + 提示词优化一体化工具

支持文生图、图生图和智能提示词优化。

## ✨ v2.0 新功能

- 🎨 **提示词优化器** - 自动增强提示词效果
- 📝 **风格选择** - anime, cyberpunk, chinese, photorealistic 等
- 💡 **光照控制** - golden, studio, neon, natural 等
- 📐 **构图建议** - wide, closeup, center 等
- 🔄 **智能负面提示词** - 自动生成高质量负面提示

## 🚀 快速开始

### 安装

```bash
pip install -r requirements.txt
```

### 配置 API Key

```bash
export SILICONFLOW_API_KEY="sk-xxx"
```

### 基本用法

```bash
# 文生图
python scripts/siliconflow-image.py "一只猫" -o cat.png

# 启用提示词优化
python scripts/siliconflow-image.py "猫" -o cat.png --optimize

# 指定风格和质量
python scripts/siliconflow-image.py "猫" -o cat.png --optimize --style anime --quality high

# 指定光照和构图
python scripts/siliconflow-image.py "风景" -o landscape.png --optimize --lighting golden --composition wide

# 图生图
python scripts/siliconflow-image.py "变成水彩画" -o output.png --ref input.png
```

## 🎛️ 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--optimize` | 启用提示词优化 | |
| `--style` | 风格 | anime, cyberpunk, chinese, fantasy |
| `--quality` | 质量 | high, photorealistic, illustration, 3d |
| `--lighting` | 光照 | golden, studio, neon, natural |
| `--composition` | 构图 | wide, closeup, center |
| `--ref` | 参考图 | 图生图模式 |
| `--batch` | 批量数量 | 1-4 |

## 📦 支持的模型

- Kwai-Kolors/Kolors (推荐中文)
- Qwen/Qwen-Image
- Qwen/Qwen-Image-Edit

## 📜 License

MIT
