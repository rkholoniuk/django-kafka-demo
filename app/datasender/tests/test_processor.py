from _datetime import timedelta
from django.test import TestCase
from datetime import datetime, timezone
from datasender.batch_processor import MessageBatchProcessor, Message
from freezegun import freeze_time


class MessageBatchProcessorBuilder:
    def __init__(self, processor, batch_size=2):
        self.processor = processor(min_batch_size=batch_size)
        self.process_messages_called = False
        self.processed_messages = []  # List to track processed messages
        self.override_process_messages()

    def override_process_messages(self):
        """Override the processor's process_messages method to track calls and perform mock processing."""

        def mock_process_messages(messages):
            self.process_messages_called = True
            for message in messages:
                # Capture each processed message
                self.processed_messages.append(message.object_cid)

        self.processor.process_messages = mock_process_messages

    def append_message(self, message_data):
        message = Message(object_cid=message_data['object_cid'],
                          time_tolerance=message_data['time_tolerance'],
                          created_date=message_data['created_date'])
        self.processor.append_message(message)

    def assert_process_messages_called(self, expected_call_state=True):
        assert self.process_messages_called is expected_call_state, \
            f"Expected process_messages to be called: {expected_call_state}, but got: {not expected_call_state}"


class MessageBatchProcessorTest(TestCase):
    def test_batch_processing_2(self):
        dsl = MessageBatchProcessorBuilder(MessageBatchProcessor, batch_size=2)

        stamp1_data = {
            'object_cid': 'cid1',
            'time_tolerance': 10,
            'created_date': datetime.now(timezone.utc)
        }
        stamp2_data = {
            'object_cid': 'cid2',
            'time_tolerance': 5,
            'created_date': datetime.now(timezone.utc)
        }
        dsl.append_message(stamp1_data)
        dsl.append_message(stamp2_data)

        # Use DSL to assert that process_messages was called
        dsl.assert_process_messages_called()

    def test_message_processing_based_on_timing(self):
        dsl = MessageBatchProcessorBuilder(MessageBatchProcessor, batch_size=2)

        # Append one message ready for immediate processing and another not ready
        dsl.append_message({
            'object_cid': 'cid_ready',
            'time_tolerance': 0,  # Ready for processing immediately
            'created_date': datetime.now(timezone.utc) - timedelta(minutes=1)
        })
        dsl.append_message({
            'object_cid': 'cid_not_ready',
            'time_tolerance': 15,  # Not ready for immediate processing
            'created_date': datetime.now(timezone.utc)
        })

        # Assert that process_messages was called
        dsl.assert_process_messages_called()

        # Assert that only one message was processed
        self.assertEqual(len(dsl.processed_messages), 1, "Only one message should have been processed")
        self.assertIn('cid_ready', dsl.processed_messages,
                      "The processed message should be the one ready for immediate processing")

    def test_message_deferred_processing_based_on_timing_and_batch_size(self):
        # Initialize DSL with a batch size of 4
        dsl = MessageBatchProcessorBuilder(MessageBatchProcessor, batch_size=4)

        # Current time for reference
        current_time = datetime.now(timezone.utc)

        # Append two messages, both not ready for immediate processing based on time_tolerance
        dsl.append_message({
            'object_cid': 'cid_not_ready_1',
            'time_tolerance': 30,  # Will be ready for processing in 30 minutes
            'created_date': current_time
        })
        dsl.append_message({
            'object_cid': 'cid_not_ready_2',
            'time_tolerance': 30,  # Will be ready for processing in 30 minutes
            'created_date': current_time
        })

        # Assert that process_messages was not called
        dsl.assert_process_messages_called(expected_call_state=False)

        # Assert that no messages were processed
        self.assertEqual(len(dsl.processed_messages), 0, "No messages should have been processed immediately")

    @freeze_time("2024-02-24")
    def test_message_processing_with_freezegun(self):
        dsl = MessageBatchProcessorBuilder(MessageBatchProcessor, batch_size=3)

        dsl.append_message({
            'object_cid': 'cid1',
            'time_tolerance': 30,  # Will be ready for processing in 30 minutes
            'created_date': datetime.now(timezone.utc)
        })

        # Assert that process_messages was not called yet
        dsl.assert_process_messages_called(expected_call_state=False)

        # Move time forward by 31 minutes and check again
        with freeze_time("2024-02-24 00:31:00"):
            # append another message that's immediately ready to process
            dsl.append_message({
                'object_cid': 'cid3',
                'time_tolerance': 0,
                'created_date': datetime.now(timezone.utc)
            })

            # Assert that process_messages was called
            dsl.assert_process_messages_called()
            self.assertEqual(len(dsl.processed_messages), 2, "All messages should have been processed after time "
                                                             "moved forward")


if __name__ == "__main__":
    unittest.main()
