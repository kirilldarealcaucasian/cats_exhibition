class ModelConversionError(Exception):
    def __init__(self, detail: str):
        self._detail = detail

    def __str__(self):
        return f"Failed to convert to orm model: {self._detail}"
