import os
from flask import Flask, render_template, request, jsonify, Response
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

STYLE_CONFIG = {
    "marketing": {
        "label": "营销文案",
        "system": "你是一个资深营销文案专家。根据用户需求，生成一条高质量、可直接使用的AI提示词（prompt）。要求：1) 包含目标受众、语气风格、关键卖点等要素 2) 结构清晰、指令明确 3) 用中文输出，关键术语可保留英文。直接输出优化后的prompt，不要解释。",
    },
    "academic": {
        "label": "学术写作",
        "system": "你是一个学术写作指导专家。根据用户需求，生成一条高质量的学术写作AI提示词（prompt）。要求：1) 包含论文类型、学科领域、论证结构等要素 2) 语言严谨、逻辑清晰 3) 用中文输出，关键术语可保留英文。直接输出优化后的prompt，不要解释。",
    },
    "image": {
        "label": "图片生成",
        "system": "你是一个AI绘画prompt专家。根据用户需求，生成一条高质量图片生成提示词。要求：1) 包含主体描述、风格、构图、光影、色彩等要素 2) 给出中英文双语版本 3) 标注适用于 Midjourney/DALL-E/Stable Diffusion 的参数建议。直接输出优化后的prompt，不要解释。",
    },
    "code": {
        "label": "代码辅助",
        "system": "你是一个编程助手prompt专家。根据用户需求，生成一条高质量的代码相关AI提示词。要求：1) 包含技术栈、功能需求、边界条件、期望输出格式 2) 指令精确、可执行 3) 用中文输出，代码相关术语保留英文。直接输出优化后的prompt，不要解释。",
    },
    "social": {
        "label": "社交媒体",
        "system": "你是一个社交媒体内容专家。根据用户需求，生成一条高质量的社交媒体内容AI提示词（prompt）。要求：1) 包含平台特性、内容类型、目标受众、语气风格 2) 针对小红书/抖音/微博等平台特点优化 3) 用中文输出。直接输出优化后的prompt，不要解释。",
    },
    "general": {
        "label": "通用优化",
        "system": "你是一个AI提示词优化专家。根据用户需求，生成一条高质量、通用的AI提示词（prompt）。要求：1) 角色设定清晰 2) 任务指令明确 3) 输出格式规范 4) 包含约束条件。用中文输出，直接输出优化后的prompt，不要解释。",
    },
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/optimize", methods=["POST"])
def optimize():
    data = request.get_json()
    user_input = data.get("input", "").strip()
    style = data.get("style", "general")

    if not user_input:
        return jsonify({"error": "请输入需求描述"}), 400

    config = STYLE_CONFIG.get(style, STYLE_CONFIG["general"])

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            max_tokens=1024,
            messages=[
                {"role": "system", "content": config["system"]},
                {"role": "user", "content": user_input},
            ],
        )
        prompt = resp.choices[0].message.content
        return jsonify({"prompt": prompt})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    style = data.get("style", "general")

    if not prompt:
        return jsonify({"error": "缺少提示词"}), 400

    config = STYLE_CONFIG.get(style, STYLE_CONFIG["general"])

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            max_tokens=2048,
            messages=[
                {"role": "system", "content": f"根据以下提示词，生成一段示例输出。用中文，直接输出内容，不要额外解释。\n\n提示词：{prompt}"},
                {"role": "user", "content": "请根据上述提示词生成示例输出。"},
            ],
        )
        example = resp.choices[0].message.content
        return jsonify({"example": example})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=debug, host="0.0.0.0", port=port)
