from google.protobuf.message import Message


def assert_messages_equal(msg1: Message, msg2: Message):
    assert msg1.SerializeToString(deterministic=True) == msg2.SerializeToString(
        deterministic=True
    )
