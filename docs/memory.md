# Memory System Documentation

The Letta DeepSeek Memory System uses a sophisticated approach to learn and improve over time.

## Memory Types

### 1. Core Memory
- Persistent information about coding standards
- Language-specific guidelines
- Security patterns
- Performance strategies

### 2. Archival Memory
Stores various types of information:

#### Code Snippets
```json
{
    "type": "CODE_SNIPPET",
    "code": "actual_code_here",
    "description": "what the code does",
    "category": "category_name"
}
```

#### Learning Insights
```json
{
    "type": "LEARNING_INSIGHT",
    "category": "category_name",
    "insight": "description",
    "code_example": "optional_code"
}
```

### 3. Message History
- Maintains conversation context
- Tracks user preferences
- Records problem-solving approaches

## Usage

```python
# Store a code snippet
memory_manager.save_code_snippet(
    code="code_here",
    description="what it does",
    category="algorithms"
)

# Record pattern usage
memory_manager.record_pattern_usage(
    pattern_name="factory_pattern",
    success_rating=0.9,
    context="creating database connections"
)
```