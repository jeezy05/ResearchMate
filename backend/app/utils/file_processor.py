"""
File Processing Utilities
"""
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class FileProcessor:
    """Handles extraction of text from various file formats"""
    
    def extract_text(self, file_path: str, filename: str) -> str:
        """
        Extract text from a file based on its extension
        
        Args:
            file_path: Path to the file
            filename: Original filename
            
        Returns:
            Extracted text content
        """
        file_ext = os.path.splitext(filename)[1].lower()
        
        try:
            if file_ext == ".pdf":
                return self._extract_from_pdf(file_path)
            elif file_ext == ".txt":
                return self._extract_from_txt(file_path)
            elif file_ext == ".md":
                return self._extract_from_txt(file_path)
            elif file_ext == ".docx":
                return self._extract_from_docx(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
                
        except Exception as e:
            logger.error(f"Error extracting text from {filename}: {str(e)}")
            raise
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        try:
            import PyPDF2
            
            text_parts = []
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        text_parts.append(text)
            
            return "\n\n".join(text_parts)
            
        except ImportError:
            logger.error("PyPDF2 not installed. Install with: pip install PyPDF2")
            raise ImportError("PyPDF2 is required for PDF processing")
        except Exception as e:
            logger.error(f"Error extracting PDF: {str(e)}")
            raise
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from plain text file"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, "r", encoding="latin-1") as file:
                return file.read()
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        try:
            import docx
            
            doc = docx.Document(file_path)
            text_parts = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
            
            return "\n\n".join(text_parts)
            
        except ImportError:
            logger.error("python-docx not installed. Install with: pip install python-docx")
            raise ImportError("python-docx is required for DOCX processing")
        except Exception as e:
            logger.error(f"Error extracting DOCX: {str(e)}")
            raise


