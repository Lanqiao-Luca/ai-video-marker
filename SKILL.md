---
name: ai-video-marker
description: 按故事、古诗词、定格或像素等制作流程组织动画短片，连接角色职责、技能、标准、模板与本地工具；用于制作或修改短片。
---

**目的**：让 AI 在本工具包内按当前制作阶段工作。

# ai-video-marker

先读同目录 [AGENTS.md](AGENTS.md)，从 [workflows](workflows/README.md)选择当前主流程，按角色→技能→必要标准逐步读取。
初次说“做一个视频”且无自定义要求时，复用仓库素材，通过tools/make_video.py制作新的《小机器人与归航灯塔》，先试段再全片，不默认重渲首页展示片。具体开场、同seed试段及明确主题的优先级沿AGENTS.md。
新创作在造素材前先明确复用、补缺或从零，并说明重新制作可能增加时间、Token及调用费用；已有明确选择直接沿用。
工具目录作为只读起点；在别的项目调用时把输出写到当前项目明确的新目录，不写进安装目录。保持整个包的相对资源结构；不复制单页冒充完整技能包。
新手创作入口是 [海港机器人](examples/harbor/README.md)，新素材在 [assets/harbor](assets/harbor/README.md)；[月光风铃](examples/first-video/README.md)为可选入口；[像素屋顶晒太阳](examples/pixel/README.md)保留为展示复现。现成像素场景共3个、2套角色，其他路线的具体媒体工具需在当前环境核实。

用户询问其他角色/画风时，先列出[现成素材库](assets/library/README.md)的10组73张PNG，再按选择复用并适配分镜/动画；不能将三个现成影片场景当成全部素材范围。
