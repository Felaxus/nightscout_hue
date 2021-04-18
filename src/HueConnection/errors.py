class HueError(Exception):
    pass


class InvalidData(HueError):
    pass


class InternalIssue(HueError):
    pass
