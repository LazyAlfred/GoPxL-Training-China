# GoPxL 多传感器标定指南 
# GoPxL SDK 与二次开发配置指南

GoPxL 提供了强大的 **GoPxL SDK** 和 **REST API**，允许开发人员使用 C++ 或 C# 编写自定义的上位机客户端应用程序。与旧版固件不同，GoPxL 的底层通信架构进行了全面升级，主要依赖 **REST API 进行系统控制与配置**，并使用 **GoPxL Data Protocol (GDP) 进行高速 3D 数据传输**。

本指南将指导您如何配置开发环境、运行示例代码以及连接传感器。

---

## 1. 开发环境与支持平台 (Supported Platforms)

GoPxL SDK 的核心是基于 C++ 开发的，同时也提供了适用于 Windows 的 .NET (C#) 封装。
支持的操作系统包括：
* **Windows** 10 / 11 (32-bit 和 64-bit)
* **Linux** (Ubuntu 64-bit) [1]

---

## 2. SDK 获取与目录结构 (Project Structure)

### 2.1 下载与解压
您可以从 LMI Technologies 官方网站的下载中心获取 SDK 安装包（文件名通常类似于 `14630-x.x.x.x_SOFTWARE_GoPxL_SDK.zip`）。解压后，您会看到以下核心目录结构 [2]：

* `GoPxL_SDK_Cpp`：C++ 开发包
    * `doc`：包含详细的类参考手册和 REST API 离线文档 (`rest-api-doc.html`)。
    * `Gocator/samples`：丰富的官方示例代码工程。
    * `Platform/kApi`：LMI 的核心底层框架库。
* `GoPxL_SDK_dotNet`：C# / .NET 开发包

### 2.2 在 Visual Studio 中设置
1. 打开 Visual Studio，点击 **文件 (File) > 打开 > 项目/解决方案**。
2. 根据您的语言偏好，选择对应的 `.sln` 文件 [2]：
   * **C++**: `GoPxL_SDK_Cpp\Gocator\GoPxLSdk.sln`
   * **.NET**: `GoPxL_SDK_dotNet\Gocator\GoPxLSdkNet.sln`
3. 展开 `samples` 文件夹，您会看到预置的多个示例项目（如 `Discover`, `ConfigureSensor`, `ReceiveProfile` 等） [3]。
4. 点击顶部菜单的 **生成 (Build) > 生成解决方案** 来编译整个 SDK 及示例程序 [3]。

---

## 3. 核心通信架构解析 (Core Architecture)

在编写代码之前，了解以下几个核心类的作用非常重要 [4]：

* **`GoSystem`**：代表与 GoPxL 实例（传感器内部、GoMax 或 PC 实例）的连接。用于整体的连接与断开。
* **`GoRestClient`**：用于与传感器进行 HTTP 通信（GET, POST, PUT, DELETE）。所有的传感器配置更改（如修改曝光、触发模式）和状态读取都通过它完成 [5]。
* **`GoGdpClient`**：用于接收高速的 3D 扫描数据（GDP 协议通道）。类似旧版 SDK 的数据接收功能 [6]。

!!! info "REST API 的重要性"
    在 GoPxL 中，设置传感器参数实际上就是向传感器的特定 URI 端点发送包含 JSON 数据的 HTTP 请求。SDK 中的 `GoJson` 类提供了便捷的 JSON 负载构建方法。

---

## 4. 运行第一个示例代码 (Running Samples)

我们以配置传感器参数的示例 `ConfigureSensor` 为例：

1. 在 Visual Studio 的解决方案资源管理器中，右键点击 `ConfigureSensor` 项目，选择 **“设为启动项目 (Set as Startup Project)”** [7]。
2. 双击打开 `ConfigureSensor.cpp` 源文件。
3. 找到代码中的 IP 地址定义，将其修改为您实际的传感器 IP [8]：
   ```cpp
   constexpr const kChar* SENSOR_IP = "192.168.1.10";
(可选) 如果您的控制端口不是默认的，可以使用 system.SetControlPort(3640); 指定。
按下 F5（调试运行）或 Ctrl+F5（不调试运行），程序将连接到传感器并输出执行结果,。

--------------------------------------------------------------------------------
## 5. 编写代码：连接与配置传感器
5.1 建立连接
以下是使用 C++ 通过 GoSystem 建立连接的基础代码框架：
#include <GoPxLSdk/GoSystem.h>

void ConnectToSensor()
{
    GoSystem system;
    kIpAddress systemIpAddress;
    
    // 解析 IP 地址
    kIpAddress_Parse(&systemIpAddress, "192.168.1.10");
    system.SetAddress(systemIpAddress);
    
    // 设置默认控制端口
    system.SetControlPort(GO_PXL_SDK_DEFAULT_CONTROL_PORT);
    
    // 建立连接
    system.Connect();
    // 连接成功后可以启动传感器扫描
    // system.Start();
}
5.2 修改传感器参数 (利用 REST Client)
假设我们要通过代码将传感器的曝光时间 (Exposure) 修改为 200：
!!! tip "获取参数 URI 的秘籍" 如果您不知道某个设置的 REST URI 路径，可以打开 GoPxL 网页界面，按 F12 打开浏览器开发者工具的 Console (控制台)。然后手动在网页上修改曝光值，控制台会立刻打印出该操作对应的 method、path (URI) 和 payload (JSON 结构)。
// 1. 定义资源路径 (将 ENGINE_ID 替换为您实际的引擎ID)
const string ENGINE_ID = "LMILaserLineProfiler";
const string SENSOR_PATH = "/scan/engines/" + ENGINE_ID + "/scanners/scanner-0/sensors/sensor-0";

// 2. 构建 JSON Payload
GoJson payload(R"({
    "parameters": {
        "exposureSettings": {
            "exposureMode": 0,
            "singleExposure": 200
        }
    }
})");

// 3. 使用 REST Client 发送 Update 请求 (类似 HTTP PUT)
constexpr int REST_COMMAND_TIMEOUT_MSEC = 3000;
system.Client().Update(uri: SENSOR_PATH, content: payload).CheckResponse(REST_COMMAND_TIMEOUT_MSEC);
[参考来源：培训手册 - Configuring a Sensor]

--------------------------------------------------------------------------------
6. 接收扫描数据 (Receiving Data)
若要接收 3D 轮廓或表面数据，您必须首先在 GoPxL 的 Web 界面中开启 GDP 输出：
进入 Communicate (通信) > GDP 页面。
开启 Enable 开关。
在 Connections 列表中添加您想要输出的数据源（例如 Data > All data 或 Surface Bounding Box / Length 等测量值）,。
在上位机代码中，您可以使用 GoGdpClient 连接并接收 GoDataSet，并通过解析其内部的 GoDataMsg 获取实际的 GoSurfaceMsg 或 GoProfileMsg。详细代码可参考 SDK 中的 ReceiveSurface 或 ReceiveProfile 示例项目。