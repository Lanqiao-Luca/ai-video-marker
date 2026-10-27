---
status: active
version: 0.1.0
---

**目的**：让新任务的输入、计划和真实状态有稳定落点。

# 最小项目结构


运行 tools/init_project.py 会复制本目录中 brief.md、shots.csv、status.json、feedback.md 及plan.md、events.md、artifacts.json到指定的新目录；既有目录拒绝覆盖。空模板不代表已经保存本作有效计划或运行记录。
按当前用途再选择专题表单；不要求每个小改都填全部文件。

复杂任务按[EX01](../../standards/执行文档与跨窗口接续.md)消费四份接续职责：计划、唯一状态、真实事件、产出身份；按[CX01](../../standards/上下文预算与可执行单元拆解.md)只展开就绪单元。接续可直接对AI说：“读本作status.json，核当前计划/产物SHA及未决动作结果，保留有效前缀继续。”这些是文件合同，初始化器不会自动运行阶段、执行预算拦截或替用户采用。

0.3.0另复制delivery.md作为未交付格式；实际视频交付经声音与后期角色/animation-finish取得AN11合同。绝对路径只用于本机定位，文案可以另行公开，输出目录仍默认不提交。
