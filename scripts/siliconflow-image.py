#!/usr/bin/env python3
"""
SiliconFlow Image Generation Client with Prompt Optimizer
AI 图像生成客户端 - 支持文生图、图生图和提示词优化
"""

import argparse
import base64
import json
import os
import random
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Dict, List, Any

# API 配置
DEFAULT_BASE_URL = "https://api.siliconflow.cn/v1"
DEFAULT_MODEL = "Kwai-Kolors/Kolors"
DEFAULT_SIZE = "1024x1024"
DEFAULT_STEPS = 20
DEFAULT_GUIDANCE = 7.5

KOLORS_SIZES = ["1024x1024", "960x1280", "768x1024", "720x1440", "720x1280"]
QWEN_SIZES = ["1328x1328", "1664x928", "928x1664", "1472x1140", "1140x1472", "1584x1056", "1056x1584"]

# ============== 提示词优化器 ==============

QUALITY_KEYWORDS = {
    "high": ["high quality", "high resolution", "detailed", "highly detailed", "sharp focus", "ultra detailed", "best quality", "masterpiece"],
    "photorealistic": ["photorealistic", "hyperrealistic", "realistic", "8k", "real photo", "DSLR", "soft lighting", "high detail"],
    "illustration": ["illustration", "digital painting", "artwork", "comic style", "anime style", "2d art"],
    "3d": ["3d render", "cgi", "blender", "unreal engine", "octane render", "3d cartoon"],
}

STYLE_KEYWORDS = {
    "anime": ["anime", "manga style", "japanese anime", "flat shading"],
    "western": ["western animation", "cartoon", "pixar style"],
    "chinese": ["chinese style", "国风", "水墨画", "工笔画"],
    "cyberpunk": ["cyberpunk", "neon", "futuristic", "cityscape", "neon lights"],
    "fantasy": ["fantasy", "magical", "enchanted", "mystical"],
    "portrait": ["portrait", "close-up", "face shot", "beautiful face"],
    "landscape": ["landscape", "scenic", "panoramic", "wide shot"],
    "product": ["product photography", "studio lighting", "white background", "commercial"],
}

LIGHTING_KEYWORDS = {
    "golden": ["golden hour", "warm lighting", "sunset", "sunrise"],
    "blue": ["blue hour", "cool tones", "moonlight"],
    "studio": ["studio lighting", "professional lighting", "three-point lighting"],
    "neon": ["neon lights", "neon", "glowing", "light trails"],
    "natural": ["natural lighting", "soft light", "window light"],
    "dramatic": ["dramatic lighting", "chiaroscuro", "rim light", "backlit"],
}

COMPOSITION_KEYWORDS = {
    "center": ["centered", "对称", "center composition"],
    "wide": ["wide shot", "wide angle", "panoramic", "broad view"],
    "closeup": ["close-up", "detail shot", "macro", "extreme close-up"],
    "overhead": ["overhead shot", "top view", "bird's eye view"],
}


def optimize_prompt(prompt: str, style: Optional[str] = None, quality: str = "high",
                    lighting: Optional[str] = None, composition: Optional[str] = None) -> str:
    """优化提示词"""
    optimized = prompt.strip()
    
    if quality and quality in QUALITY_KEYWORDS:
        optimized = f"{QUALITY_KEYWORDS[quality][0]}, {optimized}"
    
    if style and style in STYLE_KEYWORDS:
        optimized = f"{optimized}, {', '.join(STYLE_KEYWORDS[style][:2])}"
    
    if lighting and lighting in LIGHTING_KEYWORDS:
        optimized = f"{optimized}, {LIGHTING_KEYWORDS[lighting][0]}"
    
    if composition and composition in COMPOSITION_KEYWORDS:
        optimized = f"{optimized}, {COMPOSITION_KEYWORDS[composition][0]}"
    
    # 中文优化
    if any('\u4e00' <= c <= '\u9fff' for c in prompt):
        optimized = f"{optimized}, best quality, masterpiece"
    
    return optimized


def generate_negative_prompt(quality: str = "high") -> str:
    """生成负面提示词"""
    base = "ugly, blurry, low quality, distorted, deformed, bad anatomy, bad hands"
    if quality == "photorealistic":
        return f"{base}, watermark, signature, text, logo, cartoon, illustration"
    return base


# ============== 图像生成 ==============

def get_api_key() -> str:
    api_key = os.environ.get("SILICONFLOW_API_KEY")
    if api_key:
        return api_key
    
    for env_path in [Path.cwd() / ".siliconflow" / ".env", Path.home() / ".siliconflow" / ".env"]:
        if env_path.exists():
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("SILICONFLOW_API_KEY="):
                        return line.split("=", 1)[1].strip('"\'')
    
    raise ValueError("未找到 SILICONFLOW_API_KEY。请设置环境变量 export SILICONFLOW_API_KEY='your-key'")


