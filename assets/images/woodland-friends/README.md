**目的**：说明水彩狐狸与獾素材的实际文件、适配边界和复用入口。

# 水彩狐狸与獾

21张PNG，来源于《把晴天借给你-20261024》的既有原创画面/制作拆件。

角色拆件、完整坐姿/蹲姿和獾的表情/挥手姿态可组合，背景为完整画面。fox-reference与badger-reference保留原角色图集；不能把狐头/外套/手脚各当成独立完整角色。多个部件尺寸和alpha边界不同，组合前需统一缩放、设置关节锚点与遮挡。

## 文件

| 图片 | 尺寸 | 通道 |
|---|---|---|
| [badger-blink.png](badger-blink.png) | 323×533 | 有alpha通道 |
| [badger-happy.png](badger-happy.png) | 323×536 | 有alpha通道 |
| [badger-sad.png](badger-sad.png) | 341×531 | 有alpha通道 |
| [badger-wave.png](badger-wave.png) | 355×533 | 有alpha通道 |
| [fox-arm-l.png](fox-arm-l.png) | 214×296 | 有alpha通道 |
| [fox-arm-r.png](fox-arm-r.png) | 218×306 | 有alpha通道 |
| [fox-blink.png](fox-blink.png) | 397×413 | 有alpha通道 |
| [fox-body.png](fox-body.png) | 1275×1234 | 有alpha通道 |
| [fox-boot-l.png](fox-boot-l.png) | 139×220 | 有alpha通道 |
| [fox-boot-r.png](fox-boot-r.png) | 154×218 | 有alpha通道 |
| [fox-crouch.png](fox-crouch.png) | 598×542 | 有alpha通道 |
| [fox-head.png](fox-head.png) | 393×413 | 有alpha通道 |
| [fox-sit-blink.png](fox-sit-blink.png) | 561×586 | 有alpha通道 |
| [fox-sit.png](fox-sit.png) | 389×433 | 有alpha通道 |
| [fox-tail.png](fox-tail.png) | 390×322 | 有alpha通道 |
| [jar.png](jar.png) | 211×301 | 有alpha通道 |
| [plate.png](plate.png) | 1672×941 | 有alpha通道 |
| [village.png](village.png) | 1672×941 | 有alpha通道 |
| [window.png](window.png) | 1672×941 | 有alpha通道 |
| [fox-reference.png](fox-reference.png) | 1774×887 | 有alpha通道 |
| [badger-reference.png](badger-reference.png) | 1448×1086 | 有alpha通道 |

## 使用

在仓库根执行：

```bash
python tools/asset_library.py verify --pack woodland-friends
python tools/asset_library.py preview --pack woodland-friends --out outputs/woodland-friends-preview.png
```

可把“狐狸送暖光、林间拜访或同伴互助”作为新的分镜方向，先验证代表段。这里只提供素材与静态联系表，不附该新故事的一键影片渲染器；AI须适配动作/镜头和合成实现。透明通道存在不证明已经正确分层、绑定或获得艺术采用。

图像按[MIT](../../../LICENSE)随仓库公开，未包含原曲、语音、参考媒体或原始会话；源原件保持不变。尺寸和源/公开SHA见[manifest.json](manifest.json)，本批文件为原字节复制。

返回：[素材库](../../library/README.md)。
