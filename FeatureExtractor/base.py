__all__ = ["FREQ_BANDS", "BaseFeature"]

FREQ_BANDS = {
    "delta": [0.5, 4],  # 1-3
    "theta": [4, 8],  # 4-7
    "alpha": [8, 13],  # 8-12
    "beta": [13, 31],  # 13-30
    "gamma": [31, 81]  # 31-80
}


class BaseFeature:
    def __init__(self, raw, picks):
        self._raw = raw
        self._value = None
        self._picks = picks

    @property
    def raw(self):
        return self._raw

    @property
    def value(self):
        return self._value

    def save_feature(self, outfile_name):
        pass
