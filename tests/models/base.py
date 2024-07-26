from pydantic import BaseModel, ConfigDict


class CheckboxBaseModel(BaseModel):
    """
    A base model for Checkbox SDK models.

    This class serves as the base model for all models in the Checkbox SDK. It defines the model configuration with options to coerce numbers to strings in server responses.

    In server responses, all fields containing only numbers are returned without quotes.
    """

    model_config = ConfigDict(coerce_numbers_to_str=True)
