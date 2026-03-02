# GoPxL Python 脚本与 GDK

Python GDK (Generic Development Kit) 允许用户在 GoPxL 环境中直接编写 Python 脚本来处理数据、创建自定义测量工具或实现复杂的逻辑控制。

## 1. 什么是 Python GDK？

Python GDK 提供了一个集成开发环境，使你能够：
* **自定义处理**：在传感器原始数据（如 Profile 或 Surface）上运行自定义算法。
* **数据访问**：访问传感器生成的点云、强度图以及测量结果。
* **无缝集成**：将 Python 脚本作为一个“工具”直接添加到 GoPxL 的工具流水线（Toolchain）中。

!!! info "优势"
    无需在外部 PC 上安装复杂的 SDK 环境，直接在 GoPxL 界面内即可完成开发与部署。

---

## 2. 环境配置与准备

在开始编写脚本之前，请确保以下配置正确：

### 2.1 依赖安装
GoPxL 内部集成了一个标准的 Python 运行时环境，并预装了常用的科学计算库：
* **NumPy**: 用于高性能矩阵运算。
* **SciPy**: 用于高级科学计算和信号处理。
* **OpenCV (cv2)**: 用于图像处理任务。

### 2.2 资源限制
!!! warning "性能注意"
    Python 脚本运行在传感器的控制器内（或 GoPxL 运行的主机上）。复杂的算法可能会增加系统的 **Cycle Time**（循环时间）。在生产环境下，请务必监控执行耗时。

---

## 3. 开发流程 (Workflow)

要在 GoPxL 中使用 Python 工具，通常遵循以下步骤：

1. **添加工具**：在 GoPxL 工具栏中，点击 `+` 号并搜索 `Python Script`。
2. **编写代码**：在代码编辑器窗口编写处理逻辑。
3. **定义输入/输出**：
    * **Inputs**: 选择要处理的数据源（如 `Surface 1`）。
    * **Outputs**: 定义脚本返回的结果（如数字结果或处理后的几何体）。
4. **调试与执行**：点击 `Run` 观察输出结果，并在底部的 `Log Console` 查看报错信息。

---

## 4. 核心代码结构模板

下面是一个典型的 GoPxL Python 脚本结构：

```python
import numpy as np

def OnReceive(data):
    """
    这是脚本的核心入口函数。每当传感器产生新数据时，该函数会被调用。
    """
    # 1. 获取输入数据
    # 假设输入是一个 Surface
    surface = data.inputs[0]
    
    # 2. 算法处理 (示例：计算表面平均高度)
    if surface is not None:
        z_data = surface.z_offsets
        avg_height = np.nanmean(z_data)
        
        # 3. 输出结果
        # 将结果发送到 GoPxL 的测量值列表
        data.outputs[0].value = avg_height
        data.outputs[0].enabled = True
    else:
        data.outputs[0].enabled = False

    # 在控制台打印日志以便调试
    print(f"Current Average Height: {avg_height:.3f} mm")
    
## 5. 调试技巧与最佳实践

在编写 Python GDK 脚本时，遵循以下实践可以显著提高工具的稳定性和执行效率。

### 5.1 使用日志控制台 (Log Console)
使用标准 Python 的 `print()` 函数即可将调试信息输出到 GoPxL 界面底部的 **Log Console**。
* **用途**：打印中间变量、确认数据维度（`shape`）或捕捉异常。
* **注意**：在生产环境（正式上线）时，请减少 `print` 的频率，以免过多的 I/O 影响系统性能。

### 5.2 高效处理无效数据 (NaN)
3D 扫描数据中经常包含无效点（由于阴影或材质吸收导致的 NaN）。
!!! tip "计算建议"
    使用 NumPy 时，务必使用带 `nan` 前缀的函数，例如：
    * `np.nanmean(data)`：计算平均值并自动忽略 NaN。
    * `np.nanmax(data)`：获取最大高度值。
    * `np.nan_to_num(data, nan=0.0)`：将所有无效点替换为 0。

### 5.3 性能与内存优化
!!! warning "避免内存泄漏"
    尽量避免在 `OnReceive` 循环内部声明巨大的临时矩阵。如果需要进行复杂的矩阵运算，建议预先定义好缓冲区或利用 NumPy 的原位运算（In-place operations）。

---

## 6. 常见应用场景示例

Python GDK 极大地扩展了 GoPxL 的边界，常见的定制化场景包括：

* **自定义几何拟合**：官方工具无法处理的特殊形状（如不规则曲线）的拟合。
* **多工具结果逻辑组合**：根据多个测量工具的结果，编写复杂的 `If-Else` 逻辑来判定最终的 OK/NG。
* **数据格式定制化输出**：将点云坐标按照特定的协议格式化，通过 TCP/UDP 发送给第三方上位机。

---

## 7. 快速参考：常用 API 对象

| 对象 | 描述 |
| :--- | :--- |
| `data.inputs` | 获取输入流数据（如 Surface, Profile, Measurement） |
| `data.outputs` | 设置输出结果（如 Value, Decision, Geometry） |
| `surface.z_offsets` | 获取 3D 表面的高度矩阵 (2D NumPy Array) |
| `surface.x_resolution` | 获取 X 方向的物理分辨率（单位：mm/pixel） |

---

## 8. 常见问题排查 (Troubleshooting)

| 现象 | 可能原因 | 解决建议 |
| :--- | :--- | :--- |
| **脚本执行变慢** | 循环计算过于复杂 | 使用 NumPy 的矢量化运算代替 `for` 循环 |
| **结果全为 NaN** | 输入数据质量差 | 检查传感器曝光设置，或在脚本中加入数据预处理 |
| **输出不更新** | 未设置 `enabled = True` | 确保在脚本结尾设置 `data.outputs[0].enabled = True` |