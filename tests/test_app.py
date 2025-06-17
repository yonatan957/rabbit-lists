from app.app import StreamAdapter


def test_stream_adapter():
    sa = StreamAdapter()
    result = sa.GetStreamChunks([1,2,3])
    assert result == [[1,2,3,1,2,1,2,1,2,1,2,1]]