from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from foodflow.application.cart.schemas import (
    AddToCartRequest,
    CartResponse,
)
from foodflow.application.cart.service import (
    CartService,
)
from foodflow.infrastructure.database.session import (
    get_db,
)
from foodflow.infrastructure.repositories.cart_repository import (
    CartRepository,
)
from foodflow.infrastructure.repositories.menu_repository import (
    MenuRepository,
)
from foodflow.application.auth.dependencies import (
    get_current_user,
)
from foodflow.domain.models.user import User

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.post(
    "/items",
    status_code=status.HTTP_201_CREATED,
)
def add_to_cart(
    request: AddToCartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    cart_repository = CartRepository(db)

    menu_repository = MenuRepository(db)

    service = CartService(
        cart_repository,
        menu_repository,
    )

    try:
        service.add_to_cart(
            current_user.id,
            request,
        )

        return {"message": "Item added to cart"}

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.get(
    "",
    response_model=CartResponse,
)
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    cart_repository = CartRepository(db)

    menu_repository = MenuRepository(db)

    service = CartService(
        cart_repository,
        menu_repository,
    )

    try:
        return service.get_cart(
            current_user.id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )
