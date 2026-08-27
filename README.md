# 星月夜 Skill

一个可直接安装到 Codex 的照片风格转换 Skill：按上传顺序逐张生成梵高《星月夜》视觉语言的油画效果，并为每张输入单独输出“未经修改的原图＋对应效果图”高清 PNG。

## 特点

- 一张输入对应一张独立成品，支持连续批量处理。
- 原图区域由确定性排版脚本直接复制，不交给生成模型重画。
- 自动识别横版、竖版和正方形图片并选择版式。
- 锁定原始构图、地标、人物、主体数量和相对位置。
- 不凭空添加星星、月亮、柏树、村庄或教堂。
- 暖白画布、统一间距和极细暖灰描边。

## 安装

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo jimmymcgillgoodman68-max/starry-night-skill \
  --path starry-night-skill
```

安装后，在新的 Codex 对话中直接调用：

```text
$starry-night-skill 请按上传顺序处理这些照片。
```

也可以直接说：

```text
把我上传的照片批量制作成星月夜风格原图对照图。
```

## 依赖

- Codex 内置图像生成能力
- Python 3
- [Pillow](https://python-pillow.org/)

如果环境中没有 Pillow：

```bash
python3 -m pip install Pillow
```

## 输出

默认文件名：

```text
<原文件名>_starry_night_comparison.png
```

横版上下排列；竖版和正方形左右排列。每张最终画布只包含一张原图及其对应效果图。

## 许可证

MIT
