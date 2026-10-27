**目的**：帮助使用者运行、理解并扩展这套 AI 视频制作工作流。

# ai-video-marker

把创意交给 AI，按流程做一支可以修改、可以接续的视频。

这里包含 **Graph → Loop → Workflow → Agent → Skill → Standards** 六层制作方法，以及制作模板、本地工具和三个可独立运行的像素场景。简单任务直接从Workflow开始，复杂依赖/重复修订才启用Graph/Loop。AI组织阶段工作和调用工具，使用者确认创作方向与最终采用版本。

![像素示例：屋顶晒太阳](docs/images/rooftop-preview.gif)

*《屋顶晒太阳》：小兔集雨、解开水轮卡点，带动齿轮花开放，最后同一屋顶共同活动。以上为16–30秒原速节选；[44秒完整带音乐视频](examples/pixel/preview.mp4)。示例直接抽取真实作品绘图代码，保留角色、层次、动作和镜头。*

**0.3.1**：新增可观看的AI漫画案例《雨夜最后一班电车》，公开成片展示版和一张视频封面，原图、分离音轨及工程留在本地。六层框架、8条内容流程（5正式、3候选）与3个可运行像素场景保持。详见[升级说明](docs/FRAMEWORK_UPGRADE.md)与[发布范围](docs/RELEASE_REVIEW.md)。

## AI漫画案例：雨夜最后一班电车

[![雨夜最后一班电车，点击封面查看完整视频](examples/reference-comic/poster.jpg)](examples/reference-comic/preview.mp4)

[▶ 查看或下载完整视频（约30秒，1080p，带原创配乐）](examples/reference-comic/preview.mp4) · [制作说明](examples/reference-comic/README.md)

六幅新生成漫画讲述雨夜站台上的一次停留。实际制作路径是**运镜/字幕预合成 → 剪映添加片名并导出**，属于漫画有限运镜的混合制作展示；原素材和剪映工程没有随视频上传。想制作自己的案例，可沿[参考音轨与AI漫画流程](workflows/参考音轨与AI漫画剪映短视频制作.md)开始。

## 先挑一个案例：复制文字就能开场

[打开12个案例开场文案](examples/story-starters/README.md)，每个都有一句片头文案和一段可复制给AI的制作需求。可以直接在GitHub网页阅读，先挑题材，无需为阅读文案下载素材。

| 想做的方向 | 文字案例 |
|---|---|
| 温暖故事 | 没有收件人的信、把晚霞留到明天 |
| 像素短片 | 红绿灯休假一天、云朵面包店 |
| 定格动画 | 一枚纽扣的搬家、纸飞机的返航 |
| 古诗词学习 | 雪落在江面之前、竹子的回答 |
| 情绪诗词（候选流程） | 把没说完的话还给风、今晚允许自己慢一点 |
| 立体书剪纸（候选流程） | 借我一页海、星星住进了信封 |

这些创作案例需要AI按工作流适配分镜与实现；先给文字/分镜和代表段，确认后再扩全片。本次仅增加文字，默认机器人短片和现成素材保持。

## 做你的第一支视频

**先用仓库素材做一支与首页展示不同的视频，不用准备图片或音乐。** 用能读本地文件、执行命令的AI编程助手打开整个仓库，输入：

> 用仓库自带素材，做一支和README展示不同的视频。先做一个短预览，再导出完整视频；不要重新生成素材。

助手的默认开场是：

> 我们先用仓库新带的机器人、海港和灯塔素材，做一支《小机器人与归航灯塔》吧。它与首页展示的兔子视频不同，不用准备图片和音乐。我先检查装电池的短段，再导出完整视频；你也可以直接指定其他主题。

新手默认片是**36秒的机器人海港短片**：机器人拾起三枚电池，逐个装入控制台，点亮灯塔引导渔船归港。新的角色、道具、场景和动作均已放进仓库；[12张PNG素材及使用说明](assets/harbor/README.md)可供后续创作复用，含站立、搬运和挥手三种完整姿态以及拆分角色部件。

