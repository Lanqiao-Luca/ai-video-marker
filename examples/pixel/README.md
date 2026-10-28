**目的**：独立复现真实作品《屋顶晒太阳》的画面，并说明适配与修改边界。

# 屋顶晒太阳 · PIXEL-010

这是首页展示与同作复现入口。首次说“做一个视频”默认去[海港机器人](../harbor/README.md)做另一支短片；仅在明确要求复现时使用本页命令。

小兔倒置雨伞收集雨水，引水后发现叶片卡住水轮，拉叶解卡驱动齿轮花展开；随后鱼旗、花、盆栽共同活动，镜头沿同一屋顶拉远。[完整带音乐预览](../../assets/videos/pixel-rooftop/preview.mp4) · [静音母版](../../assets/videos/pixel-rooftop/preview-silent.mp4)

本示例直接抽取原作的18个绘图函数，保留角色、屋顶层次、物体细节、动作和机位；公开适配拆开路径与执行入口，音频单独作为包内文件读取。它是一部具体作品的可复现示例，不是换标题就能生成任意故事的引擎。

原绘制360×640，输出720×1280、24fps、44秒、1056帧。画面为程序绘图，无需外部图片/字体/API。仓库已带新编44秒程序合成配乐及生成源码，采用MIT许可。默认输出带音乐版本并保留静音母版；见 [配乐说明](../../assets/audio/pixel-rooftop/NOTICE.md)。

## 运行与效果核对

在仓库根安装 requirements.txt 后执行：

```bash
python tools/doctor.py
python tools/check_pixel_baseline.py
python tools/render_pixel.py --out outputs/pixel-rooftop
python tools/check_video.py outputs/pixel-rooftop/video.mp4 --manifest outputs/pixel-rooftop/run.json --out outputs/pixel-rooftop/check.json
python tools/contact_sheet.py outputs/pixel-rooftop/video.mp4 --out outputs/pixel-rooftop/review
```

绘图基线回归核18个函数的AST及全部1056帧编码前RGB，预期零不一致；[来源帧基线](source-frame-baseline.json)来自原源码，未加载原音乐。它用于同作保真，不证明新的创作已经得到用户认可。

可先只导出拉叶解卡风险段：

```bash
python tools/render_pixel.py --start 16 --end 20 --out outputs/rooftop-pilot
```

只做画面或使用自己的配乐：

```bash
python tools/render_pixel.py --silent --out outputs/rooftop-silent
python tools/render_pixel.py --audio my-audio.wav --out outputs/rooftop-my-music
```

局部导出会在音源偏移上加片段起点，例如16–20秒的试镜使用音乐16–20秒。自己的音源起点可用--audio-offset指定。
所有输出使用新目录。支持从其他工作目录通过绝对脚本路径运行，默认资源从脚本位置定位。

## 可以改哪些内容

复制 [scene.json](scene.json)到自己的项目，使用 --scene 指向副本：

- camera_keys：同一世界的相机取景路径。
- rabbit_path：角色路径；调整后核接触和镜头约束。
- objects：已支持的水轮、水槽、齿轮、花、晾衣绳、雨伞和云的配置。
- output_size/fps：输出规格，画幅保原9:16；默认设置保原版。

背景细节、动作时点和部分接触坐标仍在 [原绘图实现](../../tools/pixel_drawing.py)中，画布固定360×640、故事固定44秒。不把它们声称为已经完成的通用参数引擎；改主题/时长需先适配实现并验证代表段。

## 工作流与交付

[Workflow](../../workflows/像素节奏创意短片制作.md) → [像素职责](../../agents/像素节奏短片制作.md) → [Skill](../../skills/pixel-rhythm-short/SKILL.md) → [制作标准](../../standards/像素节奏创意与连续性.md)。新作使用 [12份工作表](../../templates/pixel/README.md)。

保真抽取的实际过程见 [制作记录](production.md)及 [验证](../../docs/VALIDATION.md)。本例视觉由内置源码/配置生成，无需外部原图片。默认读取assets/audio/pixel-rooftop/music.wav；若未携带音频，可使用--silent，或--audio FILE换自己的音轨，不会暗中寻找原电脑文件。新主题是否复用本地素材、补缺或从零制作，以及时间/Token提示，见 [素材说明](../../docs/ASSETS.md)。
