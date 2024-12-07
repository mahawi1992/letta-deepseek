from typing import Dict, Any, List, Optional
from datetime import datetime
import json

class EnhancedDocumentation:
    def __init__(self, client, agent_id: str):
        self.client = client
        self.agent_id = agent_id
        self.score_weights = {
            'keyword_match': 0.4,
            'recency': 0.3,
            'complexity_match': 0.2,
            'category_match': 0.1
        }

    async def store_documentation(self, doc_type: str, content: Dict[str, Any], metadata: Dict[str, Any]) -> None:
        """Store documentation with enhanced metadata and categorization"""
        doc_data = {
            "type": doc_type,
            "content": content,
            "metadata": {
                **metadata,
                "timestamp": str(datetime.now()),
                "version": "1.0",
                "keywords": self._extract_keywords(content),
                "category": self._categorize_content(content),
                "language": self._detect_language(content),
                "complexity": self._assess_complexity(content),
                "readability_score": self._calculate_readability(content)
            }
        }
        
        # Check for similar existing documents
        similar_docs = await self.search_documentation(
            json.dumps(content),
            {"category": doc_data["metadata"]["category"]}
        )
        
        if similar_docs:
            # Update existing document if similar
            doc_data["metadata"]["version"] = self._increment_version(
                similar_docs[0]["metadata"]["version"]
            )
            doc_data["metadata"]["previous_version"] = similar_docs[0]["metadata"]["version"]
        
        self.client.insert_archival_memory(
            self.agent_id,
            f"DOCUMENTATION_{doc_type}_{doc_data['metadata']['category']}: {json.dumps(doc_data)}"
        )

    async def search_documentation(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search documentation with advanced filtering and ranking"""
        results = []
        archival_memory = self.client.get_archival_memory(self.agent_id)
        
        for memory in archival_memory:
            if not memory.text.startswith("DOCUMENTATION_"):
                continue
                
            try:
                doc_data = json.loads(memory.text.split(": ", 1)[1])
                if self._matches_filters(doc_data, filters):
                    relevance_score = self._calculate_relevance(doc_data, query)
                    results.append((doc_data, relevance_score))
            except json.JSONDecodeError:
                continue
        
        # Sort by relevance score and extract just the documents
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        return [doc for doc, score in sorted_results]

    def _increment_version(self, version: str) -> str:
        """Increment document version"""
        try:
            major, minor = version.split('.')
            return f"{major}.{int(minor) + 1}"
        except ValueError:
            return "1.1"

    def _calculate_readability(self, content: Dict[str, Any]) -> float:
        """Calculate readability score for content"""
        text = json.dumps(content)
        words = text.split()
        sentences = text.split('.')
        
        if not sentences:
            return 0.0
            
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        avg_sentence_length = len(words) / len(sentences)
        
        # Simple readability score (lower is more readable)
        return (avg_word_length * 0.5 + avg_sentence_length * 0.5) / 10

    def _calculate_relevance(self, doc: Dict[str, Any], query: str) -> float:
        """Calculate document relevance score"""
        query_terms = query.lower().split()
        doc_text = json.dumps(doc).lower()
        
        # Keyword matching score
        keyword_score = sum(term in doc_text for term in query_terms) / len(query_terms)
        
        # Recency score
        days_old = (datetime.now() - datetime.fromisoformat(doc['metadata']['timestamp'])).days
        recency_score = max(0, 1 - (days_old / 365))
        
        # Complexity matching score (prefer documents matching query complexity)
        query_complexity = self._assess_complexity({'content': query})
        complexity_match = 1 if query_complexity == doc['metadata']['complexity'] else 0.5
        
        # Category relevance
        category_score = 1 if any(term in doc['metadata']['category'] for term in query_terms) else 0.5
        
        # Weighted average of scores
        return (
            keyword_score * self.score_weights['keyword_match'] +
            recency_score * self.score_weights['recency'] +
            complexity_match * self.score_weights['complexity_match'] +
            category_score * self.score_weights['category_match']
        )

    def _assess_complexity(self, content: Dict[str, Any]) -> str:
        """Assess content complexity"""
        text = json.dumps(content).lower()
        
        # Complexity indicators dictionary
        complexity_indicators = {
            'high': [
                'advanced', 'complex', 'sophisticated', 'optimization',
                'distributed', 'concurrent', 'scalable', 'enterprise'
            ],
            'medium': [
                'intermediate', 'moderate', 'standard', 'implementation',
                'integration', 'component', 'module'
            ],
            'low': [
                'basic', 'simple', 'beginner', 'introduction',
                'starter', 'fundamental', 'easy'
            ]
        }
        
        # Count occurrences of each complexity level's indicators
        scores = {}
        for level, indicators in complexity_indicators.items():
            scores[level] = sum(text.count(indicator) for indicator in indicators)
        
        # Return the complexity level with highest score, default to medium
        return max(scores.items(), key=lambda x: x[1])[0] if any(scores.values()) else 'medium'

    def _matches_filters(self, doc: Dict[str, Any], filters: Optional[Dict[str, Any]]) -> bool:
        """Check if document matches specified filters"""
        if not filters:
            return True
            
        metadata = doc.get('metadata', {})
        
        # Enhanced filter matching
        for key, value in filters.items():
            if key not in metadata:
                return False
                
            if isinstance(value, list):
                if not any(v == metadata[key] for v in value):
                    return False
            elif isinstance(value, dict):
                if not all(self._check_filter_condition(metadata[key], op, val)
                          for op, val in value.items()):
                    return False
            elif metadata[key] != value:
                return False
        
        return True

    def _check_filter_condition(self, value: Any, operator: str, target: Any) -> bool:
        """Check if value matches filter condition"""
        operators = {
            'gt': lambda x, y: x > y,
            'gte': lambda x, y: x >= y,
            'lt': lambda x, y: x < y,
            'lte': lambda x, y: x <= y,
            'contains': lambda x, y: y in x if isinstance(x, (str, list)) else False,
            'in': lambda x, y: x in y if isinstance(y, (list, tuple)) else False
        }
        
        return operators.get(operator, lambda x, y: x == y)(value, target)