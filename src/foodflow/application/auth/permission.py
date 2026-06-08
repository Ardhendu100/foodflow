from fastapi import Depends, HTTPException, status

from foodflow.application.auth.dependencies import (
    get_current_user,
)
from foodflow.domain.models.user import User


def require_permission(
    permission_name: str,
):
    def permission_checker(
        current_user: User = Depends(get_current_user),
    ):
        permissions = set()

        for user_role in current_user.user_roles:
            role = user_role.role

            for role_permission in role.role_permissions:
                permissions.add(role_permission.permission.name)

        if permission_name not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {permission_name}",
            )

    return permission_checker
