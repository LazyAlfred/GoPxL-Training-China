import plotly.graph_objects as go
import numpy as np

# 模拟一个传感器扫描出的金属台阶零件
x, y = np.mgrid[-10:10:100j, -10:10:100j]
z = np.sin(x/3) + np.cos(y/3) # 模拟基础表面
z[40:60, 40:60] += 2 # 在中间制造一个“测量台阶”特征

fig = go.Figure(data=[go.Surface(z=z, x=x, y=y, colorscale='Blues')])

# 设置 3D 视图的精细参数
fig.update_layout(
    title='LMI Gocator 3D 点云模拟',
    scene=dict(xaxis_title='X (mm)', yaxis_title='Y (mm)', zaxis_title='Z (mm)'),
    width=800, height=600,
    margin=dict(l=0, r=0, b=0, t=40)
)

# 关键：把这个 3D 模型存入 docs 文件夹
fig.write_html("docs/gocator_3d.html")
print("✅ 3D 模型 gocator_3d.html 已生成！")