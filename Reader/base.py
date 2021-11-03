class BaseReader:
    def __init__(self, file_name, annotation_file=None):
        self._file_name = file_name
        self._anno_file = annotation_file
        self._raw = None

    @property
    def raw(self):
        return self._raw
