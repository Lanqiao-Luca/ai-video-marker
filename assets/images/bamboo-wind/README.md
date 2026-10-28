**目的**：说明竹林与风雨山岩素材的实际文件、适配边界和复用入口。

# 竹林与风雨山岩

2张PNG，来源于《竹石-撑住这阵风》的既有原创画面/制作拆件。

两张均为无文字完整画面：wide偏远景，close强调根与岩石；不是透明前后景拆层。可以做推拉、字幕留白或粒子风雨等有限动画，不能将静图运动称为完整角色动画。

## 文件

| 图片 | 尺寸 | 通道 |
|---|---|---|
| [bamboo-close.png](bamboo-close.png) | 1672×941 | 完整不透明图 |
| [bamboo-wide.png](bamboo-wide.png) | 1672×941 | 完整不透明图 |

## 使用

在仓库根执行：

```bash
python tools/asset_library.py verify --pack bamboo-wind
python tools/asset_library.py preview --pack bamboo-wind --out outputs/bamboo-wind-preview.png
```

可把“竹石诗词、风雨中的坚韧或山林情绪片”作为新的分镜方向，先验证代表段。这里只提供素材与静态联系表，不附该新故事的一键影片渲染器；AI须适配动作/镜头和合成实现。透明通道存在不证明已经正确分层、绑定或获得艺术采用。

图像按[MIT](../../../LICENSE)随仓库公开，未包含原曲、语音、参考媒体或原始会话；源原件保持不变。尺寸和源/公开SHA见[manifest.json](manifest.json)，本批文件为原字节复制。

返回：[素材库](../../library/README.md)。
