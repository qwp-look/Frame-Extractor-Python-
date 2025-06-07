# Frame Extractor Python

> **帧提取器（Frame Extractor）：** 一个基于 Python 的视频拆帧工具，将视频文件拆分为连续的图片序列，便于后续处理与分析。

## 📖 项目简介

本项目提供了一个简洁易用的命令行工具，利用 Python 和 FFmpeg 快速将视频拆分为图片序列，支持批量处理，方便开发者与研究者对视频进行二次创作、机器学习训练或数据分析。

## 🚀 功能特性

* **支持多种视频格式**：mp4、avi、mov、mkv 等常见格式。
* **自定义帧率与分辨率**：可根据需求指定输出图片的帧率（FPS）与尺寸（宽×高）。
* **批量处理**：可对文件夹内所有视频文件进行批量拆帧。
* **进度显示**：在命令行实时显示拆帧进度。
* **插件扩展**：易于集成图像处理、风格化等二次开发。

## 📦 环境依赖

* **操作系统**：Windows、macOS、Linux
* **Python**：3.7+
* **FFmpeg**：系统环境变量中可调用 `ffmpeg` 命令

## 🔧 安装与配置

1. 克隆仓库：

   ```bash
   git clone https://github.com/qwp-look/Frame-Extractor-Python.git
   cd Frame-Extractor-Python
   ```
2. 创建并激活虚拟环境（可选）：

   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate   # Windows
   ```
3. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```
4. 确保 FFmpeg 已安装并可在命令行中调用：

   ```bash
   ffmpeg -version
   ```

## 🎬 使用方法

```bash
# 单文件拆帧：
python extract_frames.py \
  --input path/to/video.mp4 \
  --output output/images_folder \
  --fps 30 \
  --resolution 1280x720

# 批量拆帧：
python extract_frames.py \
  --input_dir path/to/videos_folder \
  --output_dir output/batch_images \
  --fps 15
```

* **参数说明**：

  * `--input`：输入视频文件路径。
  * `--input_dir`：输入视频文件夹路径，需与 `--input` 二选一。
  * `--output`：输出图片文件夹路径。
  * `--output_dir`：批量输出图片根目录。
  * `--fps`：拆帧时的帧率，默认为视频原帧率。
  * `--resolution`：输出图片分辨率，格式为 `宽x高`，默认为原视频分辨率。

## 📂 文件结构

```plain
├── extract_frames.py   # 主脚本，执行拆帧逻辑
├── requirements.txt    # Python 依赖列表
├── README_Frame_Extractor_Python.md  # 本文档
└── examples/           # 示例视频与命令
```

## 🤝 致谢 & 参考

* [FFmpeg](https://ffmpeg.org/) - 强大的多媒体处理工具
* 其他开源库：`tqdm`、`argparse` 等

*作者：qwp-look*
