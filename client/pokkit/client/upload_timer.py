import threading
import queue


class DoLater(threading.Thread):
    def __init__(self, delay=1):
        self.message_queue = queue.Queue()
        self.task_queue = queue.Queue()
        self.tasks = dict()
        self.delay = 1

    def run(self):
        time.sleep(delay)

        try:
            task = self.task_queue.get_nowait()
        except queue.Empty:
            pass
        else:
            self.tasks[task[0]] = task

        try:
            message = self.message_queue.get_nowait()
        except queue.Empty:
            pass
        else:
            del self.tasks[message]

        for message, (callback, due_date) in tasks.items():
            if datetime.datetime.now() > due_date:
                callback()
                del self.tasks[message]

    def submit(self, message, task, due_date):
        self.queue
