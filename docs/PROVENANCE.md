**目的**：说明方法、真实作品绘图代码与公开适配的来源边界。

# 来源与适配

四层方法来自维护者的动画制作体系，保留目的、基线、证据、来源、局部返工和候选状态；去除个人路径、会话、迁移账本与私有治理运行依赖。

像素示例直接取自真实作品 PIXEL-010《屋顶晒太阳》，保留18个原绘图函数；公开执行入口、场景校验与实例隔离是适配实现。来源SHA、公开文件SHA和改造边界见 [provenance.json](provenance.json)，全部原RGB帧的冻结基线见 [source-frame-baseline.json](../examples/pixel/source-frame-baseline.json)。

本包纳入该示例所需的程序绘图与场景，以及为公开版新编的44秒程序合成配乐和生成源码。原作品录音不在公开分发中。原项目保持只读，公开文件是另存的适配结果。绘图器仍专用于该示例。

媒体工具、包检查和测试为本公开包编写。Pillow、FFmpeg、imageio-ffmpeg通过本机依赖安装，各自条款沿其项目；二进制、.venv与缓存不进入源码分发。

[ai-promo-video-maker](https://github.com/liyupi/ai-promo-video-maker)用于研究工作流的组织展示，本包没有复制其代码、素材或案例。
代码、方法与项目原创示例采用 [MIT许可证](../LICENSE)，发布范围见 [发布审阅](RELEASE_REVIEW.md)。

0.1.5新增的garden_drawing.py为本公开仓库新实现，沿用pixel_drawing.py的基础绘图函数、齿轮函数及小兔的造型/配色，另编手臂接触动作与花园机制；不修改原18个函数或来源基线。默认音乐复用包内原创配乐前32秒，末尾0.8秒淡出，没有新增外部素材。make_video.py保存seed/配色并调用共用编码入口；它与原屋顶同作抽取分开记述。
