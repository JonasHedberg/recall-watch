"""Public exception hierarchy for the recall client."""


class RecallError(Exception):
    """A recall feed could not be retrieved or interpreted."""


class RecallConnectionError(RecallError):
    """The recall feed is temporarily unreachable."""


class RecallHTTPError(RecallError):
    """The feed server returned an unexpected HTTP response."""


class RecallParseError(RecallError):
    """The feed cannot be safely interpreted as a valid feed."""
