class Error(Exception):
    # Exception base class for all custom exceptions
    pass


class InsufficientResourceError(Error):
    
    def __init__(self, transfer_from, transfer_to, res_has, res_req, action):
        self.message = (f"{transfer_from} cannot transfer "
            + f"{res_req} to {transfer_to} doing {action}, "
            + f"has {res_has}")
