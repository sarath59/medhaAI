class MedhaAIException(Exception):
    """Base exception for MedhaAI"""

class LLMError(MedhaAIException):
    """Raised when there's an error with LLM operations"""

class MemoryError(MedhaAIException):
    """Raised when there's an error with memory operations"""

class PlanningError(MedhaAIException):
    """Raised when there's an error in planning"""

class ExecutionError(MedhaAIException):
    """Raised when there's an error in execution"""

class ToolError(MedhaAIException):
    """Raised when there's an error with tool operations"""

class AgentError(MedhaAIException):
    """Raised when there's an error in agent operations"""

class MultiAgentSystemError(MedhaAIException):
    """Raised when there's an error in multi-agent system operations"""