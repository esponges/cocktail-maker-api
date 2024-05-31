from sqlalchemy import Column, Unicode, BigInteger, Boolean

from core.db import Base
from core.db.mixins import TimestampMixin

class Cocktail(Base, TimestampMixin):
  __tablename__ = "cocktails"

  id = Column(BigInteger, primary_key=True)
  name = Column(Unicode(255), nullable=False)
  recipe = Column(Unicode(255), nullable=True)
  is_alcoholic = Column(Boolean, nullable=False)
  # sqlite doesn't support arrays so we use a string and parse it when needed
  mixers = Column(Unicode(255), nullable=True)
  size = Column(Unicode(255), nullable=True)
  cost = Column(Unicode(255), nullable=True)
  complexity = Column(Unicode(255), nullable=True)
  required_ingredients = Column(Unicode(255), nullable=True)
  required_tools = Column(Unicode(255), nullable=True)
