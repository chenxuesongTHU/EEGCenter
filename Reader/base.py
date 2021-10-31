class BaseReader:
    def __init__(self, file_name, annotation_file=None):
        self._file_name = file_name
        self._anno_file = annotation_file
        self._raw = None
        self._anno = None

    @property
    def raw(self):
        return self._raw

    @property
    def anno(self):
        return self._anno