自己运行时，需要Python 3.9+，按下面操作：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/doctor.py
python tools/make_video.py
```

最后一条命令会选择新seed，导出到新的 `outputs/first-video-时间-seed/`，包含36秒、720×1280、24fps的 `video.mp4`、静音母版、场景配置、动作trace及运行记录。不需要API Key、Node.js或私有素材。Pillow负责程序绘图，imageio-ffmpeg提供FFmpeg；已有系统版本也可使用。

先试装电池动作，再完整导出（两次使用相同seed）：

```bash
python tools/make_video.py --seed 42 --start 7 --end 9 --out outputs/my-first-pilot
python tools/make_video.py --seed 42 --out outputs/my-first-video
python tools/check_video.py outputs/my-first-video/video.mp4 --manifest outputs/my-first-video/run.json --out outputs/my-first-video/check.json
python tools/contact_sheet.py outputs/my-first-video/video.mp4 --out outputs/my-first-video/review
```

查看其他内容：`python tools/make_video.py --list`。

| 内容 | 主角与素材 | 入口 |
|---|---|---|
| 小机器人与归航灯塔（默认） | 新机器人、12张海港PNG | `python tools/make_video.py --theme harbor` |
| 月光风铃（可选） | 小兔、音乐盒花园 | `python tools/make_video.py --theme garden` |
| 屋顶晒太阳（展示复现） | 小兔、雨水与机械屋顶 | `python tools/render_pixel.py` |

海港可选sunset/midnight/mist配色，花园可选moon/dawn/forest。例如 `python tools/make_video.py --theme harbor --palette midnight --seed 42`。配色和seed只改变视觉细节；新主题需要AI沿工作流设计并适配代码，不强制复用同一角色或剧情。详见[新手海港入口](examples/harbor/README.md)和[可选花园](examples/first-video/README.md)。

Windows创建环境可用 `py -3 -m venv .venv`，激活使用 `.venv\Scripts\activate`；当前macOS已实跑，Windows/Linux尚未实测。

如果明确想复现首页44秒展示片，使用 `python tools/render_pixel.py --out outputs/pixel-rooftop`，详见 [屋顶示例](examples/pixel/README.md)。它的原绘图函数和1056帧基线继续保留。视频解码和静态联系表不代替正常速度观看、听审或最终采用。

## 更多现成素材：从本地制作库精选10组

![第一批素材](docs/images/library-overview.jpg)

新增[素材库](assets/library/README.md)，累计含**73张PNG，约73.74MiB**：

| 素材组 | 图片数 | 可复用内容 |
|---|---:|---|
| [狐狸与獾](assets/library/woodland-friends/README.md) | 21 | 角色拆件/姿态、暖光罐、村庄和室内背景 |
| [撑伞机器人与小鸟](assets/library/rainy-umbrella/README.md) | 10 | 雨伞、雨天背景和修订后的角色部件 |
| [纸艺少年与教室](assets/library/paper-classroom/README.md) | 3 | 男女孩角色/动作图集、教室场景 |
| [竹林与山岩](assets/library/bamboo-wind/README.md) | 2 | 无字竹石远景/近景 |
| [山水与书本](assets/library/poetry-book/README.md) | 7 | 翻页三状态、山水、纸面与原图集 |
| [蜗牛与温暖灯光](assets/library/snail-lantern/README.md) | 18 | 水彩机器人和蜗牛姿态、暮色背景、地面光与阴影 |
| [晚霞房间与圆润机器人](assets/library/sunset-room/README.md) | 8 | 已选圆润机器人参考图、推凳/走路/晚霞姿态、房间和凳子 |
| [雪江与独钓渔舟](assets/library/snow-river/README.md) | 2 | 无字雪江背景与独立渔舟原画，适合冬景/诗词有限动画 |
| [太阳邮差狐狸图集](assets/library/sunmail-fox/README.md) | 1 | 狐狸邮递员与朋友/动作部件图集，按主体框拆分使用 |
| [星光邮差狐狸图集](assets/library/starlight-fox/README.md) | 1 | 六姿态纸艺狐狸原图集，适合折星、追星与送信动作适配 |

![第二批素材](docs/images/library-batch2-overview.jpg)

两批各选择5/19组，每批约26.3%，累计**10组、约52.6%**；按作品组统计，未按全库文件数或字节量计算。复制的是可复用视觉素材，未打包参考歌曲、配音、视频、雨滴缓存帧或个人记录。

```bash
python tools/asset_library.py list
python tools/asset_library.py verify
python tools/asset_library.py preview --pack woodland-friends --out outputs/woodland-preview.png
```

可以直接对AI说：“用素材库里的狐狸和獾，做一个新故事，先给我分镜和代表段；优先复用图片与包内音乐。”助手应读取相应素材清单，按工作流适配动画。**导入素材不代表已有对应的完整影片渲染器**；完整PNG、部件、图集和背景各有不同用法，预览命令生成资产联系表。默认的海港机器人短片保持不变。

## 素材从哪里来，会花多少时间和Token

制作包内三个场景都不需要原电脑的图片、角色文件或私有归档：绘图源码、场景配置和原创配乐及其生成源码均已带齐。安装依赖后可直接生成画面和声音。

创作新主题时，AI应先确认素材方式：

| 方式 | 工作与成本提示 |
|---|---|
| 复用本地已有素材 | 先给素材位置，检查可用性和来源；通常减少重新制作 |
| 复用并补缺 | 保留已有角色/风格，只制作缺少的背景、道具或动作 |
| 全部重新制作 | 可能需要更多样稿、编程/生图/配音与反复修改，通常更慢，可能消耗更多Token或调用费用 |

用户已选方式时不重复问；未选时在新素材制作前提示，先确认实际能力与预算，再做代表段。**运行三个包内场景不会额外调用大模型或生图API**，但让AI解释、修改代码或重新造素材仍会消耗对话Token。没有可靠依据时不编造耗时或价格。
详细边界见 [素材与复现说明](docs/ASSETS.md)。

## 体验之后，做自己的视频

用能读本地文件、运行命令的 AI 编程助手打开整个仓库，让它从 [AGENTS.md](AGENTS.md)进入。例如：

> 按这里的像素工作流，做一支30秒的原创短片：一座废弃的音乐盒被重新启动。先选音乐、设计物体触发机制，给我分镜与代表段，再扩成全片。新项目写到 outputs/music-box。

AI 会选择主流程，按当前阶段读取角色、技能与标准。生图、语音及剪辑软件依实际助手和本机环境提供；仓库本身不包含这些服务。音乐按真实版本、片段及可用路径处理；没有可用音频时可交静音母版，由使用者在目标平台添加音乐。

可以先初始化项目：

```bash
python tools/init_project.py --route pixel --id my-video --assets reuse --out outputs/my-video
```

这条命令以复用素材初始化制作单、镜头表、状态、反馈与像素工作表，**不会生成视频**；从零制作时明确使用--assets generate。它属于体验后的创作准备，首次运行示例无需先初始化新项目。新故事通常需要AI编写或适配渲染逻辑；屋顶示例只支持它声明的参数，不是任意故事生成器。

## 一共有多少种制作流程

按内容制作入口统计，共 **8条流程：5条正式、3条候选**。题材与表现路线可以交叉，不是互斥的八种画风；机器目录见 [catalog.json](catalog.json)。

| 类型 | 主要制作内容 | 方法状态 | 本包实际能力 |
|---|---|---|---|
| [通用故事短片](workflows/短片制作.md) | 故事、角色行动、分镜、试镜和后期 | 正式 | 流程与模板，媒体工具另核 |
| [古诗词动画](workflows/古诗词动画制作.md) | 文本字音、早期声样、逐句声画与全文复习 | 正式 | 流程与模板，媒体工具另核 |
| [定格动画](workflows/定格动画制作.md) | 路线、姿态与曝光保持、接触锚点 | 正式 | 流程与模板，拍摄/渲染能力另核 |
| [像素节奏创意短片](workflows/像素节奏创意短片制作.md) | 音乐、物体机制、累积回报与连续空间 | 正式 | 流程、12份工作表与3个可运行场景 |
| [参考音轨与AI漫画剪映](workflows/参考音轨与AI漫画剪映短视频制作.md) | 题材/目标画布、真实原声、AI插画与原生剪映剪辑 | 正式方法 | 流程、文字模板及[漫画成片展示](examples/reference-comic/README.md)；未附生图服务/剪映自动化，完整原生图片组装未验证 |
| [情绪诗词短视频](workflows/情绪诗词短视频制作.md) | 参考、情绪脚本、声样与字幕母版 | 候选 | 方法草案，尚无本包媒体实跑 |
| [歌词／短句驱动程序动画MV](workflows/歌词驱动程序动画MV制作.md) | 真实声音/文字、材质、事件与观看兑现；含纸艺分支 | 候选 | 方法与既有纸艺分支适配，无通用换歌引擎 |
| [绘画世界穿行短片](workflows/绘画世界穿行短片制作.md) | 结尾逆推路线、关键帧、代表接缝与可选画布退出 | 候选 | 方法/制作单；附局部平面合成函数，无整片穿行生成器 |

另有 **2条辅助流程**：[作品归档与复用](workflows/作品归档与复用.md)、[文档维护与原则审查](workflows/文档维护与原则审查.md)，不计入八条内容制作流程。

## 新路线：先用文字规划AI漫画剪辑

可以对AI说：“按参考音轨与AI漫画流程，先给分镜、目标画布和素材/音轨计划；暂不生成图片或下载歌曲，先列当前工具与费用未知。”或初始化：

```bash
python tools/init_project.py --route reference-comic --id night-tram --assets mixed --out outputs/night-tram
```

初始化只带入文字制作单与空记录，不生成媒体，也不操作剪映。若明确要求原生剪映，实际使用成功才记录该阶段完成；方图加柔化侧边应称背景填充版，不能冒称宽幅重绘。

制作后每次真正交视频，助手应同时给出**可见的本地全路径、推荐标题和一段可直接复制的发布描述**，并注明版本及未验范围。具体规则由声音与后期职责消费[AN11](standards/视频交付与发布文案.md)；准备文案不会自动发布，本机路径不进入公开发布正文。

## 六层如何配合

| 层 | 职责 | 何时读取 |
|---|---|---|
| [graphs](graphs/README.md) | 阶段依赖、版本状态与局部退回 | 复杂依赖需要时 |
| [loops](loops/README.md) | 定向修订、累计预算与停止出口 | 确有重复试制/返工时 |
| [workflows](workflows/README.md) | 顺序、进入条件与返工出口 | 选路线、恢复阶段 |
| [agents](agents/README.md) | 导演、美术、动画、声音、验收及维护责任 | 交接当前阶段 |
| [skills](skills/README.md) | 组合当前方法、模板和工具 | 角色处理任务 |
| [standards](standards/README.md) | 共用原则、制作方法及验收依据 | 技能命中具体问题 |

按需读取，角色可由同一助手依次承担；文档本身不创建多 Agent、不安装全局技能或启动后台调度。

```text
ai-video-marker/
├── AGENTS.md / SKILL.md / CLAUDE.md  # AI 入口
├── graphs/ / loops/                 # 可读依赖图与有限迭代合同
├── workflows/                       # 八条制作流程 + 两条辅助流程
├── agents/                          # 制作及维护职责
├── skills/                          # 八项按阶段读取的技能
├── standards/                       # 共用方法和判断依据
├── templates/                       # 通用、专题及像素12份工作表
├── assets/harbor/                  # 新机器人与海港12张PNG素材
├── tools/                           # 初始化、渲染、音频、抽帧与检查
├── examples/pixel/                  # 场景配置与可运行示例
├── docs/                            # 预览、验证、来源与发布审阅
├── examples/first-video/            # 可选创作：月光风铃
├── examples/harbor/                 # 默认新手创作：机器人灯塔
└── outputs/                         # 本机产物，默认不提交
```

Loop/Graph为助手按需消费的文档合同，本版没有自动执行器或调度服务。长任务用同一项目的计划、唯一状态、事件、产出记录跨窗口续接，按[EX01/CX01](templates/project/README.md)只展开就绪单元，不强制每次制作都填所有记录。

想试新路线可先说：“按绘画世界流程，先设计结尾、逆推路线和代表接缝输入包，先不造素材。”或初始化：

```bash
python tools/init_project.py --route painting-world --id blue-studio --assets reuse --out outputs/blue-studio
```

这会带入专题制作单和接续模板，**不会生成关键帧或影片**。图生视频/2.5D/三维的真实能力和成本需在本次环境核实；[画框退出函数](tools/README.md#painted-world)只解决可选片尾的平面合成。

## 修改与扩展

- **改屋顶示例**：复制 [scene.json](examples/pixel/scene.json)，调整取景、角色路径、支持的对象位置或编码尺寸，再用 `--scene 新配置.json --out 新目录` 渲染；背景绘图和动作时点仍保留在原绘图实现，详见 [像素示例](examples/pixel/README.md)。
- **加自己的音轨**：工具接实际音频和源偏移，画面流复制、音频编码为 AAC；不自动循环或判断使用权，见 [工具说明](tools/README.md)。
- **做新故事**：沿 workflow 设计新的场景与实现，先验证代表段。新故事先对照参考作品做可看代表段，不以重写简化画面替代已有制作能力。
- **加制作路线**：补必要 workflow、职责/skill、模板及实际风险段验证，共用标准继续单点维护。

包内包含已选示例的绘图/配置及仓库原创配乐片段，没有个人会话、账户状态或原电脑归档。配乐与源码采用MIT许可。方法适配的来源身份与边界见 [来源说明](docs/PROVENANCE.md)。

## 验证与发布状态

实际环境、验证和未验事项见 [验证记录](docs/VALIDATION.md)。源码检查：

```bash
python tools/check_package.py
python tools/check_pixel_baseline.py
python -m unittest discover -s tests -v
```

本仓库采用 [MIT许可证](LICENSE)，包含示例画面、原创配乐及生成源码。复现示例无需付费服务或全局技能安装。
