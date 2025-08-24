# 🤖 AI Agentic Workflow Orchestrator

A sophisticated multi-agent AI workflow orchestration system powered by OpenAI's API. This project demonstrates advanced prompt engineering, LLM orchestration, and AI engineering skills.

## 🎯 Overview

The AI Agentic Workflow Orchestrator processes complex tasks through three specialized AI agents:

1. **🔍 Research Agent** - Expands user input into comprehensive research questions
2. **📋 Planning Agent** - Generates detailed, actionable execution plans  
3. **⚡ Execution Agent** - Delivers structured final output with actionable deliverables

## ✨ Features

- **Multi-Agent Architecture**: Three specialized AI agents working in sequence
- **OpenAI API Integration**: Powered by OpenAI's latest AI technology
- **Beautiful UI**: Professional Streamlit interface with real-time progress tracking
- **Comprehensive Output**: Research analysis, planning, and actionable deliverables
- **Code Templates**: Ready-to-use code snippets and implementation guides

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-agentic-workflow-orchestrator.git
cd ai-agentic-workflow-orchestrator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy the example environment file
cp env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_actual_api_key_here
```

### 4. Run the Application
```bash
# Option 1: Use the startup script (recommended)
python start.py

# Option 2: Run directly
streamlit run app.py --server.port 8502

# Option 3: Use platform-specific scripts
# Windows: start.bat
# Unix/Linux/Mac: ./start.sh
```

### 5. Access the Application
Open your browser and go to: **http://localhost:8502**

## 🎮 How to Use

1. **Enter a Task**: Describe what you want to accomplish
2. **Add Context**: Provide additional requirements or constraints
3. **Execute Workflow**: Click "Execute Workflow" and watch the AI agents work
4. **Review Results**: Explore research findings, execution plans, and deliverables

### Example Tasks
- "Create a simple to-do list application"
- "Plan a marketing strategy for a new product"
- "Design a database schema for an e-commerce site"
- "Create a Python script to analyze sales data"

## 📁 Project Structure

```
ai-agentic-workflow-orchestrator/
├── backend/
│   ├── agents/
│   │   ├── research_agent.py      # Research Agent
│   │   ├── planning_agent.py      # Planning Agent
│   │   └── execution_agent.py     # Execution Agent
│   └── services/
│       └── openai_api.py          # OpenAI API service
├── app.py                         # Main Streamlit application
├── requirements.txt               # Python dependencies
├── env.example                    # Environment template
├── start.py                       # Startup script
├── start.bat                      # Windows startup
├── start.sh                       # Unix/Linux/Mac startup
└── README.md                      # This file
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `PROJECT_NAME`: Project name for display

### Available Models
The application uses `gpt-4o-mini` by default. You can change this in `backend/services/openai_api.py`:
```python
self.model = "gpt-4o-mini"  # Change to gpt-4o, gpt-4-turbo, etc.
```

## 🎥 Demo

📹 **Demo Video**: [Watch the demo video here](demo.mp4)

The demo shows:
- Setting up the application
- Running a sample workflow
- Exploring the multi-agent process
- Reviewing comprehensive results

## 🛠️ Development

### Running in Development Mode
```bash
streamlit run app.py --server.port 8502 --server.headless false
```

### Code Structure
- **Modular Design**: Each agent is a separate, testable module
- **Type Hints**: Full type annotation throughout
- **Async Patterns**: Modern async/await implementation
- **Error Handling**: Robust error handling and logging

## 🚀 Deployment

### Local Deployment
```bash
python start.py
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8502
CMD ["streamlit", "run", "app.py", "--server.port", "8502", "--server.address", "0.0.0.0"]
```

### Cloud Deployment
- **Heroku**: Deploy using the provided Dockerfile
- **AWS/GCP/Azure**: Deploy to cloud platforms using container services
- **Streamlit Cloud**: Deploy directly to Streamlit Cloud

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI API**: For providing the AI capabilities
- **Streamlit**: For the beautiful, interactive frontend
- **Open Source Community**: For the tools and libraries

## 📞 Support

- Create an issue in the repository
- Check the demo video for usage examples
- Review the code comments for implementation details

---

**Built with ❤️ for demonstrating AI engineering excellence**
