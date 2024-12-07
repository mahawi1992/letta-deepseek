# Memory System Documentation

The Letta DeepSeek Coding Assistant uses a sophisticated memory system to learn and improve over time.

## Memory Types

### 1. Core Memory
- Persistent information about coding standards and best practices
- Language-specific guidelines
- Security patterns
- Performance optimization strategies
- Architecture patterns

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

#### Pattern Usage
```json
{
    "type": "PATTERN_USAGE",
    "pattern": "pattern_name",
    "success_rating": 0.95,
    "context": "usage_context"
}
```

#### Code Reviews
```json
{
    "type": "CODE_REVIEW",
    "code": "reviewed_code",
    "feedback": {
        "quality": "rating",
        "suggestions": ["list", "of", "suggestions"]
    }
}
```

### 3. Message History
- Maintains conversation context
- Tracks user preferences
- Records problem-solving approaches

## Memory Features

1. Pattern Recognition
   - Tracks successful code patterns
   - Learns from usage context
   - Measures pattern effectiveness

2. Learning System
   - Accumulates coding insights
   - Updates best practices
   - Improves recommendations

3. Code Review Learning
   - Stores review feedback
   - Updates coding standards
   - Improves future suggestions

## Usage Example

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

# Save learning insight
memory_manager.save_learning_insight(
    category="performance",
    insight="Connection pooling improves database performance",
    code_example="example_code"
)
```