import enum


class UserType(str, enum.Enum):
    PROJECT_USER = 'project_user'
    ISSUE_USER = 'issue_user'
