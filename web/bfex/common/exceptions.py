class DataIngestionException(Exception):
    """Exception is thrown when the data ingestor fails to ingest and parse scraped data."""
    def __init__(self, message, code=None):
        super().__init__(message)

        # If we decide to implement logging in the future, this will be useful for tracking errors.
        self.code = code


class WorkflowException(Exception):
    """Exception is thrown when the workflow queue fails to run it's task."""
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code


class WorkflowTaskArgumentException(WorkflowException):
    """Exception is thrown when the arguments to a workflow task is invalid or missing."""
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code
