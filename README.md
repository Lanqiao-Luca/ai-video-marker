**目的**：帮助使用者运行、理解并扩展这套 AI 视频制作工作流。

# ai-video-marker

把创意交给 AI，按流程做一支可以修改、可以接续的视频。

这里包含 **Workflow → Agent → Skill → Standards** 四层制作方法，以及制作模板、本地工具和两个可独立运行的像素场景。AI 组织阶段工作和调用工具，使用者确认创作方向与最终采用版本。

![像素示例：屋顶晒太阳](docs/images/rooftop-preview.gif)

*《屋顶晒太阳》：小兔集雨、解开水轮卡点，带动齿轮花开放，最后同一屋顶共同活动。以上为16–30秒原速节选；[44秒完整带音乐视频](examples/pixel/preview.mp4)。示例直接抽取真实作品绘图代码，保留角色、层次、动作和镜头。*

**0.1.5**：六条制作流程、四层AI协作方法，以及两个可运行的像素场景。新手默认用仓库素材制作《月光风铃》，首页《屋顶晒太阳》保留为展示复现。配乐使用项目原创音乐，源码和示例采用MIT许可。其余五条路线提供方法与模板，媒体能力依实际环境核实。正式/候选表示方法状态，详见 [发布范围](docs/RELEASE_REVIEW.md)。

## 做你的第一支视频

**先用仓库素材做一支与首页展示不同的视频，不用准备图片或音乐。** 用能读本地文件、执行命令的AI编程助手打开整个仓库，输入：

> 用仓库自带素材，做一支和README展示不同的视频。先做一个短预览，再导出完整视频；不要重新生成素材。

助手的默认开场是：

> 我们先用仓库自带的素材，做一支新的《月光风铃》吧。它和首页展示的屋顶视频是不同场景，不用准备图片和音乐。我会生成一份新的布局，先检查短预览，再导出完整视频；你也可以直接告诉我想做的主题。

新手默认片《月光风铃》是**32秒的花园短片**：小兔给音乐盒上弦，三朵风铃花依次展开，铜鸟和萤火加入花园合奏。它不是对屋顶片换标题、换配乐或重新编码。通过seed调整星点、水纹和花位，moon/dawn/forest可选三种配色；每次都保存配置，便于继续修改。

自己运行时，需要Python 3.9+，按下面操作：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python tools/doctor.py
python tools/make_video.py
```

最后一条命令会选择新seed，导出到新的 `outputs/first-video-时间-seed/`，包含32秒、720×1280、24fps的 `video.mp4`、静音母版、场景配置、动作trace及运行记录。不需要API Key、Node.js或私有素材。Pillow负责程序绘图，imageio-ffmpeg提供FFmpeg；已有系统版本也可使用。

先试握柄动作，再完整导出（两次使用相同seed）：

```bash
python tools/make_video.py --seed 42 --start 8 --end 10 --out outputs/my-first-pilot
python tools/make_video.py --seed 42 --out outputs/my-first-video
python tools/check_video.py outputs/my-first-video/video.mp4 --manifest outputs/my-first-video/run.json --out outputs/my-first-video/check.json
python tools/contact_sheet.py outputs/my-first-video/video.mp4 --out outputs/my-first-video/review
```

换成暖色清晨：`python tools/make_video.py --palette dawn --seed 42`；完整说明见 [首次创作](examples/first-video/README.md)。Windows创建环境可用 `py -3 -m venv .venv`，激活使用 `.venv\Scripts\activate`；当前macOS已实跑，Windows/Linux尚未实测。

**仓库素材可以复用，现成的渲染脚本有明确范围。** 目前有2个可运行场景：月光风铃（默认创作）与屋顶晒太阳（展示复现）；三种配色和seed只改变花园的视觉细节，不是无限故事生成器。指定新主题时，AI应按工作流复用角色、绘图函数和音乐，设计新分镜并适配代码，不能强制套用现成片。

如果明确想复现首页44秒展示片，使用 `python tools/render_pixel.py --out outputs/pixel-rooftop`，详见 [屋顶示例](examples/pixel/README.md)。它的原绘图函数和1056帧基线继续保留。视频解码和静态联系表不代替正常速度观看、听审或最终采用。

## 素材从哪里来，会花多少时间和Token

制作默认花园短片或复现屋顶片都不需要原电脑的图片、角色文件或私有归档：绘图源码、场景配置和原创配乐及其生成源码均已带齐。安装依赖后可直接生成画面和声音。

创作新主题时，AI应先确认素材方式：

| 方式 | 工作与成本提示 |
|---|---|
| 复用本地已有素材 | 先给素材位置，检查可用性和来源；通常减少重新制作 |
| 复用并补缺 | 保留已有角色/风格，只制作缺少的背景、道具或动作 |
| 全部重新制作 | 可能需要更多样稿、编程/生图/配音与反复修改，通常更慢，可能消耗更多Token或调用费用 |

用户已选方式时不重复问；未选时在新素材制作前提示，先确认实际能力与预算，再做代表段。**运行两个包内场景不会额外调用大模型或生图API**，但让AI解释、修改代码或重新造素材仍会消耗对话Token。没有可靠依据时不编造耗时或价格。
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
| [像素节奏创意短片](workflows/像素节奏创意短片制作.md) | 音乐、物体机制、累积回报与连续空间 | 正式 | 流程、12份工作表与2个可运行场景 |
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
├── examples/first-video/            # 默认新手创作：月光风铃
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
