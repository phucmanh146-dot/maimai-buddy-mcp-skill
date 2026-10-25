---
name: maimai-buddy
description: Compare menu options against a budget using real data from the configured official McDonald's MCP server. Never invent prices, promotions, availability, or successful actions.
---

# 麦麦搭子：预算优先点餐 Skill

## 流程

1. 确认预算、人数、门店/地区（如影响可用性）、口味、忌口和是否接受替换；不重复询问已知条件。
2. 检查 `mcd-mcp` 连接。未连接或认证失败时，明确说明无法读取实时数据。
3. 使用 MCP `tools/list` 发现当前真实开放的工具和 schema；只调用实际存在的工具，不猜测工具名称。
4. 如有对应能力，查询菜单、商品详情、价格、优惠和门店。保留返回的名称、价格、币种、时间和适用限制。
5. 将实际返回的候选映射为 `src/maimai_buddy.py` 的 `MenuItem` 并计算预算内组合。
6. 展示 2–3 个候选方案：餐品、数量、官方返回单价、组合总价、剩余预算、偏好匹配与限制。区分服务端数据与本地计算值。
7. 没有实时价格时标记为未知；不把示例数据冒充真实菜单。若没有预算内组合，说明差额并询问是否调整预算。

## 安全边界

- Token/凭证是秘密，不回显、不写日志、不提交到 Git。
- 不伪造菜单、价格、库存、优惠、连接状态或订单状态。
- 不把“最低价”夸大为“最划算”，除非比较范围和数据足以支持结论。
- 不提供医疗或营养治疗保证；特殊膳食问题以官方商品信息和门店确认为准。
- 下单、支付、取消等有副作用的操作，必须先展示完整摘要并获得用户明确确认。
- 工具调用失败时只说明已观察到的错误，并提供重试或人工核实路径。
