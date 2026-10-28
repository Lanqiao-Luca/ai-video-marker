---
name: painting-world-video
description: 按当前阶段设计绘画世界穿行短片的参考约束、逆推路线、关键帧、接缝试镜和验收；属于候选方法，具体媒体能力当次核实。
metadata:
  status: candidate
  version: 0.5.0
  atom_property_schema: "APROP01-v1"
  atom_nature: "operation"
  atom_secondary_natures: ["method", "acceptance"]
  atom_applicability: "domain"
  atom_scope_detail: "候选绘画世界的平面退出与连续嵌套；不代表整片生成、原生软件或实际艺术采用"
  atom_domain: "AI视频制作"
  maintenance_role: "canonical"
---

**目的**：让既有制作角色按需组合绘画世界的方法，不替代实际工具能力。

<!-- ATOM_PROPERTIES:BEGIN -->
**原子属性**：操作性，辅助方法性/验收性；领域：AI视频制作；维护身份canonical（本公开正文）。保candidate状态与实际工具边界，属性不代语义审查。
<!-- ATOM_PROPERTIES:END -->

# 绘画世界穿行

接原角色交入的目标、阶段、采用基线、真实工具/费用、写集与输入/过程/交付位置；缺项只停相交动作。方法仍为候选，不安装原生技能，不反向启动角色或工作流。

| 模式 / 调用角色 | 按需读取 | 返回 |
|---|---|---|
| reference / 导演 | [PW01](../../standards/绘画世界穿行短片原子.md#pw01-把参考变成可制作的体验约束) | 实际观看范围、观察/推断/提案/未知与体验约束 |
| plan / 导演 | [PW02](../../standards/绘画世界穿行短片原子.md#pw02-连续路线空间锚点与揭示节奏)、[AN01](../../standards/制作单与故事拆解.md) | 结尾画面、逆推路线、地标/尺度/接缝表和cue；使用[专题制作单](../../templates/绘画世界穿行制作单.md) |
| art / 美术 | PW02、[PW03](../../standards/绘画世界穿行短片原子.md#pw03-关键帧生成接口与代表接缝试制)、[AN02](../../standards/角色与画面一致性.md) | 同一世界关键帧/笔触/地标、来源与采用身份；实际造型沿animation-shot |
| motion / 动画 | PW03、[AN03](../../standards/镜头空间与动态分镜.md)、[AN04](../../standards/代表镜头与动作制作.md) | 实际能力选择、片段/接缝试片及局修；缺服务时交未执行输入包 |
| sound / 声音 | PW02的cue输入、[AN05](../../standards/声音色彩与交付验收.md) | 真实音源、允许用途、事件版本、混音/导出；实际后期沿animation-finish |
| review / 验收 | [PW04](../../standards/绘画世界穿行短片原子.md#pw04-连续观看与路线验收)、[AN07](../../standards/制作验证与阶段验收.md) | 同候选技术/连续观看/用户状态、具体时点问题与返工落点 |

仅在方案选择“从画中退出到固定画布”时，motion/review加读[PW05](../../standards/画中世界退出与载体揭示.md)。它提供同源内外图、唯一四角和平面投影合同，不是完整三维，也不强加片尾。对应纯函数及可选依赖见[工具说明](../../tools/README.md#painted-world)。

原则沿[五AP](../../standards/README.md)；交接/工具故障沿[AN08](../../standards/审核交接与定向复核.md)/[AN09](../../standards/渲染和工具异常恢复.md)。向原角色交实际产物、版本、成本、检查范围及未知；Markdown和进度事实交文档维护。通用阶段方法继续复用，不能将静帧/方案完整写成已生成影片。

## 连续嵌套的阶段消费

plan先区分连续嵌套、单次退出、连续穿行；嵌套分支消费[PW05](../../standards/画中世界退出与载体揭示.md#continuous-nested-reveal)，给完整层链/新外景与权威cue。art返回逐层源图、统一画布的显式适配和载体四角；motion交完整复合继承给[多层工具](../../tools/多层嵌套揭示工具.md)，先试两次连续退出再扩展。
sound保独立音乐速度/字幕与真实软件边界；review核两次接缝、最小载体、主体清晰和实际观看范围。缺工具交未执行输入，不把单次退出或相同画风当已实现多层体验；候选状态和原专业责任保持。
