"""Track metrics for prompts stored in MinisterOfMemory.

This module calculates various metrics from stored prompts:
- Word count per prompt
- Prompt count per session
- Average prompt length
- Topics and keywords
- XP estimates
"""

import json
import logging
import re
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import sys
workspace_root = Path(__file__).parent.parent
sys.path.insert(0, str(workspace_root))

from ministers.memory import AssistantOfMemory, MinisterOfMemory
from ministers.storage import FileStore

logger = logging.getLogger(__name__)


class MetricsTracker:
    """Tracks metrics for stored prompts."""

    def __init__(self, prompts_log_path: Path):
        """Initialize metrics tracker.
        
        Args:
            prompts_log_path: Path to prompts_log.jsonl file.
        """
        self.prompts_log_path = prompts_log_path
        file_store = FileStore(prompts_log_path)
        assistant = AssistantOfMemory(store=file_store)
        self.minister = MinisterOfMemory(assistant=assistant)

    def calculate_word_count(self, text: str) -> int:
        """Calculate word count in text.
        
        Args:
            text: Text to analyze.
            
        Returns:
            Number of words.
        """
        return len(text.split())

    def extract_keywords(self, text: str, limit: int = 10) -> List[str]:
        """Extract keywords from text (simple approach).
        
        Args:
            text: Text to analyze.
            limit: Maximum number of keywords to return.
            
        Returns:
            List of keywords.
        """
        # Common keywords in Slovak/English
        common_words = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'to', 'of', 'and', 'in', 'on', 'at', 'for', 'with', 'from', 'by',
            'a', 'áno', 'nie', 'je', 'sú', 'bol', 'bola', 'bolo', 'byť', 'som',
            'sa', 'si', 'sme', 'ste', 'sú', 'to', 'ten', 'tá', 'to', 'tí', 'tie',
        }
        
        # Simple word extraction
        words = re.findall(r'\b\w+\b', text.lower())
        words = [w for w in words if len(w) > 3 and w not in common_words]
        
        # Count frequency
        word_counts = Counter(words)
        return [word for word, _ in word_counts.most_common(limit)]

    def analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis.
        
        Args:
            text: Text to analyze.
            
        Returns:
            'positive', 'negative', or 'neutral'.
        """
        positive_words = [
            'dobrý', 'skvelý', 'super', 'výborný', 'perfektný', 'úžasný',
            'good', 'great', 'excellent', 'perfect', 'amazing', 'wonderful'
        ]
        negative_words = [
            'zlé', 'problém', 'chyba', 'nefunguje', 'zlý', 'horší',
            'bad', 'problem', 'error', 'broken', 'wrong', 'worse'
        ]
        
        text_lower = text.lower()
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        return 'neutral'

    def estimate_xp(self, word_count: int, complexity: float = 7.5) -> float:
        """Estimate XP based on word count and complexity.
        
        Uses the same algorithm as XVADUR_XP.md.
        
        Args:
            word_count: Number of words in prompt.
            complexity: Complexity score (1-10).
            
        Returns:
            Estimated XP value.
        """
        if word_count < 100:
            return 0.0
        
        # Base XP calculation (from XVADUR_XP.md)
        base_xp = (word_count / 100) * (complexity / 10) * 0.1
        return round(min(base_xp, 2.0), 2)  # Max 2.0 XP

    def calculate_session_metrics(self, session_id: Optional[str] = None) -> Dict:
        """Calculate metrics for a session or all prompts.
        
        Args:
            session_id: Optional session ID to filter by.
            
        Returns:
            Dictionary with metrics.
        """
        # Get all prompts (or filter by session)
        if session_id:
            records = self.minister.search_memories(
                lambda r: r.metadata.get('session_id') == session_id
            )
        else:
            # Get recent prompts (last 100 for performance)
            records = self.minister.review_context(limit=100)
        
        if not records:
            return {
                'prompt_count': 0,
                'total_words': 0,
                'avg_words_per_prompt': 0,
                'total_chars': 0,
                'avg_chars_per_prompt': 0,
                'keywords': [],
                'sentiment': 'neutral',
                'estimated_xp': 0.0,
            }
        
        # Calculate metrics
        total_words = sum(self.calculate_word_count(r.content) for r in records)
        total_chars = sum(len(r.content) for r in records)
        prompt_count = len(records)
        
        # Combine all text for keyword extraction
        all_text = ' '.join(r.content for r in records)
        keywords = self.extract_keywords(all_text)
        
        # Sentiment (majority)
        sentiments = [self.analyze_sentiment(r.content) for r in records]
        sentiment_counts = Counter(sentiments)
        dominant_sentiment = sentiment_counts.most_common(1)[0][0] if sentiment_counts else 'neutral'
        
        # XP estimate
        avg_complexity = 7.5  # Default, could be calculated from content
        estimated_xp = self.estimate_xp(total_words, avg_complexity)
        
        return {
            'prompt_count': prompt_count,
            'total_words': total_words,
            'avg_words_per_prompt': round(total_words / prompt_count, 1) if prompt_count > 0 else 0,
            'total_chars': total_chars,
            'avg_chars_per_prompt': round(total_chars / prompt_count, 1) if prompt_count > 0 else 0,
            'keywords': keywords,
            'sentiment': dominant_sentiment,
            'estimated_xp': estimated_xp,
            'timestamp': datetime.now().isoformat(),
        }

    def save_metrics(self, metrics: Dict, output_path: Path) -> None:
        """Save metrics to JSON file.
        
        Args:
            metrics: Metrics dictionary.
            output_path: Path to save metrics.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing metrics if file exists
        existing_metrics = []
        if output_path.exists():
            try:
                with open(output_path, 'r') as f:
                    existing_metrics = json.load(f)
            except (IOError, json.JSONDecodeError):
                pass
        
        # Append new metrics
        existing_metrics.append(metrics)
        
        # Save
        with open(output_path, 'w') as f:
            json.dump(existing_metrics, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved metrics to {output_path}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Track prompt metrics')
    parser.add_argument(
        '--prompts-log',
        type=Path,
        default=workspace_root / 'xvadur' / 'data' / 'prompts_log.jsonl',
        help='Path to prompts log file',
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=workspace_root / 'xvadur' / 'data' / 'metrics' / 'prompt_metrics.json',
        help='Path to output metrics file',
    )
    parser.add_argument(
        '--session-id',
        type=str,
        help='Optional session ID to filter by',
    )
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    tracker = MetricsTracker(args.prompts_log)
    metrics = tracker.calculate_session_metrics(session_id=args.session_id)
    
    print(f"Metrics calculated:")
    print(f"  Prompts: {metrics['prompt_count']}")
    print(f"  Total words: {metrics['total_words']}")
    print(f"  Avg words/prompt: {metrics['avg_words_per_prompt']}")
    print(f"  Estimated XP: {metrics['estimated_xp']}")
    print(f"  Keywords: {', '.join(metrics['keywords'][:5])}")
    
    tracker.save_metrics(metrics, args.output)


if __name__ == "__main__":
    main()

