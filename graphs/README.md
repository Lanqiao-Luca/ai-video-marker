---
status: active
version: 0.2.0
---

**目的**：按真实阶段依赖恢复制作，而不是每次重走全流程。

# Graph：阶段依赖

[短片制作图](短片制作图.md)表达阶段、采用和返工关系。实际启图时交目标/节点/依赖/版本/位置状态给[Loop与阶段接口](../loops/README.md)，由其交Workflow再进入角色、Skill与标准；不跳层启动工具。

图由助手按需应用，没有图执行器或调度服务。简单工作直接沿Workflow。状态写本作同一个[status.json](../templates/project/status.json)，不在图目录另留私人运行记录或平行进度。
