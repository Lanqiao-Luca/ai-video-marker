**目的**：让第一次使用的人用仓库素材制作与首页展示不同的短片，并能继续修改。

# 月光风铃 · 可选创作

当前默认新人短片已改为[海港机器人](../harbor/README.md)。本页保留可选的小兔花园《月光风铃》：同一小兔来到花园，转动音乐盒曲柄积蓄发条动力，三朵风铃花依次展开，顶端铜鸟展翼，萤火和盆花加入。32秒、720×1280、24fps，无文字。

复用包内兔子造型、绘图基础函数及原创音乐，新的花园场景、上弦动作、铃花与铜鸟机制由garden_drawing.py实现。原屋顶绘图源码保持不变。所有素材采用仓库MIT许可，无需AI Key、外部图集、字体或原电脑文件。

## 运行

在仓库根安装requirements.txt后：

```bash
python tools/doctor.py
python tools/make_video.py --theme garden
```

每次省略seed都会生成新seed，并打印、保存它；配乐复用包内原创曲前32秒，末尾做0.8秒淡出（短试段最多使用半段长度）。默认输出目录是当前工作目录下的 `outputs/first-video-时间-seed/`。输出包含video.mp4、silent.mp4、scene.json、run.json、trace.json及编码抽帧，既有目录不会覆盖。

如由AI带新人做，先记录seed，试段与全片使用同一个值：

```bash
python tools/make_video.py --theme garden --seed 42 --start 8 --end 10 --out outputs/first-pilot
python tools/make_video.py --theme garden --seed 42 --out outputs/first-full
python tools/check_video.py outputs/first-full/video.mp4 --manifest outputs/first-full/run.json --out outputs/first-full/check.json
python tools/contact_sheet.py outputs/first-full/video.mp4 --out outputs/first-full/review
```

试段核手掌与曲柄的接触。完整片重点看：4–12秒四圈上弦、四灯逐步保留；14–23秒三花先后展开；23–28秒铜鸟展翼；28–32秒同一地图全景。不将逐帧不同或平滑插值等同于艺术验收。

## 第一次就能改什么

| 操作 | 命令或入口 | 实际变化 |
|---|---|---|
| 月夜 / 清晨 / 森林配色 | `--palette moon` / `dawn` / `forest` | 天色、山体、叶片与花瓣配色 |
| 换布局细节 | `--seed 123`，或省略随机选seed | 星点、水纹、左右花位与中花高度；剧情保持 |
| 复现或接着改自己的版本 | 输出的scene.json → `render_pixel.py --scene 文件 --out 新目录` | 同一seed、palette和机位可重复导出 |
| 试一个片段 | `--start 8 --end 10` | 同步选取对应音乐片段 |
| 静音 / 自己的音乐 | `--silent` / `--audio 文件` | 不自动找歌、不推定新音轨许可 |

`python tools/make_video.py --theme garden --palette dawn --seed 123`可直接得到暖色版。固定seed和配置可复现画面；不保证不同FFmpeg版本的编码文件SHA相同。

这些参数不是任意故事生成器。用户指定“音乐盒以外的新主题”“新角色”“新时长”时，AI须沿[像素工作流](../../workflows/像素节奏创意短片制作.md)设计和适配实现，优先复用包内角色、基础函数和音乐；不能只换标题或返回本片。需要新增素材时先说明时间、Token和外部调用费用。运行本入口只做本机绘制与编码，不调用AI服务；与助手交流或改代码仍消耗对话Token。

换新的机器人主角去[海港入口](../harbor/README.md)。若用户明确说“复现首页示例”，才回到[屋顶复现入口](../pixel/README.md)。
