class CustomeScraperException(BaseException):
    """
    # Base Exception class created for all Scraper Exception
    """
    def __str__(self):
        return f"Exception Occurred: : [{self.error_code}], {self.message}"

class UnsupportedSiteException(CustomeScraperException):
    """
    # Exception class for unsupported sites
    """
    error_code = 520
    def __init__(self, message: str = "Unsupported Website for scraping"): 
        self.message = message
        self.error_code = self.__class__.error_code


class NextPageNotFoundException(CustomeScraperException):
    """
    # Exception class for Next PageNotFound
    """
    error_code = 521
    def __init__(self, message: str = "Next Page not found"):
        self.message = message
        self.error_code = self.__class__.error_code


class InfoNotFound(CustomeScraperException):
    """
    # Exception for Info not created
    """
    error_code = 522

    def __init__(self, message: str = "Information Not found"):
        self.message = message
        self.error_code = self.__class__.error_code


class LoginCredsMissing(CustomeScraperException):
    """
    # Exception class created for LoginCredsMissing
    """
    error_code = 523
    def __init__(self, message: str = "login creds are missing"):
        self.message = message
        self.error_code = self.__class__.error_code

class EncryptionError(CustomeScraperException):
    error_code = 524
    def __init__(self, message: str = "Error generating Key"):
        self.message = message
        self.error_code = self.__class__.error_code