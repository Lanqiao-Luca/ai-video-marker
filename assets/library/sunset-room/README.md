**目的**：说明晚霞房间与已选圆润机器人素材的文件及复用边界。

# 晚霞房间与圆润机器人

取自《窗外有晚霞》的8张PNG：A款圆润机器人原图、角色参考页、房间、凳子、推凳/走路/背向晚霞图集及晚霞窗景。未纳入未选的B款设计或失败试镜。列表、尺寸、透明通道与SHA见[manifest.json](manifest.json)。

角色原图及图集不是完整骨骼。先按格拆分、统一外观、脚底/凳面锚点与遮挡，再制作新故事；A款已选用不代表任意新组合都已采用。

```bash
python tools/asset_library.py verify --pack sunset-room
python tools/asset_library.py preview --pack sunset-room --out outputs/sunset-preview.png
```

可用于窗边等待、推来凳子看晚霞等分镜，先验证代表段。preview只生成素材联系表。PNG为原字节复制，源原件不变；按[MIT](../../../LICENSE)公开，未包含原声音、私人记录或外部参考媒体。

返回：[素材库](../README.md)。
