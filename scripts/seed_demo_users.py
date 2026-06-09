from foodflow.application.auth.security import hash_password
from foodflow.domain.models.user import User
from foodflow.domain.models.role import Role
from foodflow.domain.models.user_role import UserRole
from foodflow.infrastructure.database.session import SessionLocal


USERS = [
    {
        "full_name": "FoodFlow Admin",
        "email": "admin@foodflow.com",
        "phone": "9000000001",
        "password": "Admin@123",
        "role": "Admin",
    },
    {
        "full_name": "Pizza Owner",
        "email": "owner1@foodflow.com",
        "phone": "9000000002",
        "password": "Owner@123",
        "role": "Restaurant Owner",
    },
    {
        "full_name": "Burger Owner",
        "email": "owner2@foodflow.com",
        "phone": "9000000003",
        "password": "Owner@123",
        "role": "Restaurant Owner",
    },
    {
        "full_name": "Customer One",
        "email": "customer1@foodflow.com",
        "phone": "9000000004",
        "password": "Customer@123",
        "role": "Customer",
    },
    {
        "full_name": "Customer Two",
        "email": "customer2@foodflow.com",
        "phone": "9000000005",
        "password": "Customer@123",
        "role": "Customer",
    },
    {
        "full_name": "Customer Three",
        "email": "customer3@foodflow.com",
        "phone": "9000000006",
        "password": "Customer@123",
        "role": "Customer",
    },
    {
        "full_name": "Delivery Partner One",
        "email": "delivery1@foodflow.com",
        "phone": "9000000007",
        "password": "Delivery@123",
        "role": "Delivery Partner",
    },
    {
        "full_name": "Delivery Partner Two",
        "email": "delivery2@foodflow.com",
        "phone": "9000000008",
        "password": "Delivery@123",
        "role": "Delivery Partner",
    },
]


def main():
    db = SessionLocal()

    try:
        for user_data in USERS:
            existing_user = (
                db.query(User).filter(User.email == user_data["email"]).first()
            )

            if existing_user:
                print(f"User already exists: {user_data['email']}")
                continue

            role = db.query(Role).filter(Role.name == user_data["role"]).first()

            if not role:
                print(f"Role not found: {user_data['role']}")
                continue

            user = User(
                full_name=user_data["full_name"],
                email=user_data["email"],
                phone=user_data["phone"],
                password_hash=hash_password(user_data["password"]),
                is_active=True,
                is_verified=True,
            )

            db.add(user)
            db.flush()

            user_role = UserRole(
                user_id=user.id,
                role_id=role.id,
            )

            db.add(user_role)

            print(f"Created {user.email} -> {role.name}")

        db.commit()

        print("\nDemo users seeded successfully")

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


if __name__ == "__main__":
    main()
