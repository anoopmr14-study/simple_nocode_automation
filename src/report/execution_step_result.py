class ExecutionStepResult:
    def __init__(
        self,
        step_index,
        action_type,
        target=None
    ):
        self.step_index = step_index
        self.action_type = action_type
        self.target = target

        self.status = "PENDING"   # SUCCESS / FAILED
        self.message = ""
        self.start_time = None
        self.end_time = None
        self.duration = 0

    def mark_success(self):
        self.status = "SUCCESS"

    def mark_failed(self, message):
        self.status = "FAILED"
        self.message = message

    def complete(self):
        import time
        self.end_time = time.time()
        self.duration = round(self.end_time - self.start_time, 3)

    def start(self):
        import time
        self.start_time = time.time()