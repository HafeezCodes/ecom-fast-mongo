from typing import Type, TypeVar, Dict
from pydantic import BaseModel
from mongoengine import Document
import datetime
from bson import ObjectId

# Define type variables
TDocument = TypeVar('TDocument', bound=Document)
TSchema = TypeVar('TSchema', bound=BaseModel)

# general formatting function
def format_mongo_to_pydantic(document: TDocument, schema: Type[TSchema]) -> TSchema:
    """
    Convert a MongoEngine document to a Pydantic model.

    Args:
        document (Document): The MongoEngine document.
        schema (Type[BaseModel]): The Pydantic schema to use for formatting.

    Returns:
        BaseModel: The formatted Pydantic model.
    """
    # Convert MongoEngine fields to Pydantic fields
    document_data: Dict[str, any] = {field: getattr(document, field) for field in schema.__annotations__.keys() if hasattr(document, field)}

    # Format ObjectId fields and datetime fields
    for field in schema.__annotations__.keys():
        if isinstance(document_data.get(field), ObjectId):
            document_data[field] = str(document_data[field])
        elif isinstance(document_data.get(field), datetime.datetime):
            document_data[field] = document_data[field].isoformat()

    return schema(**document_data)


# cart formatting function
def cart_mongo_to_pydantic(document, schema):
    document_data = {
        'id': str(document.id),
        'user_id': str(document.user_id.id),
        'product_id': str(document.product_id.id),
        'quantity': document.quantity,
        'createdAt': document.createdAt.isoformat(),
        'updatedAt': document.updatedAt.isoformat()
    }
    return schema(**document_data)





