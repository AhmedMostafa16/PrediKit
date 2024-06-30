class DataNotFittedError(Exception):
    """Raised when transform is called before fit."""

    def __init__(
        self,
        msg="Data must be fitted first using the 'fit' method",
        *args,
        **kwargs,
    ):
        super().__init__(msg, *args, **kwargs)
