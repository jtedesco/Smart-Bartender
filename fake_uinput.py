_fake = lambda x: x 

class _FakeClass(object):

    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self, *args, **kwargs):
        pass

    def __exit__(self, *args, **kwargs):
        pass


Device = _FakeClass
KEY_ENTER = _fake
KEY_RIGHT = _fake
