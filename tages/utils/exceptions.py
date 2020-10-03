from django.core.exceptions import ValidationError
from django.forms.fields import Field


class FieldRequiredError(ValidationError):
    """An error while validating data."""
    def __init__(self, params=None):
        code = 'required'
        message = Field.default_error_messages[code]
        super(FieldRequiredError, self).__init__(
            message, code=code, params=params)
