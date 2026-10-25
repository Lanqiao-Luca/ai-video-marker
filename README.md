**目的**：帮助使用者运行、理解并扩展这套 AI 视频制作工作流。

# ai-video-marker

把创意交给 AI，按流程做一支可以修改、可以接续的视频。

这里包含 **Workflow → Agent → Skill → Standards** 四层制作方法，以及制作模板、本地工具和一个可独立运行的像素示例。AI 组织阶段工作和调用工具，使用者确认创作方向与最终采用版本。

![像素示例：屋顶晒太阳](docs/images/rooftop-preview.gif)

*《屋顶晒太阳》：小兔集雨、解开水轮卡点，带动齿轮花开放，最后同一屋顶共同活动。以上为16–30秒原速节选；[44秒完整带音乐视频](examples/pixel/preview.mp4)。示例直接抽取真实作品绘图代码，保留角色、层次、动作和镜头。*

**0.1.4**：六条制作流程、四层AI协作方法，以及可独立复现的像素动画。默认使用仓库自带画面与新编原创配乐，源码和示例采用MIT许可。其余五条路线提供方法与模板，媒体能力依实际环境核实。正式/候选表示方法状态，详见 [发布范围](docs/RELEASE_REVIEW.md)。

## 先跑起来

**第一次先用仓库自带的素材体验，不用准备自己的图片或音乐。** 下载并解压仓库，用能读取本地文件、执行命令的AI编程助手打开这个目录，输入：

> 先用这个仓库自带的素材，做一支示例视频试试。不要重新生成素材，把结果放到新的outputs目录。

给助手的开场指引是：

> 我们先用仓库自带的素材，做一支视频试试吧。你不用先准备图片和音乐；我先检查环境，生成一小段预览，再导出完整视频。

当前默认体验《屋顶晒太阳》，直接使用随包的绘图代码、场景配置和配乐。体验完成后，再选择换成自己的本地素材，或开始全新创作；不会一上来就要求选图、找歌或重新造素材。

如果希望自己运行命令，按下面的步骤操作：

需要 Python 3.9+。示例使用 Pillow 和 FFmpeg；imageio-ffmpeg 提供 FFmpeg，已有系统版本也可使用。不需要 API Key、Node.js 或私有素材。

在仓库目录执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/doctor.py
python tools/check_pixel_baseline.py
python tools/render_pixel.py --out outputs/pixel-rooftop
python tools/check_video.py outputs/pixel-rooftop/video.mp4 --manifest outputs/pixel-rooftop/run.json --out outputs/pixel-rooftop/check.json
python tools/contact_sheet.py outputs/pixel-rooftop/video.mp4 --out outputs/pixel-rooftop/review
```

Windows 创建环境可用 `py -3 -m venv .venv`，激活使用 `.venv\Scripts\activate`；激活后仍使用 `python`。当前实跑覆盖 macOS，Windows/Linux 尚未实测。

默认结果是 **44秒、720×1280、24fps、1056帧的带音乐 MP4**（同时保留silent.mp4静音母版），位于 `outputs/pixel-rooftop/video.mp4`。输出目录必须是新的，重复运行请更换目录名；工具拒绝覆盖。绘制尺寸360×640，沿原作的最近邻取景与放大。默认设置已对照全部1056帧，检验抽取是否保持原作品画面，见 [效果保持报告](docs/rooftop-baseline-check.json)。

视频检查会完整解码和比对规格，联系表取自实际编码。两者不代替正常速度观看、听审或用户采用。

## 素材从哪里来，会花多少时间和Token

复现本示例不需要原电脑的图片、角色文件或私有归档：绘图源码、场景配置和原创配乐及其生成源码均已带齐。安装依赖后可直接生成画面和声音。

创作新主题时，AI应先确认素材方式：

| 方式 | 工作与成本提示 |
|---|---|
| 复用本地已有素材 | 先给素材位置，检查可用性和来源；通常减少重新制作 |
| 复用并补缺 | 保留已有角色/风格，只制作缺少的背景、道具或动作 |
| 全部重新制作 | 可能需要更多样稿、编程/生图/配音与反复修改，通常更慢，可能消耗更多Token或调用费用 |

用户已选方式时不重复问；未选时在新素材制作前提示，先确认实际能力与预算，再做代表段。**本地重渲本示例不会额外调用大模型或生图API**，但让AI解释、修改代码或重新造素材仍会消耗对话Token。没有可靠依据时不编造耗时或价格。
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

按内容制作入口统计，共 **6条流程：4条正式、2条候选**。题材与表现路线可以交叉，不是互斥的六种画风；机器目录见 [catalog.json](catalog.json)。

| 类型 | 主要制作内容 | 方法状态 | 本包实际能力 |
|---|---|---|---|
| [通用故事短片](workflows/短片制作.md) | 故事、角色行动、分镜、试镜和后期 | 正式 | 流程与模板，媒体工具另核 |
| [古诗词动画](workflows/古诗词动画制作.md) | 文本字音、早期声样、逐句声画与全文复习 | 正式 | 流程与模板，媒体工具另核 |
| [定格动画](workflows/定格动画制作.md) | 路线、姿态与曝光保持、接触锚点 | 正式 | 流程与模板，拍摄/渲染能力另核 |
| [像素节奏创意短片](workflows/像素节奏创意短片制作.md) | 音乐、物体机制、累积回报与连续空间 | 正式 | 流程、12份工作表与可运行示例 |
| [情绪诗词短视频](workflows/情绪诗词短视频制作.md) | 参考、情绪脚本、声样与字幕母版 | 候选 | 方法草案，尚无本包媒体实跑 |
| [立体书剪纸 MV](workflows/歌词驱动程序动画MV制作.md) | 音乐意象、纸页舞台、主体动作和折页 | 候选 | 既有实践的方法适配，未附历史渲染工程 |

另有 **2条辅助流程**：[作品归档与复用](workflows/作品归档与复用.md)、[文档维护与原则审查](workflows/文档维护与原则审查.md)，不计入六条内容制作流程。

## 四层如何配合

| 层 | 职责 | 何时读取 |
|---|---|---|
| [workflows](workflows/README.md) | 顺序、进入条件与返工出口 | 选路线、恢复阶段 |
| [agents](agents/README.md) | 导演、美术、动画、声音、验收及维护责任 | 交接当前阶段 |
| [skills](skills/README.md) | 组合当前方法、模板和工具 | 角色处理任务 |
| [standards](standards/README.md) | 共用原则、制作方法及验收依据 | 技能命中具体问题 |

按需读取，角色可由同一助手依次承担；文档本身不创建多 Agent、不安装全局技能或启动后台调度。

```text
ai-video-marker/
├── AGENTS.md / SKILL.md / CLAUDE.md  # AI 入口
├── workflows/                       # 六条制作流程 + 两条辅助流程
├── agents/                          # 制作及维护职责
├── skills/                          # 七项按阶段读取的技能
├── standards/                       # 共用方法和判断依据
├── templates/                       # 通用、专题及像素12份工作表
├── tools/                           # 初始化、渲染、音频、抽帧与检查
├── examples/pixel/                  # 场景配置与可运行示例
├── docs/                            # 预览、验证、来源与发布审阅
└── outputs/                         # 本机产物，默认不提交
```

局部返工已在各阶段保留，本版不附加独立 Loop/Graph 执行器。

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
