# 《星月夜》风格提示规范

对每张输入照片分别构造提示。保留照片独有的主体描述，不要把多张照片的信息混在一起。

## 生成提示模板

```text
Use case: style-transfer
Asset type: standalone oil-painting effect image for a before/after comparison
Input image: the single attached photograph is the only content, geometry, and composition reference.

Primary request: Repaint this exact scene in the post-impressionist visual language of Vincent van Gogh's The Starry Night. Output ONLY the transformed oil-painting version, not a comparison layout.

Composition/framing: preserve the input image's exact [ORIENTATION] aspect ratio, full uncropped field of view, camera viewpoint, perspective, horizon, subject positions, relative scale, silhouettes, and all major geometry. Keep [PHOTO-SPECIFIC SUBJECTS AND LANDMARKS] immediately recognizable. Do not crop, expand, shift, replace, add, remove, duplicate, or merge any object.

Style/medium: authentic hand-painted oil on canvas; thick impasto; visible short, curved, directional strokes; rhythmic wave-like and swirling movement in the existing sky and atmosphere; brush directions that follow buildings, mountains, trees, roads, water, and other real forms; expressive but structurally accurate rendering; natural canvas texture. Make the result unmistakably Starry Night-inspired without copying that painting's objects or composition.

Lighting/mood: translate the scene into a luminous deep-blue evening or night atmosphere while retaining the source scene's spatial relationships and recognizability. Use ultramarine, cobalt, Prussian blue, indigo, teal, blue-green, and violet-blue, contrasted with chrome yellow, warm gold, pale lemon, ivory, and limited ochre derived from existing highlights. Avoid featureless pure black; keep layered indigo and blue-black texture in the darkest regions.

Existing-light rule: if the source contains the sun, moon, lamps, lit windows, reflections, or other real light sources, render only those existing lights with yellow or ivory cores and rhythmic halos. If no celestial body or light is visible, do not invent one; create Starry Night energy through curved atmospheric currents, color rhythm, and directional brushwork.

Constraints: preserve every important subject's identity, count, placement, pose, shape, and relative size. Buildings must not lean or melt. Faces and limbs must not deform. The result must be a genuine oil-painting transformation rather than a photographic filter.

Avoid: invented stars or moon; cypress trees, village, church, people, buildings, animals, text, signature, logo, watermark, border, or frame not present in the source; direct copying of The Starry Night composition; cartoon or anime style; thick black outlines; plastic or 3D-rendered texture; muddy colors; oversharpening; surreal deformation; changed crop or camera angle.
```

## 照片专属补充

在 `[PHOTO-SPECIFIC SUBJECTS AND LANDMARKS]` 中列出当前照片最需要锁定的内容，例如：

- 山景：山峰数量、主峰位置、雪线、山脊、前景暗部和地平线。
- 城市：可辨识地标、楼体轮廓、塔尖、道路、桥梁和建筑相对位置。
- 人物：人数、身份、面部、发型、服装、姿态、手脚和相互位置。
- 室内：墙面、门窗、家具数量、摆放、透视和光源。
- 风景：树木、河流、道路、海岸、倒影和远近层次。

只锁定原图中真实存在的内容，不补充新情节。

## 重试提示

首次结果出现构图漂移或比例错误时，在原提示末尾加入：

```text
Revision priority: match the source image's aspect ratio and full framing exactly. Restore every edge of the original field of view and every major subject to its original position. Change only paint medium, palette, light atmosphere, and brushwork. Do not crop, zoom, extend, or redesign the scene.
```

最多针对同一原因自动重试一次；不要无限生成。
