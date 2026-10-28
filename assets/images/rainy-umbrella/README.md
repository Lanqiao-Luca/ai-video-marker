**目的**：说明撑伞机器人与小鸟素材的实际文件、适配边界和复用入口。

# 撑伞机器人与小鸟

10张PNG，来源于《把伞分你一半》的既有原创画面/制作拆件。

取自修订后的制作拆件，保留原画布坐标；head/body/upper/fore/hand及clean肩盖需要按alpha边界、关节锚点和遮挡组装，不保证满屏直接叠放即可得到正常姿态。umbrella为道具，bird为角色，shadow为地面阴影。雨滴序列、旧肩盖与试错版本未纳入。

## 文件

| 图片 | 尺寸 | 通道 |
|---|---|---|
| [background.png](background.png) | 1920×1080 | 有alpha通道 |
| [bird.png](bird.png) | 1920×1080 | 有alpha通道 |
| [body.png](body.png) | 1920×1080 | 有alpha通道 |
| [fore.png](fore.png) | 1920×1080 | 有alpha通道 |
| [hand.png](hand.png) | 1920×1080 | 有alpha通道 |
| [head.png](head.png) | 1920×1080 | 有alpha通道 |
| [shadow.png](shadow.png) | 1920×1080 | 有alpha通道 |
| [shoulder_joint-clean.png](shoulder_joint-clean.png) | 1920×1080 | 有alpha通道 |
| [umbrella.png](umbrella.png) | 1920×1080 | 有alpha通道 |
| [upper.png](upper.png) | 1920×1080 | 有alpha通道 |

## 使用

在仓库根执行：

```bash
python tools/asset_library.py verify --pack rainy-umbrella
python tools/asset_library.py preview --pack rainy-umbrella --out outputs/rainy-umbrella-preview.png
```

可把“雨中相遇、给小鸟遮雨或拾起雨伞”作为新的分镜方向，先验证代表段。这里只提供素材与静态联系表，不附该新故事的一键影片渲染器；AI须适配动作/镜头和合成实现。透明通道存在不证明已经正确分层、绑定或获得艺术采用。

图像按[MIT](../../../LICENSE)随仓库公开，未包含原曲、语音、参考媒体或原始会话；源原件保持不变。尺寸和源/公开SHA见[manifest.json](manifest.json)，本批文件为原字节复制。

返回：[素材库](../../library/README.md)。
