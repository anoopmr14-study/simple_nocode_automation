class ExecutionReport:
    def __init__(self):
        self.results = []
        self.start_time = None
        self.end_time = None

    def start(self):
        import time
        self.start_time = time.time()

    def end(self):
        import time
        self.end_time = time.time()

    def add_result(self, result):
        self.results.append(result)

    def summary(self):
        total = len(self.results)
        success = len([r for r in self.results if r.status == "SUCCESS"])
        failed = len([r for r in self.results if r.status == "FAILED"])

        return {
            "total": total,
            "success": success,
            "failed": failed,
            "duration": round(self.end_time - self.start_time, 2)
        }