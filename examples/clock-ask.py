from mq.component import Component
from mq.protocol import message_type, message_spec, message_pid, create_message, never_expires
import time
import json
from clock_messages import ClockRequest, ClockResponse


class ClockAsk(Component):
    """
    Simple component example.
    Asks "What time is it?" and waits result from one of the clocks in cluster.
    """

    def run(self, sched_out, contr_out, sched_in, message):
        while True:
            ask_message = create_message(b'', self.get_config().creator, never_expires, 'example_clock', 'MessagePack', 'config', ClockRequest().pack())
            self.write_log('Question sent.')
            sched_in.send(ask_message)
            while True:
                tag, msg = sched_out.recv_multipart()
                if message_type(tag) == 'result' and message_spec(tag) == 'example_clock' and message_pid(tag) == ask_message.id:
                    response = ClockResponse()
                    response.unpack(msg.data)
                    ans = str(time.asctime(time.gmtime(response.answer / 1000)))
                    self.write_log('Answer received: time is %s' % ans)
                    print("Time is %s" % ans)
                    time.sleep(1)
                    break

if __name__ == "__main__":
    comp = ClockAsk("example_clock-ask-py")
