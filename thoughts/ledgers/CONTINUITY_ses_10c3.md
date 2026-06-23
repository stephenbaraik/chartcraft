---
session: ses_10c3
updated: 2026-06-23T09:50:00.915Z
---

Let me try running the example app directly.

<｜｜DSML｜｜tool_calls>
<｜｜DSML｜｜invoke name="bash">
<｜｜DSML｜｜parameter name="command" string="true">cd /home/steve/Documents/chartcraft && python example_app.py 2>&1</｜｜DSML｜｜parameter>
<｜｜DSML｜｜parameter name="timeout" string="false">10000</｜｜DSML｜｜parameter>
</｜｜DSML｜｜invoke>
</｜｜DSML｜｜tool_calls>
