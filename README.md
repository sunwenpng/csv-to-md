# csv-to-md

一个很小的命令行工具：把 CSV 转成 GitHub 风格的 Markdown 表格。

只用 Python 标准库，不需要安装任何依赖（Python 3.9 及以上）。

## 用法

```bash
python3 csv_to_md.py data.csv
```

也可以从标准输入读取：

```bash
cat data.csv | python3 csv_to_md.py
```

## 示例

输入 `data.csv`：

```csv
name,qty
apple,3
pear,5
```

运行：

```bash
python3 csv_to_md.py data.csv --align right
```

输出：

```markdown
| name | qty |
| ---: | ---: |
| apple | 3 |
| pear | 5 |
```

## 参数

| 参数 | 说明 | 默认值 |
| :--- | :--- | :--- |
| `file` | CSV 文件路径，省略时读取标准输入 | 标准输入 |
| `-d`, `--delimiter` | 字段分隔符 | `,` |
| `-a`, `--align` | 列对齐方式：`left`、`center`、`right` | `left` |

## 处理规则

- 第一行作为表头。
- 单元格里的 `|` 会被转义，换行会变成 `<br>`。
- 列数不足的行会用空单元格补齐，空行会被跳过。
- 文件开头的 BOM 会被自动忽略，表格软件导出的 CSV 可以直接用。

## 测试

```bash
python3 -m unittest
```

## 许可证

[MIT](LICENSE)
