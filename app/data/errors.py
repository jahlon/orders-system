class OrdersSystemError(Exception):
    pass


class CouldNotUpdateProductError(OrdersSystemError):
    pass


class ProductAlreadyExistsError(OrdersSystemError):
    pass


class ProductNotFoundError(OrdersSystemError):
    pass


class CouldNotUploadFileError(OrdersSystemError):
    pass
