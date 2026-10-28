**目的**：用新的可复用机器人与海港素材完成默认新人短片，并说明实际制作范围。

# 小机器人与归航灯塔

36秒、720×1280、24fps。小机器人在码头找到三枚电池，依次搬到控制台装入，已接通的线路持续亮起；第三枚装入后，塔顶透镜启动，光束引导渔船归港，机器人挥手回应。

角色、背景、灯塔、船和电池来自[新的海港素材包](../../assets/images/harbor/README.md)，含12张PNG和原始绘图源码；运行时不使用兔子图片或兔子造型函数。灯光、手臂接触、搬运与归航动作由harbor_drawing.py实现，配乐复用仓库已带的原创曲，前36秒、末尾0.8秒淡出。

## 一条命令开始

在仓库根安装requirements.txt后：

```bash
python tools/doctor.py
python tools/make_video.py
```

现在默认theme为harbor。省略seed时产生并保存新seed，输出写入当前工作目录下新的outputs/first-video-时间-seed/，包含带音乐MP4、静音母版、配置、动作trace和运行记录；拒绝覆盖已有目录。不需要原电脑素材、AI Key或在线图像服务。

先试第一枚电池的接触，再用同一seed导出完整版本：

```bash
python tools/make_video.py --theme harbor --seed 42 --start 7 --end 9 --out outputs/harbor-pilot
python tools/make_video.py --theme harbor --seed 42 --out outputs/harbor-full
python tools/check_video.py outputs/harbor-full/video.mp4 --manifest outputs/harbor-full/run.json --out outputs/harbor-full/check.json
python tools/contact_sheet.py outputs/harbor-full/video.mp4 --out outputs/harbor-full/review
```

## 还有哪些可选内容

先运行 `python tools/make_video.py --list`。现有3个可运行场景、2套角色：

| 内容 | 角色 | 运行入口 |
|---|---|---|
| 小机器人与归航灯塔（默认） | 新机器人 | `python tools/make_video.py --theme harbor` |
| 月光风铃（可选） | 小兔 | `python tools/make_video.py --theme garden` |
| 屋顶晒太阳（展示复现） | 小兔 | `python tools/render_pixel.py` |

海港有sunset/midnight/mist配色，例如 `python tools/make_video.py --theme harbor --palette midnight --seed 42`。seed只改变水面闪光细节，不冒称新剧情。花园配色moon/dawn/forest须与`--theme garden`一起使用。

用户指定新的角色、场景或故事时，AI应沿[像素工作流](../../workflows/像素节奏创意短片制作.md)选择和复用素材、设计新分镜并适配动画，不能只返回同一成片。12张新素材能复用，现成渲染器仍有明确范围。需要额外素材时先说明时间、Token和外部调用成本；运行包内场景不再调用AI服务。

## 检查重点

3–4、11–12、19–20秒拾取；7–8、15–16、23–24秒装入。三枚电池的唯一身份和位置必须连续，已安装状态不能归零。24秒后才启动灯塔与归航；全片沿同一地图取景。

技术解码、动作轨迹检查、实际编码抽帧与完整实时观看/听审分别记录。静态检查不代替使用者采用。
