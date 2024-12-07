from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import json
from collections import defaultdict
from letta.schemas.block import Block

class MemoryOptimizer:
    def __init__(self, client, agent_id: str):
        self.client = client
        self.agent_id = agent_id
        self.block_categories = {
            'code': 'Programming code and patterns',
            'research': 'Research findings and documentation',
            'api': 'API documentation and usage',
            'best_practices': 'Best practices and guidelines',
            'patterns': 'Design patterns and architecture',
            'security': 'Security guidelines and implementations',
            'performance': 'Performance optimization techniques'
        }

    def consolidate_memory(self) -> None:
        archival_memory = self.client.get_archival_memory(self.agent_id)
        consolidated = defaultdict(list)
        
        for memory in archival_memory:
            if memory.text.startswith("DOCUMENTATION_"):
                try:
                    doc_data = json.loads(memory.text.split(": ", 1)[1])
                    key = f"{doc_data['type']}_{doc_data['content'].get('topic', '')}"
                    consolidated[key].append(doc_data)
                except json.JSONDecodeError:
                    continue

        for key, entries in consolidated.items():
            if len(entries) > 1:
                merged_entry = self._merge_entries(entries)
                self._update_memory_entries(key, merged_entry)

    def _merge_entries(self, entries: List[Dict]) -> Dict:
        entries.sort(key=lambda x: x['timestamp'], reverse=True)
        base_entry = entries[0].copy()
        
        for entry in entries[1:]:
            self._recursive_merge(base_entry['content'], entry['content'])
            
        base_entry['version'] = str(float(base_entry['version']) + 0.1)
        base_entry['merged_from'] = len(entries)
        return base_entry

    def _recursive_merge(self, base: Dict, new: Dict) -> None:
        for key, value in new.items():
            if key not in base:
                base[key] = value
            elif isinstance(base[key], dict) and isinstance(value, dict):
                self._recursive_merge(base[key], value)
            elif isinstance(base[key], list) and isinstance(value, list):
                base[key] = list(set(base[key] + value))

    def _update_memory_entries(self, key: str, merged_entry: Dict) -> None:
        block_id = f"MERGED_{key}"
        self.client.insert_archival_memory(
            self.agent_id,
            f"DOCUMENTATION_{block_id}: {json.dumps(merged_entry)}"
        )