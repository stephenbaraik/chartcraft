---
session: ses_10c3
updated: 2026-06-23T09:55:49.192Z
---

Let me serve the dashboard first, then provide the summary. I'll run it in the background so it stays up:

<｜｜DSML｜｜tool_calls>
<｜｜DSML｜｜invoke name="bash">
<｜｜DSML｜｜parameter name="command" string="true">cd /home/steve/Documents/chartcraft && nohup python3 -c "
import chartcraft as cc

# Build the dashboard from the example
data = cc.Data({
    'month': ['Jan','Feb','Mar','Apr','May','Jun'],
    'sales': [100,150,200,180,220,250],
    'profit': [20,35,50,40,60,70],
    'expenses': [80,115,150,140,160,180]
})

bar_chart = cc.bar(data, title='Monthly Sales Performance', x='month', y='sales')
line_chart = cc.line(data, title='Profit Trend', x='month', y='profit')
area_chart = cc.area(data, title='Expenses Over Time', x='month', y='expenses')
pie_data = cc.Data({'status': ['Active','Inactive','Pending'], 'count': [450, 120, 80]})
pie_chart = cc.pie(pie_data, title='Account Distribution')

dashboard = cc.Dashboard(title='ChartCraft Demo Dashboard', charts=[bar_chart, line_chart, area_chart, pie_chart])
cc.serve(dashboard, port=8050)
" > /tmp/chartcraft_server.log 2>&1 &
echo "Server PID: $!"</｜｜DSML｜｜parameter>
<｜｜DSML｜｜parameter name="description" string="true">Start ChartCraft dashboard server in background</｜｜DSML｜｜parameter>
<｜｜DSML｜｜parameter name="timeout" string="false">10000</｜｜DSML｜｜parameter>
</｜｜DSML｜｜invoke>
</｜｜DSML｜｜tool_calls>
