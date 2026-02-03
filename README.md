# 小六壬占卜器

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/GUI-Tkinter-green.svg" alt="GUI">
  <img src="https://img.shields.io/badge/版本-3.1.0-orange.svg" alt="版本">
  <img src="https://img.shields.io/badge/许可-MIT-lightgrey.svg" alt="许可">
  <img src="https://img.shields.io/badge/平台-Windows%20|%20macOS%20|%20Linux-yellow.svg" alt="平台">
</p>

<p align="center">
  <strong>基于传统小六壬算法开发的现代化占卜应用程序</strong>
</p>

<p align="center">
  <a href="#-项目简介">项目简介</a> •
  <a href="#-功能特性">功能特性</a> •
  <a href="#-安装使用">安装使用</a> •
  <a href="#-界面截图">界面截图</a> •
  <a href="#-掌诀说明">掌诀说明</a> •
  <a href="#-开发技术">开发技术</a> •
  <a href="#-打包部署">打包部署</a> •
  <a href="#-贡献指南">贡献指南</a> •
  <a href="#-许可证">许可证</a>
</p>

## ✨ 项目简介

**小六壬占卜器** 是一款基于传统小六壬占卜算法开发的现代化GUI应用程序。它将古老的中国占卜文化与现代计算机技术相结合，为用户提供精美、易用的占卜体验。

小六壬，又称诸葛亮马前课，是中国传统占卜文化的重要组成部分，常用于占卜吉凶、预测未来、趋吉避凶。

### 📜 算法原理
```python
# 核心算法代码
def get_elements(n1, n2, n3):
    elements = ["大安", "留连", "速喜", "赤口", "小吉", "空亡", "病符", "桃花", "天德"]
    first_index = (n1 - 1) % len(elements)
    second_index = (n1 + n2 - 2) % len(elements)
    third_index = (n1 + n2 + n3 - 3) % len(elements)
    return elements[first_index], elements[second_index], elements[third_index]
```

## 📖 掌诀说明

### 六大主掌诀

| 掌诀 | 吉凶 | 属性 | 方位 | 含义 | 宜 |
|------|------|------|------|------|----|
| 大安 | ★★★★★ 大吉 | 青龙 | 东方 | 身未动时，平安吉祥 | 求财、出行、婚嫁 |
| 留连 | ★★☆☆☆ 凶 | 玄武 | 南方 | 卒未归时，拖延停滞 | 静守、等待 |
| 速喜 | ★★★★☆ 吉 | 朱雀 | 南方 | 人便至时，快速喜讯 | 求财、考试、婚嫁 |
| 赤口 | ★☆☆☆☆ 凶 | 白虎 | 西方 | 官事凶时，口舌是非 | 诉讼、争斗 |
| 小吉 | ★★★★☆ 吉 | 六合 | 东方 | 人来喜时，和合喜事 | 合作、婚嫁 |
| 空亡 | ☆☆☆☆☆ 大凶 | 勾陈 | 中央 | 音信稀时，事不遂心 | 不宜作为 |

### 额外掌诀
- **病符**：主疾病伤痛，需注意健康
- **桃花**：主人际缘分，感情机遇
- **天德**：主贵人相助，逢凶化吉

## 💻 开发技术

### 技术栈
- **编程语言**: Python 3.9+
- **GUI框架**: Tkinter
- **图形处理**: Pillow (可选)
- **打包工具**: PyInstaller

### 项目结构

### 各目录说明

- **src/**: 存放所有源代码，采用模块化设计
  - `main.py`: 程序启动入口
  - `lunar_calendar.py`: 农历日期计算功能
  - `divination_engine.py`: 核心占卜算法实现
  - `gui/`: 图形用户界面相关模块
  - `data/`: JSON格式的数据文件，便于维护和扩展

- **docs/**: 项目文档
  - `README.md`: 项目主要说明文档（即本文档）
  - `CHANGELOG.md`: 版本更新记录
  - `ARCHITECTURE.md`: 系统架构设计说明

- **tests/**: 单元测试和集成测试
  - 确保代码质量和功能正确性

- **resources/**: 静态资源文件
  - `icons/`: 应用程序图标
  - `fonts/`: 自定义字体（如需支持特殊字符）

- **scripts/**: 辅助脚本
  - `build.py`: 自动化打包脚本
  - `deploy.py`: 部署相关脚本

- **根目录文件**:
  - `requirements.txt`: Python依赖包列表
  - `setup.py`: 项目安装配置（如需打包为Python包）
  - `LICENSE`: 开源许可证文件
  - `.gitignore`: Git版本控制忽略文件列表
 
## ⚠️ 免责声明

### 法律声明
1. **非专业工具**：本软件仅为娱乐工具，不替代专业命理咨询
2. **结果参考性**：占卜结果仅供参考，不具备科学依据
3. **个人责任**：用户应对自己的决策负责，不因占卜结果做出重大决定
4. **法律责任**：开发者不对因使用本软件造成的任何损失负责

### 使用须知
1. **心理建设**：请以平常心对待占卜结果
2. **合理使用**：避免过度依赖占卜结果
3. **隐私保护**：本软件不会收集用户个人信息
4. **版权声明**：软件内传统文化内容源自公开资料

### 特别提醒
- 占卜结果不能作为医疗、法律、财务等专业决策的依据
- 如遇心理问题，请寻求专业心理咨询师帮助
- 本软件不涉及任何宗教、政治内容
- 请勿将占卜结果用于商业宣传或欺诈行为

### 风险提示
- 软件可能存在技术缺陷，结果仅供参考
- 传统文化内容可能存在解读差异
- 使用过程中如感不适，请立即停止使用

## 📞 联系方式

### 官方渠道
- **项目主页**：[GitHub仓库链接](https://github.com/Thedustye-1/divination_app)
- **官方网站**：[项目官网](https://thedustye.com)
- **问题反馈**：[Issues页面](https://github.com/Thedustye-1/divination_app/issues)
- **功能建议**：[Discussions页面](https://github.com/Thedustye-1/divination_app/discussions)
