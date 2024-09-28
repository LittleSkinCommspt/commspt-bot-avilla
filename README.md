# commspt-bot-avilla

LittleSkin Community Support QQ bot

LittleSkin 的社区支持 QQ 机器人，主要基于 [GraiaProject/Avilla](https://github.com/GraiaProject/Avilla) 框架。

> [!IMPORTANT]
> 不要再用 `cookit.pyd.compat` 和 `type_validate_python()`
> 这里只有 Pydantic 2，不需要兼容其他版本

## 如何使用

- 安装项目

  ```bash
  pdm install
  ```

- 填写配置文件

  `.config.yaml`，自行参考 `/commspt_bot_avilla/utils/setting_manager.py` 进行填写。

- 启动项目

  ```bash
  pdm run start-bot
  ```

- 推送至生产环境

  直接提交即可，`Drone CI` 会自动 deploy 到 production 环境。

## 更新项目依赖

```bash
pdm sync --clean
```

## 许可证

参照 [`AGPL-3.0 license`](LICENSE)。
