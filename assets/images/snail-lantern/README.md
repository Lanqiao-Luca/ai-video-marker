**目的**：说明第二批蜗牛与灯光素材的文件、来源及实际复用边界。

# 蜗牛与温暖灯光

取自《给蜗牛留一盏灯》的18张既有PNG：3张原始背景/姿态图集、8个机器人姿态、4个蜗牛姿态及背景、阴影、地面光。图片列表、尺寸、透明通道和源/公开SHA见[manifest.json](manifest.json)。

派生图保留制作画布与坐标，蜗牛在画布中很小；使用前按alpha边界统一比例、脚底/地面接触及遮挡。完整姿态切换和位移属于有限动画，不是骨骼或逐帧新绘。

```bash
python tools/asset_library.py verify --pack snail-lantern
python tools/asset_library.py preview --pack snail-lantern --out outputs/snail-preview.png
```

可用于陪伴蜗牛、为慢行者留灯等新分镜。preview是静态资产联系表，新剧情仍需适配动画/合成实现。PNG为原字节复制，原件保持不变；按仓库[MIT](../../../LICENSE)公开，不含原曲、旁白、私人记录或第三方参考媒体。

返回：[素材库](../../library/README.md)。
