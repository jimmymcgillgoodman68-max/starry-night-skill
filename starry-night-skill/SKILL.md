---
name: starry-night-skill
description: Batch-transform uploaded photos into oil paintings inspired by Vincent van Gogh's The Starry Night, then create one independently mounted original-plus-effect comparison PNG per input. Use for 星月夜风格、梵高星空风格、Starry Night photo conversion, or ordered batch comparison requests. Do not use for unrelated Van Gogh styles or when the user wants only a standalone painting without the original comparison.
---

# 星月夜照片对照

按上传顺序逐张处理照片。每张输入只对应一张最终成品，成品只包含未经修改的当前原图和它自己的《星月夜》风格效果图。

## 工作流

1. 建立输入清单并保留上传顺序。不要把不同照片交给同一次生成或放进同一张画布。
2. 逐张检查原图方向、像素尺寸、构图、主体和主要几何结构。
3. 每张原图单独调用一次内置图像生成工具，使用编辑/风格转换模式。生成前读取并套用 [风格提示规范](references/style-prompt.md)：
   - 当前原图是唯一内容依据和唯一编辑目标。
   - 只生成效果图，不让生成工具制作对照排版。
   - 明确要求输出与原图相同的画幅比例、完整视野和主体位置。
   - 不得凭空加入星星、月亮、柏树、村庄、教堂、人物、文字或水印。
4. 检查效果图：构图、地标、人物、主体数量和相对位置必须可辨且对应。效果图与原图的宽高比差异不得超过 0.25%；否则用更强的画幅锁定提示重新生成一次。仍不合格时不要静默拉伸或大幅裁切。
5. 用 `scripts/compose_comparison.py` 制作最终 PNG，而不是让生成模型重画原图区域：

   ```bash
   python3 scripts/compose_comparison.py \
     --original "/absolute/path/input.jpg" \
     --effect "/absolute/path/effect.png" \
     --output "/absolute/path/input_starry_night_comparison.png"
   ```

6. 横版原图上下排列，原图在上、效果图在下；竖版和正方形原图左右排列，原图在左、效果图在右。脚本负责暖白画布、间隔、留白、细描边和原图像素校验。
7. 完成全部输入后再交付。最终只展示按输入顺序排列的独立对照 PNG；不要额外展示单独原图、单独效果图或中间过程。

## 输出约束

- 输入 N 张，最终必须输出且只输出 N 张独立对照成品。
- 默认文件名为 `<原文件名>_starry_night_comparison.png`；遇到同名文件时加入顺序号，禁止覆盖或遗漏。
- 输出必须是高清 PNG。画布背景 `#F7F4EE`，描边 `#E5E0D7`。
- 不添加标题、编号、标签、说明文字、投影、签名、Logo、水印或装饰。
- 不在处理途中询问是否继续；按顺序自动完成剩余图片。

## 验收

- 数量和顺序与输入一一对应。
- 每张成品只含当前原图及其效果图。
- 原图区域来自真实原始文件，不经过生成模型。
- 两个图像区域的显示尺寸和比例一致，均完整、清晰且不重叠。
- 效果图具有深蓝与金黄对比、厚涂画布肌理、短促弯曲笔触和旋涡式运动感，同时保持原图内容准确可辨。
