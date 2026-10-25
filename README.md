# 麦麦搭子·省着吃（MaiMai Saver）

独立参赛项目：基于麦当劳中国 MCP 开放服务，帮助用户核对可用工具返回的菜单/优惠信息、比较点单方案，并透明展示省钱计算。**本项目不是麦当劳官方产品，也不代表麦当劳背书。**

## 当前能力

- 使用 Python 标准库实现 Streamable HTTP MCP 客户端：初始化、发现工具 Schema、按明确参数调用工具。
- 根据服务实际返回的工具与报价进行核验；不硬编码或猜测官方工具名称、菜单、价格和优惠。
- 对报价进行可复核排序，比较商品合计、优惠、配送费和实付金额（仅使用 MCP 返回字段）。
- 提供 WorkBuddy / TRAE 接入说明、Agent Skill、离线单元测试和活动声明文件。
- 不自动下单、付款、兑换积分或领取优惠券；会改变账户状态的操作必须先说明后果并取得用户明确确认。

## 项目结构

- `SKILL.md`：根目录技能入口。
- `skills/maimai-saver/SKILL.md`：详细工作流、安全与失败处理规则。
- `src/mcp_client.py`：MCP Streamable HTTP 客户端。
- `src/cli.py`：发现官方服务器工具，或按返回 Schema 手动调用工具。
- `src/savings.py`：报价金额核算与排序。
- `tests/`：离线单元测试。
- `MCP_INTEGRATION.md`：WorkBuddy / TRAE 配置说明。
- `mcp-config.example.json`：不含真实凭证的配置模板。
- `CONTEST_DECLARATION.md`：项目活动声明。

## 准备与测试

需要 Python 3.10+。在项目根目录运行：

```powershell
python -m unittest discover -s tests
```

配置好个人 MCP Token 后，可在 PowerShell 当前会话中设置环境变量（不要把真实 Token 写入代码、仓库、截图或命令历史）：

```powershell
$env:MCD_MCP_TOKEN = "YOUR_MCP_TOKEN"
python -m src.cli tools
```

先运行 `tools` 查看服务实际公布的工具名称、描述和 `inputSchema`，再根据 Schema 决定是否调用。不要猜测参数或把示例当成真实服务响应。

## 接入

参考 [MCP_INTEGRATION.md](MCP_INTEGRATION.md) 和 `mcp-config.example.json`。官方服务端地址及鉴权方式以麦当劳 MCP 开放平台当前说明为准。真实配置文件应保留在本机并由 `.gitignore` 排除；公开仓库只提交占位符。

## 安全边界

- 不上传 Token、Cookie、手机号、地址、订单或账户数据。
- 不绕过登录、验证码、访问控制或平台限制。
- 对鉴权失败、网络错误、返回缺字段等情况如实报告；不伪造“连接成功”。
- 任何会改变账户状态的动作均需用户明确确认；最终价格和优惠以官方渠道实际展示为准。

## License

MIT
