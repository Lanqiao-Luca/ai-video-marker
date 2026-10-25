**目的**：说明实际工具的输入、输出及验证边界。

# 本地工具

在仓库根部、激活虚拟环境后运行。媒体工具可用 `--ffmpeg 可执行文件` 或 `FFMPEG_BINARY` 指定 FFmpeg。

| 工具 | 输入 → 输出 | 边界 |
|---|---|---|
| [doctor.py](doctor.py) | 当前环境 → 检查 JSON | 不安装、不联网、不读凭据 |
| [init_project.py](init_project.py) | 路线、ID、新目录 → 模板与状态 | 只初始化，不生成视频 |
| [render_pixel.py](render_pixel.py) | 屋顶场景 JSON → 带音乐视频/静音母版、配置、trace、run身份 | 真实作品专用绘图复现，不是任意故事引擎 |
| [check_video.py](check_video.py) | 最终视频、可选run → 规格/完整声画解码 | 不代实时观看、听审和采用 |
| [contact_sheet.py](contact_sheet.py) | 视频、时点 → 编码帧与联系表 | 静态取样，不称全程观看 |
| [attach_audio.py](attach_audio.py) | 视频、自带音轨、偏移 → 新带声MP4及来源记录 | 画面复制、AAC编码，不循环或推定许可 |
| [check_pixel_baseline.py](check_pixel_baseline.py) | 默认场景 → 原绘图函数与全部1056帧RGB回归 | 只覆盖同作品编码前画面，不替艺术采用 |
| [check_package.py](check_package.py) | 公开包 → 链接/语法/目录/来源检查 | 窄范围静态检查，不是完整安全审计 |

[pixel_engine.py](pixel_engine.py)负责场景校验与实例隔离，[pixel_drawing.py](pixel_drawing.py)保留原作18个绘图函数，[media.py](media.py)为共用FFmpeg适配，均非用户CLI入口。

render_pixel.py默认读取包内原创配乐，--silent可只导出画面，--audio FILE可替换音轨，--audio-offset指定音源起点；导出局部片段时自动加入片段起点，避免错用开头音乐。仓库配乐采用MIT许可。
init_project.py的--assets reuse|mixed|generate只记录素材策略，不调用AI或自动生成素材；未选时将下一步记为确认策略。

音频必须覆盖整个片段，不够长时工具拒绝自动循环：

```bash
python tools/attach_audio.py outputs/pixel-rooftop/video.mp4 my-audio.wav --offset 0 --out outputs/pixel-rooftop-with-audio/video.mp4
python tools/check_video.py outputs/pixel-rooftop-with-audio/video.mp4
```

所有工具拒绝覆盖既有输出。渲染失败保留 run.json 和部分现场，先看 render.log，再在新目录恢复。用 `--help` 看参数。
FFmpeg由系统或本机imageio-ffmpeg安装提供，二进制与虚拟环境不进入源码分发。
