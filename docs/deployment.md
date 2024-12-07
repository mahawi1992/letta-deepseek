# Deployment Guide for Lightning AI

## Prerequisites
1. Lightning AI account (https://lightning.ai)
2. DeepSeek API key
3. Tavily API key
4. Git repository access

## Deployment Steps

### 1. Local Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/letta-deepseek.git
cd letta-deepseek

# Create virtual environment
python -m venv venv
source venv/bin/activate  # For Linux/Mac
# or
.\venv\Scripts\activate   # For Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup
Create `.env` file with your API keys:
```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 3. Lightning AI Deployment

1. Log in to Lightning AI (https://lightning.ai)
2. Create a new project
3. Go to Project Settings
4. Add Environment Variables:
   - DEEPSEEK_API_KEY
   - TAVILY_API_KEY
5. Deploy the app:
   - Choose "Deploy from Git"
   - Select your repository
   - Choose main branch
   - Select app.py as entry point

### 4. Monitor Deployment
- Check build logs for any issues
- Monitor resource usage
- Test the application endpoints

## Directory Structure
```
letta-deepseek/
├── app.py                 # Main application
├── components/           # Agent components
├── docs/                # Documentation
├── .env.example        # Environment template
├── .lightning          # Lightning AI config
├── requirements.txt    # Dependencies
└── README.md          # Project documentation
```

## Deployment Configuration

### Lightning AI Config (.lightning)
```yaml
name: letta-deepseek
requirements:
  - lightning>=2.1.0
  - gradio>=4.0.0
  - letta>=0.2.0
  # ... other dependencies

compute:
  instance_type: cpu-medium
  disk_size: 10GB

env:
  DEEPSEEK_API_KEY: ${DEEPSEEK_API_KEY}
  TAVILY_API_KEY: ${TAVILY_API_KEY}
```

### Resource Requirements
- CPU: 2 cores minimum
- RAM: 4GB minimum
- Storage: 10GB minimum

## Monitoring and Maintenance

### Health Checks
- Monitor agent memory usage
- Check API response times
- Monitor error rates

### Optimization
- Regular memory consolidation
- Cleanup old workflows
- Update performance metrics

## Troubleshooting

### Common Issues
1. Memory Issues
   - Increase disk size in .lightning config
   - Run memory optimization more frequently

2. API Issues
   - Verify API keys in environment variables
   - Check API quota limits

3. Performance Issues
   - Adjust compute resources
   - Optimize memory usage
   - Configure caching

### Getting Help
- Check Lightning AI documentation
- Review Letta documentation
- Contact support team