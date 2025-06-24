from enum import Enum

class Roles(str, Enum):
    DUBBER = "dubber"
    TIMER = "timer"
    ADMIN = "admin"

class ReportStatus(str, Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    LATE = "late"