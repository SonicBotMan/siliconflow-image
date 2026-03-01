# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-03-01

### ✨ Added
- **Prompt Optimizer** - Integrated Image Prompt Optimizer functionality
  - `--optimize` flag to enable prompt optimization
  - `--style` for style selection (anime, cyberpunk, chinese, fantasy, portrait, landscape, product)
  - `--quality` for quality level (high, photorealistic, illustration, 3d)
  - `--lighting` for lighting control (golden, blue, studio, neon, natural, dramatic)
  - `--composition` for composition (wide, closeup, center, overhead)
- **Smart Negative Prompts** - Auto-generate negative prompts based on quality level

### 🔄 Changed
- Improved Chinese language support for Kolors model
- Better negative prompt generation

### 📝 Examples
```bash
# Basic optimization
python siliconflow-image.py "猫" -o cat.png --optimize

# Full control
python siliconflow-image.py "少女" -o girl.png --optimize --style anime --quality high --lighting golden
```

---

## [1.0.0] - 2026-02-13

### ✨ Added
- Initial release
- Text-to-image generation
- Image-to-image generation
- Support for Kolors and Qwen models
- Multiple resolution options
- Batch generation support
