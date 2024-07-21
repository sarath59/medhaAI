import time
from typing import Dict, Any, List
from ..logging_utils import setup_logger

logger = setup_logger(__name__)

class PerformanceMonitor:
    def __init__(self):
        self.tasks: List[Dict[str, Any]] = []
        self.start_time = time.time()

    def start_task(self, task: str) -> None:
        self.tasks.append({
            "task": task,
            "start_time": time.time(),
            "end_time": None,
            "duration": None
        })

    def end_task(self, task: str) -> None:
        for t in reversed(self.tasks):
            if t["task"] == task and t["end_time"] is None:
                t["end_time"] = time.time()
                t["duration"] = t["end_time"] - t["start_time"]
                break

    def get_performance_data(self) -> Dict[str, Any]:
        completed_tasks = [t for t in self.tasks if t["end_time"] is not None]
        ongoing_tasks = [t for t in self.tasks if t["end_time"] is None]
        
        return {
            "total_tasks": len(self.tasks),
            "completed_tasks": len(completed_tasks),
            "ongoing_tasks": len(ongoing_tasks),
            "average_task_duration": sum(t["duration"] for t in completed_tasks) / len(completed_tasks) if completed_tasks else 0,
            "total_runtime": time.time() - self.start_time
        }

    def generate_report(self) -> Dict[str, Any]:
        performance_data = self.get_performance_data()
        
        return {
            "performance_data": performance_data,
            "task_details": self.tasks,
            "summary": f"Completed {performance_data['completed_tasks']} out of {performance_data['total_tasks']} tasks. "
                       f"Average task duration: {performance_data['average_task_duration']:.2f} seconds. "
                       f"Total runtime: {performance_data['total_runtime']:.2f} seconds."
        }