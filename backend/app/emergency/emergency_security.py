from __future__ import annotations

from routes.auth_routes import ROLE_HOSPITAL, SessionUser

UNAUTHORIZED_EMERGENCY_ACCESS_MESSAGE = "Unauthorized Emergency Access"


class UnauthorizedEmergencyAccessError(Exception):
    """Raised when non-hospital access is attempted in emergency mode."""


def enforce_emergency_access(
    *,
    role: str,
    current_user: SessionUser | None,
) -> None:
    normalized_role = role.strip().lower()
    if normalized_role != ROLE_HOSPITAL:
        raise UnauthorizedEmergencyAccessError(
            UNAUTHORIZED_EMERGENCY_ACCESS_MESSAGE
        )
    if (
        current_user is None
        or current_user.role != ROLE_HOSPITAL
        or not current_user.hospital_id
    ):
        raise UnauthorizedEmergencyAccessError(
            UNAUTHORIZED_EMERGENCY_ACCESS_MESSAGE
        )
