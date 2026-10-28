**目的**：说明山水与翻页书本素材的实际文件、适配边界和复用入口。

# 山水与翻页书本

7张PNG，来源于《古诗词学习片头-20261023》的既有原创画面/制作拆件。

book-state-0/1/2是同一书本的三种状态，适合有限状态切换；landscape为透明山水，paper-background为完整纸面。book-opening-sprites和poetry-landscape保留原图集/原画，可按需要派生；三状态不等于逐帧连续翻书。

## 文件

| 图片 | 尺寸 | 通道 |
|---|---|---|
| [book-state-0.png](book-state-0.png) | 780×620 | 有alpha通道 |
| [book-state-1.png](book-state-1.png) | 780×620 | 有alpha通道 |
| [book-state-2.png](book-state-2.png) | 780×620 | 有alpha通道 |
| [landscape.png](landscape.png) | 740×485 | 有alpha通道 |
| [paper-background.png](paper-background.png) | 1920×1080 | 有alpha通道 |
| [book-opening-sprites.png](book-opening-sprites.png) | 2172×724 | 有alpha通道 |
| [poetry-landscape.png](poetry-landscape.png) | 1448×1086 | 有alpha通道 |

## 使用

在仓库根执行：

```bash
python tools/asset_library.py verify --pack poetry-book
python tools/asset_library.py preview --pack poetry-book --out outputs/poetry-book-preview.png
```

可把“诗词片头、书中山河或翻开一本故事书”作为新的分镜方向，先验证代表段。这里只提供素材与静态联系表，不附该新故事的一键影片渲染器；AI须适配动作/镜头和合成实现。透明通道存在不证明已经正确分层、绑定或获得艺术采用。

图像按[MIT](../../../LICENSE)随仓库公开，未包含原曲、语音、参考媒体或原始会话；源原件保持不变。尺寸和源/公开SHA见[manifest.json](manifest.json)，本批文件为原字节复制。

返回：[素材库](../../library/README.md)。
