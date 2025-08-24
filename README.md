# 🤖 AI Agentic Workflow Orchestrator

A sophisticated multi-agent AI workflow orchestration system powered by OpenAI's API. This project demonstrates advanced prompt engineering, LLM orchestration, and AI engineering skills through a production-ready application.

## 🎯 Overview

The AI Agentic Workflow Orchestrator is a stateless, multi-agent system that processes complex tasks through three specialized AI agents:

1. **🔍 Research Agent** - Expands user input into comprehensive research questions and areas
2. **📋 Planning Agent** - Generates detailed, actionable execution plans
3. **⚡ Execution Agent** - Delivers structured final output with actionable deliverables

Built with Streamlit, this project showcases modern AI engineering practices including async/await patterns, proper error handling, and modular architecture.

## ✨ Features

### Multi-Agent Architecture
- **Research Agent**: Analyzes tasks and generates comprehensive sub-questions
- **Planning Agent**: Creates detailed, step-by-step execution plans
- **Execution Agent**: Delivers structured, actionable final output

### Technical Features
- **Stateless Design**: No persistence beyond session (no database required)
- **OpenAI API Integration**: Powered by OpenAI's API
- **Async/Await Patterns**: Modern Python async programming
- **Modular Architecture**: Clean, production-like code structure
- **Professional UI**: Beautiful Streamlit interface with progress tracking
- **Error Handling**: Comprehensive error handling and validation
- **API Health Checks**: Built-in monitoring and status endpoints

### User Experience
- **Real-time Progress Tracking**: Visual progress indicators for each phase
- **Session History**: View and manage workflow history (session-based)
- **Structured Output**: Well-formatted, actionable deliverables
- **Code Templates**: Ready-to-use code snippets and templates
- **Professional Styling**: Modern, responsive UI design

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   Gemini API    │
│   Application   │◄──►│   (External)    │
└─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│   Multi-Agent   │
│   Orchestrator  │
│                 │
│  🔍 Research    │
│  📋 Planning    │
│  ⚡ Execution   │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AI-Agentic-Workflow-Orchestrator
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
PROJECT_NAME=AI Agentic Workflow Orchestrator
```

### 4. Start the Application
```bash
# Option 1: Use the startup script (recommended)
python start.py

# Option 2: Use platform-specific scripts
# Windows:
start.bat

# Unix/Linux/Mac:
./start.sh

# Option 3: Start manually
streamlit run app.py --server.port 8501
```

### 5. Access the Application
- **Main Application**: http://localhost:8501

## 📁 Project Structure

```
AI-Agentic-Workflow-Orchestrator/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── research_agent.py      # Research Agent implementation
│   │   ├── planning_agent.py      # Planning Agent implementation
│   │   └── execution_agent.py     # Execution Agent implementation
│   ├── services/
│   │   ├── __init__.py
│   │   └── gemini_api.py          # Gemini API service
│   └── __init__.py
├── app.py                         # Main Streamlit application
├── requirements.txt               # Python dependencies
├── env.example                    # Environment variables template
├── start.py                       # Easy startup script
├── start.bat                      # Windows startup script
├── start.sh                       # Unix/Linux/Mac startup script
└── README.md                      # This file
```

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `PROJECT_NAME`: Project name for display purposes

### API Endpoints
- `GET /health`: Health check endpoint
- `POST /workflow`: Main workflow orchestration endpoint
- `GET /`: API information

### Application Configuration
- **Single Port**: Everything runs on port 8501
- **Streamlit Application**: Direct access at `http://localhost:8501`
- **Session timeout**: 2 minutes for workflow execution
- **History storage**: Session-based (cleared on page refresh)

## 🎮 Usage

### 1. Start a New Workflow
1. Navigate to the "Workflow" page
2. Enter your task or problem statement
3. Add optional context or constraints
4. Click "Execute Workflow"

### 2. Monitor Progress
- Watch real-time progress indicators
- View metrics for each phase
- Track execution time and results

### 3. Review Results
- **Research Results**: View task analysis and research questions
- **Planning Results**: Examine execution phases and detailed steps
- **Execution Results**: Access deliverables, code templates, and next steps

### 4. Manage History
- View previous workflows in the "History" page
- Access detailed results from past executions
- Clear session history as needed

## 🛠️ Development

### Code Quality
- **Modular Design**: Each agent is a separate, testable module
- **Type Hints**: Full type annotation throughout the codebase
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Robust error handling and logging
- **Async Patterns**: Modern async/await implementation

### Testing
```bash
# Run backend tests (when implemented)
cd backend
python -m pytest

# Run frontend tests (when implemented)
cd frontend
streamlit test app.py
```

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Include comprehensive docstrings
- Implement proper error handling

## 🚀 Deployment

### Local Development
```bash
# Easy startup with environment checks
python start.py

# Or start manually
streamlit run app.py --server.port 8501
```

### Production Deployment

#### Option 1: Docker Deployment
```dockerfile
# Dockerfile (create this file)
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

```bash
# Build and run
docker build -t ai-workflow-orchestrator .
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key ai-workflow-orchestrator
```

#### Option 2: Cloud Deployment

**Heroku:**
```bash
# Create Procfile
echo "web: uvicorn backend.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create your-app-name
heroku config:set GEMINI_API_KEY=your_key
git push heroku main
```

**AWS/GCP/Azure:**
- Deploy FastAPI backend to cloud functions or containers
- Deploy Streamlit frontend to cloud platforms
- Configure environment variables in cloud console

### Environment Variables for Production
```bash
OPENAI_API_KEY=your_production_api_key
PROJECT_NAME=AI Agentic Workflow Orchestrator
```

## 🔒 Security Considerations

- **API Key Management**: Store Gemini API key securely in environment variables
- **CORS Configuration**: Configure CORS appropriately for production
- **Input Validation**: All user inputs are validated
- **Error Handling**: Sensitive information is not exposed in error messages
- **Rate Limiting**: Consider implementing rate limiting for production use

## 📊 Monitoring and Logging

### Backend Logging
- Structured logging with different levels
- Request/response logging
- Error tracking and reporting
- Performance metrics

### Frontend Monitoring
- API health checks
- User session tracking
- Error reporting
- Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow the existing code style
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenAI API**: For providing the AI capabilities
- **Streamlit**: For the beautiful, interactive frontend
- **Open Source Community**: For the tools and libraries that made this possible

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the troubleshooting section below

## 🔧 Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check if port 8000 is available
lsof -i :8000
# Kill process if needed
kill -9 <PID>
```

**Frontend not loading:**
```bash
# Verify backend is running
curl http://localhost:8000/health
# Check if Streamlit process started
curl http://localhost:8000/app
```

**OpenAI API errors:**
```bash
# Verify API key is set
echo $OPENAI_API_KEY
# Test API connection
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

**Memory issues:**
```bash
# Monitor memory usage
htop
# Consider reducing max_tokens in gemini_api.py
```

### Performance Optimization

- **Reduce API calls**: Implement caching where appropriate
- **Optimize prompts**: Refine system prompts for better efficiency
- **Monitor usage**: Track API usage and costs
- **Scale horizontally**: Deploy multiple instances for high load

---

**Built with ❤️ for demonstrating AI engineering excellence**
