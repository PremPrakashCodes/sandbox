import enum


class ApiScope(enum.Enum):
    """API key permission scopes"""

    # Sandbox
    WRITE_SANDBOX = "write:sandbox"
    DELETE_SANDBOX = "delete:sandbox"

    # Snapshots
    WRITE_SNAPSHOTS = "write:snapshots"
    DELETE_SNAPSHOTS = "delete:snapshots"

    # Registries
    WRITE_REGISTRIES = "write:registries"
    DELETE_REGISTRIES = "delete:registries"

    # Volumes
    READ_VOLUMES = "read:volumes"
    WRITE_VOLUMES = "write:volumes"
    DELETE_VOLUMES = "delete:volumes"


class OrganizationRole(enum.Enum):
    """Organization member roles"""
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"