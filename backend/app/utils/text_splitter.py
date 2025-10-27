"""
Text Splitting Utilities
"""
from typing import List
import logging

logger = logging.getLogger(__name__)


class TextSplitter:
    """Splits text into chunks for processing"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize text splitter
        
        Args:
            chunk_size: Maximum size of each chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to split
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            # Calculate end position
            end = start + self.chunk_size
            
            # If this is not the last chunk, try to break at a sentence or word boundary
            if end < text_length:
                # Look for sentence boundary (., !, ?)
                sentence_end = self._find_sentence_boundary(text, start, end)
                if sentence_end > start:
                    end = sentence_end
                else:
                    # Look for word boundary
                    word_end = self._find_word_boundary(text, start, end)
                    if word_end > start:
                        end = word_end
            
            # Extract chunk
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position, considering overlap
            start = end - self.chunk_overlap if end < text_length else text_length
        
        logger.info(f"Split text into {len(chunks)} chunks")
        return chunks
    
    def _find_sentence_boundary(self, text: str, start: int, end: int) -> int:
        """
        Find the last sentence boundary before end position
        
        Args:
            text: Full text
            start: Start position
            end: End position
            
        Returns:
            Position of sentence boundary, or -1 if not found
        """
        sentence_endings = ['. ', '! ', '? ', '.\n', '!\n', '?\n']
        
        # Search backwards from end
        search_start = max(start, end - 100)  # Don't search too far back
        substring = text[search_start:end]
        
        best_pos = -1
        for ending in sentence_endings:
            pos = substring.rfind(ending)
            if pos > best_pos:
                best_pos = pos + len(ending)
        
        if best_pos > 0:
            return search_start + best_pos
        
        return -1
    
    def _find_word_boundary(self, text: str, start: int, end: int) -> int:
        """
        Find the last word boundary before end position
        
        Args:
            text: Full text
            start: Start position
            end: End position
            
        Returns:
            Position of word boundary
        """
        # Search backwards for whitespace
        search_start = max(start, end - 50)
        substring = text[search_start:end]
        
        pos = substring.rfind(' ')
        if pos > 0:
            return search_start + pos + 1
        
        return end


