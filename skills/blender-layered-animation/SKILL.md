---
name: blender-layered-animation
description: 按当前Blender分层角色有限动画阶段组装资产、绑定、表演、缓存与后期方法；不是自动渲染器或完整三维角色能力。
metadata:
  status: active
  version: 0.6.0
  atom_property_schema: "APROP01-v1"
  atom_nature: "operation"
  atom_secondary_natures: ["method", "acceptance"]
  atom_applicability: "domain"
  atom_scope_detail: "Blender分层角色2.5D有限动画的当前授权阶段；不覆盖完整三维人物表演"
  atom_domain: "AI视频制作"
  maintenance_role: "canonical"
---

**目的**：按现有职责的当前模式组装Blender分层角色有限动画方法与实现，返回可定位结果。

<!-- ATOM_PROPERTIES:BEGIN -->
**原子属性**：主性质：操作性；辅助性质：方法性、验收性。适用范围：领域（AI视频制作，沿当前任务真实授权）；维护身份：canonical（本公开适配）。属性检查不代实际执行或语义审查。
<!-- ATOM_PROPERTIES:END -->

# Blender分层角色动画

接现有制作职责交入的作品/run、当前阶段、采用身份、授权/位置、输入版本与未知。只取相交模式，不直接调度上层、不自动生成新作品/开后台。公共要求由制作视频原入口返回，文档由animation-docs维护。

<a id="methods"></a>
## 模式与原子

|模式 / 原调用职责|薄组装与输入→输出|
|---|---|
|plan / 导演|调用[animation-plan](../animation-plan/SKILL.md)的既有AN01/03/10适配，按BL02选择有限动画能力与环境；经[BL04](../../standards/角色表演与曲线精修.md)收敛本片表演意图/注视目标和关键姿态；交观看承诺、创作范围、画布/镜头/cue、风险集合、制作位置/缺项。题材/来源事实不足时如实返回未知。|
|art / 美术|既有[animation-shot](../animation-shot/SKILL.md)核AN02，按[BL01](../../standards/分层贴图与变形绑定.md)核透明/注册可绑定资产；交实际图像工具来源、候选/原件、尺寸/alpha、补图和静态身份；表演需脸部变化时交BL04所需校准表情/控件，不默认整脸扭曲。|
|rig / 动画|消费BL01及[BL02](../../standards/可重建场景与镜头.md)，用AN04接触支点；交权重/shape keys/局部mask、附件铰链、镜头/层序、真实工程和依赖；BL01关节测试须返回肩胸非目标影响、IK/FK/拉伸选择和限制范围，再交BL04。|
|motion / 动画|既有animation-shot消费AN04/10，BL02组织场景试段；用BL04落实关键姿态→过渡→局部神态→曲线精修/次级跟随，返回连续样段覆盖、局部动作与表演证据、失败/未验，修订走AN06/08/09，不把关键帧通过当连续已看。|
|render / 动画|按[BL03](../../standards/动作采样与渲染缓存.md)固定时间采样/切点/缓存依赖；沿AN06返工，交有效/失效帧及真实重渲身份。|
|finish / 声音后期|通过[animation-finish](../animation-finish/SKILL.md)消费AN05/07/11，BL03仅提供源/编码采样映射；保留原音流与新合成音分别选择，不无意重复叠乐。交真实编码、声音身份、全路径/标题/描述和必要依赖。|
|review / 作品验收|通过animation-finish的AN07/08消费本轮目的/同候选与BL01–04返回；核本片肩臂/神态协调及BL04实际正常速度观察，必要失败不能凭技术通过扩片；分技术、抽帧、连续看听及Owner采用，失败回具体阶段；不自签独立审查。|

各既有AN正文沿原通用Skill取得，不在本Skill重写；BL只维护Blender的具体增量。通用AP通过[animation-docs](../animation-docs/SKILL.md)取得，既有权限/基线和职责保持。

<a id="sources"></a>
## 来源与实现

首次选实现或恢复时，从同层[工具说明](../../tools/Blender分层动画实现.md)取得环境探测、构建/工程依赖和未提供项。本包没有附Blender构建脚本、.blend、插件、分层角色姿势或私有案例源码；实际新作品需在当前授权工作区编写/适配脚本并绑定可用输入。没有工程时能规划方法，不声称已有重渲输入或一键产片。

<a id="return-context"></a>
## 返回与断点

返回模式、输入SHA/范围、实际输出、已用位置、验证/未知及下一消费者。缺alpha回art；缺空间/新侧面回plan/art；绑定/接触失败回rig；时间映射/混版回render；编码/音轨失败回finish。工程依赖或工具不可用只停依赖步骤，保有效前缀。位置变化交原文档维护职责，不在此另建平行状态。

返回：[Skill目录](../README.md)。
