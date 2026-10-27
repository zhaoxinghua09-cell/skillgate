# SkillGate 四道闸门检查指南

用 SkillGate 实现 LGD 三律的四道闸门门禁。

---

## 四道闸门总览

| 闸门 | 什么时候过 | 检查什么 |
|------|-----------|----------|
| **落地闸** | 发布前 | 有没有可执行的测试用例？ |
| **身份闸** | 提交前 | 作者信息是不是准确？ |
| **时效闸** | 发布后 | 有没有持续监控？ |
| **留痕闸** | 每次扫描后 | 结果有没有存档？ |

---

## 1. 落地闸（有可执行方案才提）

**检查项**:
- ✅ 有 SKILL.md 吗？
- ✅ 有 scripts/ 目录吗？
- ✅ 有测试用例吗？
- ✅ 跑过 SkillGate 扫描吗？

**命令**:
```bash
skillgate scan ./my-skill/ --fail-under 80
```

**不过怎么办**:
- 分数 < 80 → 先修完问题再发布
- 没有测试用例 → 先写测试

---

## 2. 身份闸（作者信息准确）

**检查项**:
- ✅ SKILL.md 里有 author 字段吗？
- ✅ 有 license 吗？
- ✅ 有 version 吗？

**命令**:
```bash
skillgate scan ./my-skill/ --format agent
```

**输出里看**:
- `frontmatter.author` 有没有
- `frontmatter.license` 有没有
- `frontmatter.version` 有没有

---

## 3. 时效闸（持续监控）

**检查项**:
- ✅ 配了 skillwatch 吗？
- ✅ 有每周回归测试吗？
- ✅ 分数暴跌有告警吗？

**命令**:
```bash
# 启动持续监控
python skillwatch.py ./my-skill/ --weekly
```

---

## 4. 留痕闸（结果存档）

**检查项**:
- ✅ 每次扫描都有存档吗？
- ✅ 有历史趋势吗？
- ✅ 能追溯到规则版本吗？

**命令**:
```bash
# 输出 SARIF 格式存档
skillgate scan ./my-skill/ --format sarif --output scan-2026-10-27.sarif

# 生成趋势图
python trend_chart.py scores.txt labels.txt
```

---

## LGD 三律对照

| 三律 | 对应闸门 |
|------|----------|
| **有籍**（registered） | 落地闸 + 身份闸（有档案可追溯） |
| **有证**（evidenced） | 留痕闸（每个结论有出处有证据） |
| **有门禁**（gated） | 四道闸门都是门禁（关键节点有检查） |

---

**这样就把 LGD 三律工程化了——用 SkillGate 做门禁，自动检查，自动留痕。**
