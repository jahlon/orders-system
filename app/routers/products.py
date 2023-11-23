from fastapi import APIRouter

router = APIRouter(
    prefix='/products',
    tags=['products'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/')
async def get_products():
    return {'products': []}


@router.get('/{product_sku}')
async def get_product(product_sku: str):
    return {'product': product_sku}


@router.post('/')
async def create_product():
    return {'product': 'created'}


@router.put('/{product_sku}')
async def update_product(product_sku: str):
    return {'product': product_sku}