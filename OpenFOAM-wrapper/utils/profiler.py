import time


class Trace:
    def __init__(self, trace_name):
        self._trace_start = -1.
        self._trace_end = -1.
        self._trace_name = trace_name

    def start(self):
        self._trace_start = time.time()

    def end(self):
        self._trace_end = time.time()

    def __str__(self):
        return "Trace: {:>20}\tTime: {:>5}".format(self._trace_name, self._trace_end - self._trace_start)


class Profiler:
    def __init__(self, enable):
        self._enable = enable
        self._traces = {}

    def start(self, trace_name):
        if not self._enable: return
        if trace_name not in self._traces:
            self._traces[trace_name] = Trace(trace_name)
        self._traces[trace_name].start()

    def stop(self, trace_name):
        if not self._enable: return
        if trace_name not in self._traces:
            raise Exception("Start trace is not found")
        self._traces[trace_name].end()

    def print_report(self):
        if not self._enable: return
        for key, trace in self._traces.items():
            print(trace)
