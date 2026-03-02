# GoPxL 传感器操作指南 🚀

欢迎来到 LMI Gocator 新一代培训教材。本手册通过交互式示例，帮助你快速掌握传感器配置。

---

## 🛠️ 快速连接步骤
1. 将电脑 IP 设置为 `192.168.1.x` 频段。
2. 打开浏览器，输入传感器的默认地址：
   `http://192.168.1.10`

!!! tip "小技巧"
    如果无法连接，请检查网线是否连接到传感器的 **Power/LAN** 接口。

## 📐 核心算法原理
传感器通过激光三角测量法获取数据。 $Z$ 轴的测量精度取决于：

$$
Accuracy_z = \frac{Range}{2^{Resolution}}
$$

## 💻 Python SDK 示例
你可以直接复制以下代码来初始化传感器：

```python
import gocator
device = gocator.Device("192.168.1.10")
device.connect()
print("连接成功！")
```

## 3D 扫描数据预览（实时交互）

<iframe src="gocator_3d.html" width="100%" height="650px" frameborder="0" scrolling="no"></iframe>

> 💡 **提示**：你可以用鼠标在上方窗口中旋转、缩放模型，查看测量表面的细节。