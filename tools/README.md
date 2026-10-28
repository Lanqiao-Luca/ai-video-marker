**目的**：说明实际工具的输入、输出及验证边界。

# 本地工具

在仓库根部、激活虚拟环境后运行。媒体工具可用 `--ffmpeg 可执行文件` 或 `FFMPEG_BINARY` 指定 FFmpeg。

| 工具 | 输入 → 输出 | 边界 |
|---|---|---|
| [asset_library.py](asset_library.py) | 10组73张素材 → 列表、SHA/图片验证、新预览联系表 | 离线使用，不调用AI，不自动生成新剧情 |
| [doctor.py](doctor.py) | 当前环境 → 检查 JSON | 不安装、不联网、不读凭据 |
| [init_project.py](init_project.py) | 路线、ID、新目录 → 模板与状态 | 只初始化，不生成视频 |
| [make_video.py](make_video.py) | theme、seed、配色 → 新手短片、配置、trace、run身份 | 默认做海港机器人；--theme garden选小兔，--list列出内容；不调用AI服务 |
| [render_pixel.py](render_pixel.py) | 三种已支持场景JSON → 带音乐视频/静音母版、配置、trace、run身份 | 未指定scene时仍为屋顶复现；不生成任意故事 |
| [check_video.py](check_video.py) | 最终视频、可选run → 规格/完整声画解码 | 不代实时观看、听审和采用 |
| [contact_sheet.py](contact_sheet.py) | 视频、时点 → 编码帧与联系表 | 静态取样，不称全程观看 |
| [attach_audio.py](attach_audio.py) | 视频、自带音轨、偏移 → 新带声MP4及来源记录 | 画面复制、AAC编码，不循环或推定许可 |
| [check_pixel_baseline.py](check_pixel_baseline.py) | 默认场景 → 原绘图函数与全部1056帧RGB回归 | 只覆盖同作品编码前画面，不替艺术采用 |
| [check_package.py](check_package.py) | 公开包 → 链接/语法/目录/来源检查 | 窄范围静态检查，不是完整安全审计 |
| [painted_world_reveal.py](painted_world_reveal.py) | 内图/外图RGB数组、画布四角、进度 → 同源退出揭示RGB帧 | 可选NumPy/OpenCV纯函数，不读写文件、不生成视频、不构建三维 |

[pixel_engine.py](pixel_engine.py)负责场景校验与实例隔离，[pixel_drawing.py](pixel_drawing.py)保留原作18个绘图函数，[media.py](media.py)为共用FFmpeg适配，[garden_drawing.py](garden_drawing.py)实现花园场景及校验，[harbor_drawing.py](harbor_drawing.py)读取新机器人PNG素材并实现海港故事，均非用户CLI入口。

[harbor_assets.py](harbor_assets.py)用可编辑源码生成12张可复用PNG到新的--out目录，见[海港素材包](../assets/images/harbor/README.md)。

render_pixel.py默认读取包内原创配乐，--silent可只导出画面，--audio FILE可替换音轨，--audio-offset指定音源起点；导出局部片段时自动加入片段起点，避免错用开头音乐。仓库配乐采用MIT许可。
init_project.py的--assets reuse|mixed|generate只记录素材策略，不调用AI或自动生成素材；未选时将下一步记为确认策略。

`--route reference-comic`会带入AI漫画/参考音轨的文字制作单，新项目均有未交付的delivery.md；初始化不调用剪映、生图或音源下载。实际交视频沿声音与后期角色/animation-finish消费AN11，不因填交付文案重渲或发布。

音频必须覆盖整个片段，不够长时工具拒绝自动循环：

```bash
python tools/attach_audio.py outputs/pixel-rooftop/video.mp4 my-audio.wav --offset 0 --out outputs/pixel-rooftop-with-audio/video.mp4
python tools/check_video.py outputs/pixel-rooftop-with-audio/video.mp4
```

所有工具拒绝覆盖既有输出。渲染失败保留 run.json 和部分现场，先看 render.log，再在新目录恢复。用 `--help` 看参数。
FFmpeg由系统或本机imageio-ffmpeg安装提供，二进制与虚拟环境不进入源码分发。

<a id="painted-world"></a>
## 可选：从画中拉回画框

先核[PW05合同](../standards/画中世界退出与载体揭示.md)。只有使用该合成函数时安装可选依赖；默认像素示例继续只用requirements.txt：

```bash
python -m pip install -r requirements-painting.txt
```

在仓库根目录可这样调用（变量须由调用者提供真实数组/坐标）：

```python
from tools.painted_world_reveal import reveal_painted_world

# inner/outer: H×W×3 uint8 RGB或[0,1]浮点RGB，尺寸可以不同。
# quad: outer像素坐标中的左上、右上、右下、左下，凸且不退化。
frame = reveal_painted_world(inner, outer, quad, progress=0.5)
```

progress为调用者已经缓动后的[0,1]进度：0让画中图充满输出，1回到外部场景内的固定画布；返回outer尺寸的float32 RGB。live_inner_rgb/live_weight可把动态画中帧逐渐冻结；RGBA输入、错误顺序/凹面/越界/退化四角和非有限进度会报错。函数采用直立画布的无歧义左上约定，不支持任意旋转画框。

读图时由调用者明确RGB（OpenCV默认BGR须转换）、裁切/比例、四角坐标与身份；不同宽高比须先选裁切/留边，不静默拉伸。图内动效先合入内图，前景遮挡/屏幕字幕在视野变换后由调用者合成。大角度画框可能拉伸外图边缘，不会生成未知场景。完整时序、音轨、编码和正常速度审看仍沿实际制作流程。
