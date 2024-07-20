class MedhaAIException(Exception):
    """Base exception for MedhaAI"""

class LLMError(MedhaAIException):
    """Raised when there's an error with LLM operations"""

class ToolError(MedhaAIException):
    """Raised when there's an error with tool operations"""

class ConfigError(MedhaAIException):
    """Raised when there's a configuration error"""

class WebScrapingError(ToolError):
    """Raised when there's an error during web scraping"""

class UnsupportedModelError(MedhaAIException):
    """Raised when an unsupported model is requested"""

class RateLimitError(MedhaAIException):
    """Raised when rate limit is exceeded"""