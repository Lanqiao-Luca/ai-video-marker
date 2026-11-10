**目的**：按类型、模块和文件定位仓库已公开素材，保留来源及真实复用范围。

# 素材中心

素材实际按 **类型 → 模块 → 文件** 存放，每个已有媒体文件只保留一份；示例配置、制作说明和检查记录仍由examples管理。

| 类型 | 模块入口 | 实际内容 |
|---|---|---|
| [图片](images/README.md) | 10个制作素材包、harbor、pixel-rooftop、garden、library、reference-comic | 原图、拆件、图集、封面、联系表及预览GIF；另有单列题材模块 |
| [视频](videos/README.md) | pixel-rooftop、reference-comic | 屋顶带声/静音成片及漫画展示片 |
| [音频](audio/README.md) | pixel-rooftop | 原创配乐WAV、source.json与NOTICE |

```text
assets/
├── images/
│   ├── harbor/                # 机器人、海港PNG与manifest
│   ├── woodland-friends/      # 图片模块，其他素材包同层
│   ├── pixel-rooftop/         # 屋顶预览/联系表
│   ├── reference-comic/       # 漫画封面
│   └── catalog.json           # 10个既有素材包的唯一目录清单
├── videos/
│   ├── pixel-rooftop/         # preview.mp4、preview-silent.mp4
│   └── reference-comic/       # preview.mp4
└── audio/
    └── pixel-rooftop/         # music.wav、source.json、NOTICE.md
```

[新增题材模块：蛊真人 / 幽魂魔尊](images/蛊真人/幽魂魔尊/README.md)，含用户指定的9张图片；与既有精选库分列，许可见该模块说明。

[题材模块：蛊真人 / 柳贯一](images/蛊真人/柳贯一/README.md)，含另5张用户指定图片，来源与许可独立声明。

[题材模块：蛊真人 / 大胡子蛊师](images/guzhenren/huzidashu/README.md)，含7张用户指定图片；本模块使用拼音路径，既有中文模块路径保持。

[题材模块：蛊真人 / Road](images/guzhenren/road/README.md)，含11张用户指定图片，保原编号、文件名与独立许可说明。

[题材模块：蛊真人 / 黄龙江](images/guzhenren/huanglongjiang/README.md)，含14张用户指定PNG，规格与许可见独立模块清单。

[题材模块：蛊真人 / 开窍大典](images/guzhenren/kaiqiaodadian/README.md)，含17张用户指定PNG，规格和许可见独立模块清单。

[题材模块：蛊真人 / 三王山](images/guzhenren/sanwangshan/README.md)，含19张用户指定PNG，规格和许可见独立模块清单。

[题材模块：动画 / 风云](images/donghua/fengyun/README.md)，含6张用户指定的黑金风格镜头参考PNG；donghua与guzhenren位于同一级，许可见独立模块说明。

同一模块跨类型使用相同模块ID，避免把各项目文件混在类型根目录。现有图片包的README、manifest及图集布局随包保存；library说明页只作逻辑索引，不另存图片或第二份catalog。

完整成片用于案例展示，不等于有独立镜头素材、分层工程或任意故事渲染器；参考漫画只公开成片与封面，未附原图和分离音轨。可复用片段按实际用途单独说明，不能把成片自动算作片段库。

新增素材也按类型/模块保存，记录实际用途、规格、来源、版本与再分发许可，必要时记录SHA。只上传本次需要且允许分发的内容；大文件按授权选择压缩展示或独立分发，缓存、临时输出与私人制作记录不直接打包。输出仍写本地outputs。

既有素材重排的对应和SHA见[迁移清单](migration-20261028.json)；该清单仅记录当次97个已公开媒体的原字节迁移。后续新增素材按各模块说明与manifest核实，不混入旧迁移统计。

## 一次检查所有已公开媒体

在仓库根运行：

```bash
python tools/check_assets.py
```

工具只读并按模块输出文件数/字节、用途与许可说明入口、重复SHA和具体错误。当前覆盖229媒体（464,409,293字节），逐一核已有来源声明与字节身份；图片含GIF各帧解码，WAV核头信息，MP4只核SHA/大小，不冒称完整声画解码。旧`asset_library.py verify`仍只检查10包73图，适合选包复用。

身份输入复用97媒体的冻结迁移账本及十四个题材模块132图的现行manifest，并交叉核图片包、harbor、漫画和音频当前声明；声明冲突会报错。迁移账本仅是历史基线：以后新增素材应附现行模块manifest并扩展本检查器的读取适配，**不改写旧迁移账本来登记新文件**。尚未接入的文件报Unregistered media，新增前先核当前授权与来源。

该检查不生成联系表或修改任何素材。重复SHA仅供人工了解，不自动删除；技术PASS不授予再利用许可，用户提供的题材图仍按各独立模块说明处理，不能套用旧图库MIT。

返回：[项目首页](../README.md)。

[三王山第二批 v2](images/guzhenren/sanwangshan/v2/README.md)：16张PNG，与原批次并存，许可见模块说明。

[动画 / 心静万事可期](images/donghua/xinjing/README.md)：6张参考PNG，规格与独立许可见模块说明。

[蛊真人 / 灰骨](images/guzhenren/huigu/README.md)：5张参考PNG，规格与独立许可见模块说明。

[动画 / 一束光](images/donghua/yishuguang/README.md)：6张参考PNG，规格与独立许可见模块说明。

[蛊真人 / 逆境](images/guzhenren/nijing/README.md)：5张用户提供PNG，规格与独立许可见模块说明。

[动画 / 守灯人](images/donghua/shoudengren/README.md)：6张参考PNG，规格和独立许可见模块说明。
