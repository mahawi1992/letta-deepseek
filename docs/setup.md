# Setup Guide

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/letta-deepseek.git
cd letta-deepseek
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys:
# - DEEPSEEK_API_KEY
# - TAVILY_API_KEY
```

5. Run the application:
```bash
python app.py
```

## Lightning AI Deployment

1. Go to [Lightning AI](https://lightning.ai)
2. Create new project
3. Import from GitHub
4. Configure environment variables
5. Deploy

### Environment Variables

Required environment variables:
- `DEEPSEEK_API_KEY`: Your DeepSeek API key
- `TAVILY_API_KEY`: Your Tavily API key

### Resource Requirements

Minimum requirements:
- CPU: 2 cores
- RAM: 4GB
- Storage: 10GB

## Architecture Overview

Components:
1. Research Agent: Technical research using Tavily
2. Coding Agent: Implementation using DeepSeek
3. Memory Manager: Knowledge optimization
4. Documentation System: Information storage and retrieval

## Development Workflow

1. Make changes locally
2. Test with `python app.py`
3. Deploy to Lightning AI
4. Monitor deployment

## Getting Help

- Check [Lightning AI Documentation](https://lightning.ai/docs)
- Review [Letta Documentation](https://docs.letta.com)
- File issues on GitHub