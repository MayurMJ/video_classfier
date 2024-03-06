import zmq
import signal
import sys
import threading
from collections import defaultdict


def sigint_handler(signal, frame):
    print("SIGINT received. Exiting...")
    sys.exit(0)


def main() -> None:
    signal.signal(signal.SIGINT, sigint_handler)
    reporter = stats_reporter()
    reporter.init()
    pass

class stats_reporter:
    m_context = None
    m_socket = None
    m_classification_map = None
    m_map_mutex = None 

    def init(self):
        self.m_context = zmq.Context()
        self.m_socket = self.m_context.socket(zmq.SUB)
        self.m_socket.connect("tcp://127.0.0.1:1234")
        self.m_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.m_classification_map = defaultdict(int)
        self.m_map_mutex = threading.Lock()
        self.report_stats()
        self.receive_message()

    def receive_message(self):
        while True:
            message = self.m_socket.recv_pyobj()
            #print(f"Received message: {message}")
            self.m_map_mutex.acquire()
            self.m_classification_map[message] += 1
            self.m_map_mutex.release()
            
    def report_stats(self):
        self.m_map_mutex.acquire()
        for key, value in self.m_classification_map.items():
            message = "class " + str(key)  + " detected " + str(value) + " times."
            print(message)
        self.m_classification_map.clear()
        self.m_map_mutex.release()
        threading.Timer(10, self.report_stats).start()


if __name__ == "__main__":
    main()
