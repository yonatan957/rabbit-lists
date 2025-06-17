from app.app import make_call_back, EXCHANGE_NAME, OUTPUT_QUEUE_NAME
from app.stream_adapter import StreamAdapter
from unittest.mock import Mock

def test_stream_adapter():
    sa = StreamAdapter()
    result = sa.GetStreamChunks([1,2,3])
    assert result == [[1,2,3,1,2,1,2,1,2,1,2,1]]

def test_stream_adapter_start_with_2():
    sa = StreamAdapter()
    sa.last_added = 1
    result = sa.GetStreamChunks([1,2,3])
    assert result == [[2,1,2,3,1,2,1,2,1,2,1,2]]

def test_stream_adapter_multy_lists():
    sa = StreamAdapter()
    sa.last_added = 2
    result = sa.GetStreamChunks([5 for i in range(23)])
    assert result[0] == [6 for i in range(12)]
    assert len(result) == 2
    assert result[1][-1] == 1

def test_stream_adapter_multy_lists_start_with_2():
    sa = StreamAdapter()
    sa.last_added = 1
    result = sa.GetStreamChunks([4 for i in range(23)])
    assert len(result) == 2
    assert result[1][0] == 2

def test_callback():
    fake_channel = Mock()
    callback = make_call_back(fake_channel)

    ch = Mock()
    method = Mock()
    method.delivery_tag = "dummy_tag"
    properties = Mock()

    body = b'1,2,3'

    callback(ch, method, properties, body)

    assert fake_channel.basic_publish.called
    publish_calls = fake_channel.basic_publish.call_args_list

    assert len(publish_calls) > 0

    for call in publish_calls:
        args, kwargs = call
        assert kwargs["exchange"] == EXCHANGE_NAME
        assert kwargs["routing_key"] == OUTPUT_QUEUE_NAME
        assert isinstance(kwargs["body"], str)

    ch.basic_ack.assert_called_once_with(delivery_tag="dummy_tag")