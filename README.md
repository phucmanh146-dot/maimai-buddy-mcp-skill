# 麦麦搭子 MaiMai Buddy

麦当劳 MCP 驱动的预算优先点餐与省钱决策 Agent Skill。它把预算、人数、口味与限制转成可解释的候选组合，并要求在任何下单或支付动作前获得用户明确确认。

> 本项目为独立参赛作品，非麦当劳官方产品。菜单、价格、库存、优惠及下单能力以官方 MCP 实时返回为准。未连通有效 Token 时不会伪造菜单或调用成功结果。

## 功能

- 预算优先：根据 MCP 实际返回的餐品与价格计算预算内组合。
- 解释选择：展示组合总价、预算余额和价格依据；只有官方数据支持时才声称有优惠。
- 尊重偏好：询问口味、忌口和是否接受替换。
- 真实数据优先：服务端工具名称及参数以运行时发现的 schema 为准，不猜测未验证的工具。
- 安全确认：订单、支付、取消等有副作用的操作必须先展示摘要并取得明确确认。

## 文件

- `SKILL.md`：Agent 技能说明和安全边界。
- `src/maimai_buddy.py`：离线预算组合算法。
- `tests/test_maimai_buddy.py`：单元测试。
- `MCP_INTEGRATION.md`：官方 MCP 配置和调用流程。
- `mcp-config.example.json`：脱敏配置示例。
- `CONTEST_DECLARATION.md`：官方原版声明。

## 配置官方 MCP

官方 endpoint：`https://mcp.mcd.cn`。在支持 Streamable HTTP 的客户端配置：

```json
{
  "mcpServers": {
    "mcd-mcp": {
      "type": "streamablehttp",
      "url": "https://mcp.mcd.cn",
      "headers": {
        "Authorization": "Bearer ${MCD_MCP_TOKEN}"
      }
    }
  }
}
```

通过官方渠道申请 Token，并在客户端的安全密钥管理中设置 `MCD_MCP_TOKEN`。若客户端不支持环境变量展开，请用客户端支持的 secret 配置方式。不要把真实 Token 提交到 Git。

## 测试本地算法

需要 Python 3.10+，无第三方依赖：

```bash
python -m unittest discover -s tests -v
```

```python
from src.maimai_buddy import MenuItem, find_budget_combinations
items = [MenuItem("示例餐品 A", 12.0), MenuItem("示例餐品 B", 8.0)]
print(find_budget_combinations(items, budget=20.0, max_items=2))
```

示例名称和价格仅用于演示算法，不代表真实菜单或当前售价。实际使用时，必须将成功的官方 MCP 返回映射为 `MenuItem`。

## 真实接入边界

本仓库包含技能流程和本地算法；尚未证明当前环境已使用有效 Token 完成官方服务端实时调用。详见 [MCP 集成说明](MCP_INTEGRATION.md)。本地算法不会联网、申请 Token、生成菜单或调用支付/下单接口。
