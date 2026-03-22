from src.report.execution_step_result import ExecutionStepResult
from src.report.execution_report import ExecutionReport


class ExecutionTracker:

    def __init__(self):
        self.report = ExecutionReport()

    def start_run(self):
        self.report.start()

    def end_run(self):
        self.report.end()

    def start_step(self, index, action):
        result = ExecutionStepResult(
            step_index=index,
            action_type=action.action_type,
            target=action.target
        )
        result.start()
        return result

    def end_step(self, result):
        result.complete()
        self.report.add_result(result)