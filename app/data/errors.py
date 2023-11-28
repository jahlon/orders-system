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


class CouldNotDeleteFileError(OrdersSystemError):
    pass


class OrderNotFoundError(OrdersSystemError):
    pass


class UserNotFoundError(OrdersSystemError):
    pass


class IncorrectPasswordError(OrdersSystemError):
    pass
