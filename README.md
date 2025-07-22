# RAG 知识问答系统

基于检索增强生成（RAG）技术的中文智能问答系统，支持PDF文档知识库构建和对话式问答。

## 🚀 功能特性

- 📚 **PDF文档处理**：自动解析和索引PDF文档内容
- 🔍 **语义检索**：基于FAISS向量数据库的高效相似度搜索
- 🤖 **智能问答**：集成Azure OpenAI GPT-4模型，提供准确的中文回答
- 💬 **对话记忆**：支持多轮对话，自动维护最近20条对话历史
- 🎯 **中文优化**：使用专门的中文句子嵌入模型，提升中文理解能力

## 🛠️ 技术栈

- **向量数据库**: FAISS
- **嵌入模型**: ModelScope iic/nlp_corom_sentence-embedding_chinese-base
- **大语言模型**: Azure OpenAI GPT-4
- **框架**: LangChain
- **编程语言**: Python 3.8+

## 📋 环境要求

- Python 3.8+
- 8GB+ RAM（推荐）
- 网络连接（用于访问Azure OpenAI服务）

## 🔧 安装配置

### 1. 克隆项目

```bash
git clone <your-repository-url>
cd rag-practice
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置Azure OpenAI

设置环境变量（推荐）：

**Windows PowerShell:**
```powershell
$env:OPENAI_API_KEY="your-azure-openai-api-key-here"
$env:AZURE_OPENAI_ENDPOINT="https://your-resource-name.cognitiveservices.azure.com"
$env:AZURE_OPENAI_API_VERSION="2024-02-15-preview"
$env:AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o"
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your-azure-openai-api-key-here"
export AZURE_OPENAI_ENDPOINT="https://your-resource-name.cognitiveservices.azure.com"
export AZURE_OPENAI_API_VERSION="2024-02-15-preview"
export AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4o"
```

或创建 `.env` 文件（参考 `config_example.txt`）

## 📖 使用方法

### 构建知识库

1. 将PDF文档放置在项目根目录
2. 运行索引器创建向量数据库：

```bash
python indexer.py
```

### 启动问答系统

```bash
python rag.py
```

### 交互示例

```
会话ID: xxx-xxx-xxx
请输入问题：福建天创公司主要业务是什么？
回答: 根据文档内容，福建天创公司主要从事...
当前历史记录数量: 2

请输入问题：公司的发展历程如何？
回答: 福建天创公司的发展历程...
当前历史记录数量: 4

请输入问题：exit
```

支持的退出命令：`exit`、`quit`、`退出`

## 📁 项目结构

```
rag-practice/
├── README.md                          # 项目说明文档
├── requirements.txt                    # Python依赖包
├── indexer.py                         # 文档索引构建器
├── rag.py                            # 主程序（问答系统）
├── main.py                           # 主入口文件
├── 2025中富通企业宣传ppt202505.pdf      # 示例PDF文档1
├── 福建天创公司介绍.pdf                 # 示例PDF文档2
└── tianchuang_faiss_db/              # FAISS向量数据库
    ├── index.faiss                   # 向量索引文件
    └── index.pkl                     # 元数据文件
```

## ⚙️ 核心组件

### 文档处理流程

1. **PDF解析**：提取文档文本内容
2. **文本分块**：将长文档切分为适合检索的片段
3. **向量化**：使用中文嵌入模型生成向量表示
4. **索引构建**：存储到FAISS向量数据库

### 问答流程

1. **用户提问**：接收用户自然语言问题
2. **问题向量化**：将问题转换为向量表示
3. **相似度检索**：在向量数据库中找到最相关的文档片段
4. **上下文构建**：结合检索结果和对话历史
5. **答案生成**：调用GPT-4生成准确回答

## 🔧 配置说明

### 关键参数

- **检索数量**: `k=5` - 返回Top5个最相似的文档片段
- **对话历史**: 最多保留20条历史记录
- **温度参数**: `temperature=0.7` - 控制回答的创造性
- **流式输出**: `streaming=True` - 支持实时响应

### 自定义配置

您可以根据需要调整以下参数：

```python
# 修改检索数量
retriever = vector_db.as_retriever(search_kwargs={"k": 10})

# 修改历史记录数量
if len(history.messages) > 30:  # 改为30条

# 修改温度参数
temperature=0.5  # 更保守的回答
```

## 🚨 注意事项

1. **API密钥安全**：请勿将API密钥提交到代码仓库
2. **文档格式**：目前支持PDF格式，文档应包含可提取的文本
3. **内存使用**：大型文档库可能需要更多内存
4. **网络连接**：需要稳定的网络连接访问Azure OpenAI服务

## 🐛 常见问题

### Q: 出现OpenMP库冲突警告？
A: 已在代码中设置 `KMP_DUPLICATE_LIB_OK=TRUE` 解决此问题。

### Q: FAISS加载失败？
A: 确保设置了 `allow_dangerous_deserialization=True` 参数。

### Q: 中文回答效果不佳？
A: 检查文档编码是否正确，建议使用UTF-8编码的PDF文档。

### Q: 响应速度慢？
A: 可以减少检索数量(k值)或优化文档分块大小。

## 📝 开发说明

### 添加新文档

1. 将PDF文件放入项目目录
2. 重新运行 `python indexer.py`
3. 新文档会自动加入知识库

### 自定义Prompt

在 `rag.py` 中修改系统提示词：

```python
system_prompt = SystemMessagePromptTemplate.from_template(
    "你是一个专业的企业知识库助手，请基于提供的文档内容准确回答问题。"
)
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request来帮助改进项目！

---

**注意**：使用前请确保已正确配置Azure OpenAI服务，并拥有有效的API密钥。 