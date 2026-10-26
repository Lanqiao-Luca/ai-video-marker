**目的**：说明六姿态星光邮差狐狸原图集及分格参数的实际使用方式。

# 星光邮差狐狸图集

一张1536×1024原图集，取自《把星光寄给你》，含6个纸艺狐狸姿态。原图SHA见[manifest.json](manifest.json)；3列×2行、512×512分格与原alpha派生参数见[atlas-layout.json](atlas-layout.json)。分格参数不代表完整骨骼、走跑周期或口型。

```bash
python tools/asset_library.py verify --pack starlight-fox
python tools/asset_library.py preview --pack starlight-fox --out outputs/starlight-preview.png
```

可设计折星、捡星或向月亮邮局投信。此狐狸与太阳邮差包外观不同，新故事先固定一种角色身份，不按镜头交替换造型。preview仅生成联系表，新剧情仍需动画适配。PNG原字节复制、原件不变，按[MIT](../../../LICENSE)公开，不含原配乐或私人记录。

返回：[素材库](../README.md)。
