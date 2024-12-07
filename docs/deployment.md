# Deployment Guide

## Prerequisites
1. Lightning AI account
2. DeepSeek API key
3. Tavily API key

## Local Setup
```bash
# Clone repository
git clone https://github.com/yourusername/letta-deepseek.git
cd letta-deepseek

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

## Lightning AI Deployment

1. Go to [Lightning AI](https://lightning.ai)
2. Create new project
3. Import from GitHub
4. Set environment variables:
   - DEEPSEEK_API_KEY
   - TAVILY_API_KEY
5. Deploy

## Monitoring

### Health Checks
- Monitor agent memory usage
- Check API response times
- Monitor error rates

### Optimization
- Regular memory consolidation
- Cleanup old workflows
- Update performance metrics