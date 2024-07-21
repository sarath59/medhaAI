from typing import Dict, Any, Optional
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.trace.status import Status, StatusCode
from ..logging_utils import setup_logger

logger = setup_logger(__name__)

tracer_provider = TracerProvider()
tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer(__name__)

class Tracer:
    @staticmethod
    def trace(func):
        async def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(func.__name__) as span:
                try:
                    result = await func(*args, **kwargs)
                    span.set_attribute("result", str(result)[:1000])  # Limit result size
                    return result
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise
        return wrapper

    @staticmethod
    def log_llm_call(provider: str, model: str, prompt: str, response: str, duration: float):
        with tracer.start_as_current_span("llm_call") as span:
            span.set_attribute("provider", provider)
            span.set_attribute("model", model)
            span.set_attribute("prompt", prompt[:1000])  # Limit prompt size
            span.set_attribute("response", response[:1000])  # Limit response size
            span.set_attribute("duration", duration)

    @staticmethod
    def log_agent_interaction(agent_name: str, action: str, input_data: Optional[str] = None, output_data: Optional[str] = None):
        with tracer.start_as_current_span("agent_interaction") as span:
            span.set_attribute("agent_name", agent_name)
            span.set_attribute("action", action)
            if input_data:
                span.set_attribute("input", input_data[:1000])  # Limit input size
            if output_data:
                span.set_attribute("output", output_data[:1000])  # Limit output size

    @staticmethod
    def log_error(error_type: str, error_message: str, stack_trace: str):
        with tracer.start_as_current_span("error") as span:
            span.set_status(Status(StatusCode.ERROR))
            span.set_attribute("error_type", error_type)
            span.set_attribute("error_message", error_message)
            span.set_attribute("stack_trace", stack_trace)