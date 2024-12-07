# Letta DeepSeek Coding Assistant

An intelligent coding assistant powered by Letta AI and DeepSeek V2.5, featuring advanced memory capabilities and continuous learning.

## Features

- 🧠 Advanced Memory Management
  - Stores and retrieves code snippets
  - Maintains best practices
  - Learns from interactions
  - Accumulates domain knowledge

- 💡 Intelligent Code Generation
  - Context-aware responses
  - Multiple programming languages
  - Best practices integration
  - Pattern recognition

- 📚 Continuous Learning
  - Stores successful patterns
  - Updates best practices
  - Learns from code reviews
  - Improves recommendations

- 🛠 Best Practices Categories
  - Language-specific standards
  - Security guidelines
  - Performance optimization
  - Architecture patterns
  - Testing strategies
  - API design
  - Database practices
  - Deployment guidelines

## Installation

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

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your DeepSeek API key
```

## Usage

Run the application:
```bash
python app.py
```

Access the web interface at `http://localhost:7860`

## Project Structure

```
letta-deepseek/
├── app.py                 # Main application
├── components/           # Core components
│   ├── __init__.py
│   └── memory_manager.py
├── docs/                # Documentation
├── tests/              # Test suite
├── requirements.txt    # Dependencies
└── .env.example       # Environment template
```

## Documentation

- [Setup Guide](docs/setup.md)
- [Memory System](docs/memory.md)
- [Best Practices](docs/best_practices.md)
- [API Reference](docs/api.md)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Create a pull request

## License

MIT License - see [LICENSE](LICENSE) for details