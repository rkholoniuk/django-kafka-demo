from typing import List, Dict
import datetime
from datetime import datetime, timedelta, timezone


class Message:
    def __init__(self, object_cid: str, time_tolerance: int, created_date: datetime):
        self.object_cid = object_cid
        self.time_tolerance = time_tolerance
        self.created_date = created_date

    def is_ready_for_processing(self) -> bool:
        """Determine if the message is ready for processing by date."""
        process_after = self.created_date + timedelta(minutes=self.time_tolerance)
        return datetime.now(timezone.utc) >= process_after


class MessageBatchProcessor:
    def __init__(self, min_batch_size: int = 2, max_batch_size: int = 10) -> None:
        """
        Initializes the MessageBatchProcessor with a specified batch size.

        :param batch_size: The number of messages to accumulate before processing the batch.
        """
        self.min_batch_size: int = min_batch_size
        self.max_batch_size: int = max_batch_size
        self.messages: List[Message] = []  # Use Message instances

    def append_message(self, message: Message) -> None:
        """Append a Message to the batch."""
        self.messages.append(message)
        self.check_and_process_messages()

    def check_and_process_messages(self) -> None:
        """Check if messages are ready to be processed based on batch size or timing."""

        if len(self.messages) >= self.min_batch_size:
            self.process_messages(self.messages)
            self.messages.clear()
        else:
            ready_to_process = [msg for msg in self.messages if msg.is_ready_for_processing()]
            if len(ready_to_process) > 0:
                self.process_messages(ready_to_process)
                self.messages = [msg for msg in self.messages if msg not in ready_to_process]

    def process_messages(self, messages: List[Message]) -> None:
        """Process a batch of messages that are ready."""
        print(f"Processing batch of {len(messages)} messages")
        for message in messages:
            print(f"Processing: {message.object_cid}")

        # if len(self.messages) <= self.max_batch_size:
        #     for message in messages:
        #         print(f"Processing: {message.object_cid}")
        # else:
        #     split_arrays = []
        #     for i in range(0, len(self.messages), self.max_batch_size):
        #         split_array = self.messages[i:i + self.max_batch_size]
        #         split_arrays.append(split_array)
        #         self.process_messages(split_array)
