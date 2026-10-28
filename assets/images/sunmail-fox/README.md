**目的**：说明太阳邮差角色/道具原图集及完整主体裁切参数的复用边界。

# 太阳邮差狐狸图集

一张1536×1024原图集，取自《把太阳寄给你》，含狐狸姿态、自行车、兔朋友、房屋与邮筒。PNG尺寸和源/公开SHA见[manifest.json](manifest.json)，完整主体框及alpha边界见[atlas-layout.json](atlas-layout.json)。原格不等宽，不能按固定网格盲切。

```bash
python tools/asset_library.py verify --pack sunmail-fox
python tools/asset_library.py preview --pack sunmail-fox --out outputs/sunmail-preview.png
```

可适配骑车送信、太阳邮票等新故事；图集不是骑行骨骼或完整影片引擎。preview只生成联系表。PNG原字节复制，定位参数仅保留素材名、SHA和数值框，未包含私人路径。按[MIT](../../../LICENSE)公开；原曲、配音和参考媒体不在本包内。

返回：[素材库](../../library/README.md)。
