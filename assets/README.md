**目的**：按类型、模块和文件定位仓库已公开素材，保留来源及真实复用范围。

# 素材中心

素材实际按 **类型 → 模块 → 文件** 存放，每个已有媒体文件只保留一份；示例配置、制作说明和检查记录仍由examples管理。

| 类型 | 模块入口 | 实际内容 |
|---|---|---|
| [图片](images/README.md) | 10个制作素材包、harbor、pixel-rooftop、garden、library、reference-comic | 原图、拆件、图集、封面、联系表及预览GIF |
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

同一模块跨类型使用相同模块ID，避免把各项目文件混在类型根目录。现有图片包的README、manifest及图集布局随包保存；library说明页只作逻辑索引，不另存图片或第二份catalog。

完整成片用于案例展示，不等于有独立镜头素材、分层工程或任意故事渲染器；参考漫画只公开成片与封面，未附原图和分离音轨。可复用片段按实际用途单独说明，不能把成片自动算作片段库。

新增素材也按类型/模块保存，记录实际用途、规格、来源、版本与再分发许可，必要时记录SHA。只上传本次需要且允许分发的内容；大文件按授权选择压缩展示或独立分发，缓存、临时输出与私人制作记录不直接打包。输出仍写本地outputs。

本次只迁移已公开文件，媒体原字节未改，无新素材生成或重编码。迁移对应和SHA见[迁移清单](migration-20261028.json)，运行工具与示例入口已更新。

返回：[项目首页](../README.md)。
