---
status: active
version: 0.4.0
atom_property_schema: "APROP01-v1"
atom_nature: "method"
atom_secondary_natures: ["principle", "operation", "acceptance"]
atom_applicability: "domain"
atom_scope_detail: "当前公开视频制作方法及本轮授权写集；不扩大权限、候选效力或工具能力"
atom_domain: "AI视频制作"
maintenance_role: "canonical"
atom_nature_map: [{"selector": "## AT01 按正文判断", "primary": "method", "secondary": ["principle"], "applicability": "domain", "domain": "AI视频制作"}, {"selector": "## AT02 声明与保存", "primary": "operation", "secondary": ["principle"], "applicability": "domain", "domain": "AI视频制作"}, {"selector": "## AT03 检查与离线边界", "primary": "acceptance", "secondary": ["method"], "applicability": "domain", "domain": "AI视频制作"}]
---

**目的**：按真实正文标明能力原子的性质、范围和维护身份，区分属性检查、语义判断与来源同步。

<!-- ATOM_PROPERTIES:BEGIN -->
**原子属性**：主性质：方法性；辅助性质：原则性、操作性、验收性。适用范围：领域（AI视频制作，沿本次真实授权）；维护身份：canonical（本公开正文）。属性不代语义审查或实际执行。

| 可定位组 | 主性质 | 辅助性质 | 适用范围 |
|---|---|---|---|
| AT01 按正文判断 | 方法性 | 原则性 | AI视频制作 |
| AT02 声明与保存 | 操作性 | 原则性 | AI视频制作 |
| AT03 检查与离线边界 | 验收性 | 方法性 | AI视频制作 |
<!-- ATOM_PROPERTIES:END -->

# APROP01 原子性质、范围与维护身份

## AT01 按正文判断

性质、适用范围、维护身份是三个独立分类轴：

| 主性质 | 机器值 | 主要用途 |
|---|---|---|
| 原则性 | principle | 取舍、不变量、授权与边界 |
| 方法性 | method | 分析、比较、推演和拆解 |
| 操作性 | operation | 接输入、执行动作并返回产物 |
| 验收性 | acceptance | 检查条件、证据、通过/未知与复核 |

每个原子有一个主性质，可有不重复且不同于主性质的辅助性质。标题、文件名、所在目录和“有输入输出”均不代正文判断。
适用范围为general或domain，领域项必须写实际领域；general仍有原适用前提，不表示所有组织适用。
维护身份canonical表示本正文的正式维护路径，portable_replica表示保有来源/版本关系的随包副本；两者都不改变active/candidate或用户采用状态。

纯导航、空模板、机器目录、参数和历史证据按真实用途排除；README中若定义方法，该方法部分仍须判断。不能将旧原子改称资源来逃避检查。

## AT02 声明与保存

新建或修改能力文档时，由文档职责核原目的和真实写集，保留必要前件与来源。声明atom_property_schema（APROP01-v1）、atom_nature、atom_secondary_natures、atom_applicability、atom_scope_detail、领域项的atom_domain和maintenance_role。
Skill使用metadata承载这些字段；其他能力文档在frontmatter直接声明。正文目的仍为首个可见段，属性说明置于ATOM_PROPERTIES注释块内。

含独立不同性质/范围的方法组时，用atom_nature_map登记唯一完整标题selector、primary、secondary、applicability及领域项的domain；不能按每一步机械拆组，也不能漏掉实质不同的组。
排版可以复用仍有效的属性和语义判断，缺属性或旧判断未知不能豁免。保原状态、效力、采用基线与版本谱系；本轮仅维护实际写集，不自动重写整个仓库。

保存前核候选与旧SHA、结构和相交分类依据，保存后读回目标SHA；若目标已被他人修改则停相交写入，不覆盖并发版本。
公开版提供本轮登记目标的结构检查及来源SHA核对，没有迁入私有保存器、语义签名系统或文件锁；作者仍须核正文分类和混合组覆盖，不以JSON/字段齐全自签独立审查。

## AT03 检查与离线边界

缺属性返回NEEDS_PROPERTIES；非法值、主辅重复、domain缺失或组标题不唯一返回具体错误；语义未核、维护身份冲突保UNKNOWN。独立项仍可继续。
结构检查、作者语义自检、独立审查、来源完整性、上游同步和用户采用分别报告。规范SHA合同已有标界时保其字节规则，不把属性说明偷偷计入或改写旧证据。

来源清单证明本次读取的源/目标身份，不证明持续与私人源自动同步。离线只核本地完整性；有真实上游并获授权时才比较上游版本/规范SHA。副本漂移先保差异，不自动覆盖或反写；获准离线修订保起点并标待协调身份。
本公开正文是独立维护的公开适配，maintenance_role为canonical；私人源本身的portable_replica身份见provenance，只用于追溯，不能冒称公开版与上游规范字节相同。

返回：[标准目录](README.md)。
