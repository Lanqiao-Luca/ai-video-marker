---
name: animation-finish
description: 处理动画声音、混音、编码和交付检查；也用于版本范围及作品验收。
metadata:
  status: active
  version: 0.1.0
---

**目的**：按实际请求选择后期、验收或版本方法。

# 声画后期与验收

先区分请求，避免只核版本却重新渲染：

- 声音/色彩/编码：[AN05](../../standards/声音色彩与交付验收.md)。锁画面和音源身份，核 cue，复测最终编码。
- 版本/返工范围：[AN06](../../standards/版本资产与返工.md)，保留采用版、来源和无变化镜头。
- 作品验收：[AN07](../../standards/制作验证与阶段验收.md)及 [AN10](../../standards/动作因果与场内节奏.md)，技术、可读性、完整听看和用户采用分别记录。
- 同候选复核：[AN08](../../standards/审核交接与定向复核.md)；工具失败：[AN09](../../standards/渲染和工具异常恢复.md)。

[check_video.py](../../tools/check_video.py)可全解码和读规格；[contact_sheet.py](../../tools/contact_sheet.py)抽编码帧；[attach_audio.py](../../tools/attach_audio.py)为静音母版附加用户提供的音轨。命令和真实边界见 [工具说明](../../tools/README.md)。
音乐/录音/生成/合成来源分开，不能以母带数值代替最终音轨，也不能以自动检查代替听感。
