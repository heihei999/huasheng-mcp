# Data Material Gate Hardening v0.4.2

## Overview

v0.4.2 fixes a routing vulnerability where questions with explicit material/table/chart signals (like "表中", "根据表格", "上述资料", "图中数据") were being routed to quantity_relation instead of data_analysis, bypassing the missing_table_or_material gate.

## Problem

External clean runtime 60-case stress test found:

**Sample**: "表中2018—2022年工业增加值平均每年增长量约为多少亿元？"

**Expected**: route.module_guess = data_analysis, answer_allowed = false (missing table)

**Actual (before fix)**: route.module_guess = quantity_relation, answer_allowed = true

**Root cause**: "表中" was not recognized as a data_analysis strong signal. The question was routed to quantity_relation (because of "增长量" and numbers), which bypassed the data_analysis missing_table_or_material gate.

## Fix 1: Enhanced Material Signal Detection

Added `_DATA_MATERIAL_STRONG_KW` list with explicit material/table/chart signals:

```python
_DATA_MATERIAL_STRONG_KW = [
    "表中", "表格", "根据表格", "根据下表", "下表", "上表", "统计表",
    "图表", "根据图表", "图中数据", "图中", "折线图", "柱状图", "饼状图",
    "材料显示", "根据材料", "上述材料", "上述资料", "根据上述资料", "资料显示",
]
```

Added `_has_data_material_signal()` helper function to check for these signals.

Updated routing logic to check material signals BEFORE quantity_relation keywords:

```python
# Data material strong signals (v0.4.2): "表中/表格/图表/材料/资料/图中数据"
# These should route to data_analysis even if quantity keywords are present
# Check before quantity_relation to prevent "表中...增长量" being misrouted
if module_guess == "unknown" and _has_data_material_signal(combined):
    signals.append("data_material_strong_signal")
    module_guess = "data_analysis"
    confidence = "high"
```

## Fix 2: Independent Material Gate

Updated `tool_compose_xingce_answer_prompt()` to add independent material signal detection:

```python
# Independent data material signal detection (v0.4.2)
# Even if route is not data_analysis, if the question has material signals,
# we should still require material/table context
combined_text = (question_text or "") + " " + " ".join((options or {}).values())
requires_table_or_material = (
    module_guess == "data_analysis"
    or _has_data_material_signal(combined_text)
)
```

This ensures that even if route temporarily misroutes to quantity_relation, the answer gate still blocks when material signals are present but material/table context is missing.

## Fix 3: context_requirements Update

Updated `context_requirements.requires_table_or_material` to use the new `requires_table_or_material` variable:

```python
context_requirements = {
    "requires_visual": module_guess == "graphic_reasoning",
    "requires_table_or_material": requires_table_or_material,
    ...
}
```

## Verification

### Route Results

| Sample | Expected | Actual |
|--------|----------|--------|
| 表中2018—2022年工业增加值平均每年增长量约为多少亿元？ | data_analysis | data_analysis ✅ |
| 根据表格，2021年甲地区生产总值同比增长率约为多少？ | data_analysis | data_analysis ✅ |
| 上述资料显示，2022年A市常住人口比上年增加了多少万人？ | data_analysis | data_analysis ✅ |
| 图中数据显示，第三季度销售额占全年销售额的比重约为多少？ | data_analysis | data_analysis ✅ |

### Negative Cases (should NOT be misrouted)

| Sample | Expected | Actual |
|--------|----------|--------|
| 一个水池甲管注满需8小时，乙管注满需12小时，两管同时开几小时注满？ | quantity_relation | quantity_relation ✅ |
| 甲乙两车相向而行，甲车每小时60公里，乙车每小时80公里，几小时相遇？ | quantity_relation | quantity_relation ✅ |

### Answer Gate Results

| Sample | material_present | answer_allowed | answer_block_reason |
|--------|------------------|----------------|---------------------|
| 表中...增长量 | false | false | missing_table_or_material ✅ |
| 表中...增长量 | true | true | null ✅ |

## Test Status

- tests/test_mcp_guidance_tools_preview.py: 210 passed (was 198, +12)
- python -m pytest: 541 passed (was 529, +12)

## Safety

- No answer / selected_option / prediction in tool return
- No external LLM/API call
- No solver/scaffold/all_cards/cli modification
- No analyze_xingce_question developed

## Follow-up

- v0.4.3: Conservative route coverage hardening for text-based arrangement and definition judgement
