from foodflow.infrastructure.database.session import SessionLocal

from foodflow.domain.models.user import User
from foodflow.domain.models.role import Role
from foodflow.domain.models.permission import Permission
from foodflow.domain.models.user_role import UserRole
from foodflow.domain.models.role_permission import RolePermission


ROLES = [
    "App Admin",
    "Customer",
    "Restaurant Owner",
    "Delivery Partner",
]


PERMISSIONS = [
    "admin:access",
    "restaurant:create",
    "restaurant:update",
    "restaurant:delete",
    "restaurant:view",
    "menu:create",
    "menu:update",
    "menu:delete",
    "menu:view",
    "order:create",
    "order:update",
    "order:view",
    "order:cancel",
    "order:confirm",
    "order:reject",
    "order:prepare",
    "order:pickup",
    "order:deliver",
    "delivery:accept",
    "delivery:update",
    "delivery:view",
    "user:view",
    "user:update",
]


ROLE_PERMISSIONS = {
    "App Admin": PERMISSIONS,
    "Customer": [
        "restaurant:view",
        "menu:view",
        "order:create",
        "order:view",
        "order:cancel",
    ],
    "Restaurant Owner": [
        "restaurant:create",
        "restaurant:update",
        "restaurant:view",
        "menu:create",
        "menu:update",
        "menu:delete",
        "menu:view",
        "order:view",
        "order:confirm",
        "order:reject",
        "order:prepare",
        "order:pickup",
    ],
    "Delivery Partner": [
        "delivery:accept",
        "delivery:update",
        "delivery:view",
        "order:view",
        "order:deliver",
    ],
}


ADMIN_EMAIL = "ard@gmail.com"


def create_roles(db):
    roles = {}

    for role_name in ROLES:
        role = db.query(Role).filter(Role.name == role_name).first()

        if not role:
            role = Role(
                name=role_name,
            )

            db.add(role)
            db.flush()

            print(f"Created role: {role_name}")

        roles[role_name] = role

    return roles


def create_permissions(db):
    permissions = {}

    for permission_name in PERMISSIONS:
        permission = (
            db.query(Permission).filter(Permission.name == permission_name).first()
        )

        if not permission:
            permission = Permission(
                name=permission_name,
            )

            db.add(permission)
            db.flush()

            print(f"Created permission: {permission_name}")

        permissions[permission_name] = permission

    return permissions


def assign_role_permissions(
    db,
    roles,
    permissions,
):
    for role_name, permission_names in ROLE_PERMISSIONS.items():
        role = roles[role_name]

        for permission_name in permission_names:
            permission = permissions[permission_name]

            exists = (
                db.query(RolePermission)
                .filter(
                    RolePermission.role_id == role.id,
                    RolePermission.permission_id == permission.id,
                )
                .first()
            )

            if exists:
                continue

            db.add(
                RolePermission(
                    role_id=role.id,
                    permission_id=permission.id,
                )
            )

            print(f"Assigned {permission_name} -> {role_name}")


def assign_admin_role(
    db,
    roles,
):
    user = db.query(User).filter(User.email == ADMIN_EMAIL).first()

    if not user:
        raise ValueError(f"User not found: {ADMIN_EMAIL}")

    admin_role = roles["App Admin"]

    exists = (
        db.query(UserRole)
        .filter(
            UserRole.user_id == user.id,
            UserRole.role_id == admin_role.id,
        )
        .first()
    )

    if exists:
        print("Admin role already assigned")
        return

    db.add(
        UserRole(
            user_id=user.id,
            role_id=admin_role.id,
        )
    )

    print(f"Assigned App Admin role to {ADMIN_EMAIL}")


def main():
    db = SessionLocal()

    try:
        roles = create_roles(db)

        permissions = create_permissions(db)

        assign_role_permissions(
            db,
            roles,
            permissions,
        )

        assign_admin_role(
            db,
            roles,
        )

        db.commit()

        print("\nRBAC seeding completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
