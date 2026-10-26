**目的**：说明纸艺少年与教室素材的实际文件、适配边界和复用入口。

# 纸艺少年与教室

3张PNG，来源于《把晴天折进书里-20261024》的既有原创画面/制作拆件。

character-atlas-v1为3列×2行，女孩在上、男孩在下；action-atlas-v3为6列×2行，提供有限完整姿态变化。图集需按格裁切并清理相邻格残片，绑定脚底/手部锚点后使用，不是完整骨骼或已完成的连续走跑周期。classroom-v1为完整背景。

## 文件

| 图片 | 尺寸 | 通道 |
|---|---|---|
| [classroom-v1.png](classroom-v1.png) | 1672×941 | 完整不透明图 |
| [character-atlas-v1.png](character-atlas-v1.png) | 1536×1024 | 有alpha通道 |
| [action-atlas-v3.png](action-atlas-v3.png) | 1536×1024 | 有alpha通道 |

## 使用

在仓库根执行：

```bash
python tools/asset_library.py verify --pack paper-classroom
python tools/asset_library.py preview --pack paper-classroom --out outputs/paper-classroom-preview.png
```

可把“教室相遇、传递纸条或共同完成纸艺作品”作为新的分镜方向，先验证代表段。这里只提供素材与静态联系表，不附该新故事的一键影片渲染器；AI须适配动作/镜头和合成实现。透明通道存在不证明已经正确分层、绑定或获得艺术采用。

图像按[MIT](../../../LICENSE)随仓库公开，未包含原曲、语音、参考媒体或原始会话；源原件保持不变。尺寸和源/公开SHA见[manifest.json](manifest.json)，本批文件为原字节复制。

返回：[素材库](../README.md)。
