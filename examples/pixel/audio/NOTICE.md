**目的**：说明随仓库配乐的来源和分发方式。

# 示例配乐

《屋顶晴天 · Rooftop Daylight》是为 ai-video-marker 新编写的程序合成配乐，未使用外部录音、采样或原作品歌曲。44秒、双声道PCM WAV随源码提供，采用仓库的 [MIT许可证](../../../LICENSE)。

旋律、和声与音色生成见 [make_demo_music.py](../../../tools/make_demo_music.py)，使用Python标准库即可重新生成；固定随机种子，文件身份见 [source.json](source.json)。

默认渲染使用music.wav；--silent导出静音版本，--audio FILE使用自己的音轨。替换音轨的权利范围由使用者另核。新配乐不代表原作品的选歌与同步听审结果。