def image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def save_image_from_url(url: str, output_path: str) -> None:
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
    with open(output_path, "wb") as f:
        f.write(data)


def generate_image(prompt: str, output: str, api_key: Optional[str] = None,
                   base_url: str = DEFAULT_BASE_URL, model: str = DEFAULT_MODEL,
                   size: str = DEFAULT_SIZE, steps: int = DEFAULT_STEPS,
                   guidance: float = DEFAULT_GUIDANCE, seed: Optional[int] = None,
                   negative_prompt: Optional[str] = None, batch_size: int = 1,
                   ref_image: Optional[str] = None, optimize: bool = False,
                   style: Optional[str] = None, quality: str = "high",
                   lighting: Optional[str] = None, composition: Optional[str] = None) -> Dict[str, Any]:
    """生成图像"""
    if api_key is None:
        api_key = get_api_key()
    
    # 优化提示词
    if optimize:
        original_prompt = prompt
        prompt = optimize_prompt(prompt, style=style, quality=quality, lighting=lighting, composition=composition)
        print(f"📝 原始提示词: {original_prompt}")
        print(f"✨ 优化后: {prompt}")
    
    if not negative_prompt:
        negative_prompt = generate_negative_prompt(quality)
    
    body = {
        "model": model,
        "prompt": prompt,
        "image_size": size,
        "num_inference_steps": steps,
        "guidance_scale": guidance,
        "batch_size": batch_size,
    }
    
    if seed is not None:
        body["seed"] = seed
    if negative_prompt:
        body["negative_prompt"] = negative_prompt
    
    if ref_image:
        if model not in ["Qwen/Qwen-Image-Edit", "Qwen/Qwen-Image-Edit-2509"]:
            print(f"⚠️ 警告: {model} 可能不支持图生图，建议使用 Qwen/Qwen-Image-Edit")
        
        body["image"] = ref_image if ref_image.startswith("http") else f"data:image/png;base64,{image_to_base64(ref_image)}"
    
    url = f"{base_url}/images/generations"
    data = json.dumps(body).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP 错误: {e.code}")
        print(f"📄 响应: {e.read().decode('utf-8')}")
        raise
    
    if "data" in result and len(result["data"]) > 0:
        images = result["data"]
        saved_paths = []
        
        for i, img_data in enumerate(images):
            if "url" in img_data:
                output_path = Path(output).parent / f"{Path(output).stem}_{i}{Path(output).suffix}" if batch_size > 1 else Path(output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                print(f"📥 下载图片到: {output_path}")
                save_image_from_url(img_data["url"], str(output_path))
                saved_paths.append(str(output_path))
        
        return {"success": True, "paths": saved_paths, "model": model, "seed": images[0].get("seed")}
    else:
        return {"success": False, "error": result}


def main():
    parser = argparse.ArgumentParser(description="SiliconFlow Image Generation with Prompt Optimizer")
    parser.add_argument("prompt", help="图像描述提示词")
    parser.add_argument("-o", "--output", required=True, help="输出文件路径")
    parser.add_argument("--api-key", help="SiliconFlow API Key")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"模型名称")
    parser.add_argument("--size", default=DEFAULT_SIZE, help=f"图像尺寸")
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS, help="生成步数")
    parser.add_argument("--guidance", type=float, default=DEFAULT_GUIDANCE, help="引导强度")
    parser.add_argument("--seed", type=int, help="随机种子")
    parser.add_argument("--negative", help="负面提示词")
    parser.add_argument("--ref", "--reference", dest="ref_image", help="参考图片路径")
    parser.add_argument("--batch", "--batch-size", type=int, default=1, help="批量生成数量")
    parser.add_argument("--optimize", "-O", action="store_true", help="启用提示词优化")
    parser.add_argument("--style", choices=list(STYLE_KEYWORDS.keys()), help="图像风格")
    parser.add_argument("--quality", default="high", choices=list(QUALITY_KEYWORDS.keys()), help="质量级别")
    parser.add_argument("--lighting", choices=list(LIGHTING_KEYWORDS.keys()), help="光照风格")
    parser.add_argument("--composition", choices=list(COMPOSITION_KEYWORDS.keys()), help="构图方式")
    
    args = parser.parse_args()
    
    print(f"🎨 生成图像...")
    print(f"📝 提示词: {args.prompt}")
    print(f"📐 尺寸: {args.size}")
    print(f"🤖 模型: {args.model}")
    
    result = generate_image(
        prompt=args.prompt, output=args.output, api_key=args.api_key,
        model=args.model, size=args.size, steps=args.steps, guidance=args.guidance,
        seed=args.seed, negative_prompt=args.negative, batch_size=args.batch,
        ref_image=args.ref_image, optimize=args.optimize, style=args.style,
        quality=args.quality, lighting=args.lighting, composition=args.composition,
    )
    
    if result["success"]:
        print(f"✅ 成功! 已保存到: {', '.join(result['paths'])}")
    else:
        print(f"❌ 生成失败: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
