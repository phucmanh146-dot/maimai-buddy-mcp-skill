# MCP 集成说明

## 服务与传输

- 服务：麦当劳中国官方 MCP Server。
- 接入地址：`https://mcp.mcd.cn`。
- 传输：Streamable HTTP。
- 协议版本：`2025-06-18`（官方文档注明服务器支持该版本及更早版本）。
- 鉴权请求头：`Authorization: Bearer <MCD_MCP_TOKEN>`。
- Token 仅存放在客户端本地配置或环境变量中；公开示例只使用占位符。

## 工具调用流程

1. 客户端发送 `initialize` 并确认服务器返回正常的初始化结果。
2. 发送 `tools/list`，读取服务端实际提供的工具名称、描述和 `inputSchema`；参数以实时 Schema 为准，不从示例猜测。
3. 按用户场景选择只读工具：`available-coupons`、`query-my-coupons`、`query-nearby-stores`、`delivery-query-stores`、`query-meals`、`query-meal-detail`、`query-store-coupons`、`calculate-price`、`query-my-account`、`mall-points-products`、`campaign-calendar`、`list-nutrition-foods`。
4. 先比较方案并呈现数据来源、优惠前后金额与限制条件。
5. 只有在用户明确确认后，才调用会改变账户状态的工具，例如 `auto-bind-coupons`、`create-order` 或 `mall-create-order`。

## 本项目的省钱决策

- **优惠检查**：读取当前可领取优惠及账户已有优惠；不默认自动领券。
- **菜单与门店**：根据用户选择的到店/外送方式，查询适用门店与菜单。
- **实付比较**：调用 `calculate-price` 比较候选方案，优先展示 MCP 明确返回的最终应付金额、优惠额和费用。
- **积分评估**：读取账户积分及可兑换商品；区分“可兑换”与“直接抵扣现金”，不自行假定积分价值。
- **透明输出**：说明数据更新时间、未确认条件与不可比较项；工具失败时不编造结果。

## 本机验证记录

- 已将本机 WorkBuddy 配置中的 `Authorization` 修正为 `Bearer <Token>` 格式；真实 Token 未写入仓库。
- 使用该鉴权格式，MCP `initialize` 返回 HTTP 200，服务器标识为 `mcd-mcp`、版本 `1.0.0`。
- CLI 的 `tools/list` 返回了 35 个工具定义，证明服务端鉴权与工具发现链路可用。
- WorkBuddy 全局配置已更新；TRAE 项目级配置已写入本机 `.trae/mcp.json`，该文件已从版本控制中排除。两款客户端的界面状态仍需各自刷新/启用后确认。

## 排障

- `401` 通常表示 Token 缺失、错误或过期；重新到官方开放平台核对 Token。
- `429` 表示触发服务限流；降低请求频率后重试。
- 若客户端显示未连接，检查 URL、`Bearer` 前缀、协议兼容性以及客户端是否启用该 MCP。

## 官方参考

- MCP Server 集成指南：https://github.com/M-China/mcd-mcp-server
- 活动规则与报名要求：https://github.com/M-China/mcd-developer-innovation-challenge
- MCP Token 申请：https://open.mcd.cn/mcp
