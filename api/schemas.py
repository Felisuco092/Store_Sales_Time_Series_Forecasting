from typing import Annotated
from pydantic import BaseModel, Field
from enum import Enum
from datetime import date

class Family(str, Enum):
    """
    Enum of the valid product families accepted by the prediction API.
    """
    AUTOMOTIVE = "AUTOMOTIVE"
    BABY_CARE = "BABY CARE"
    BEAUTY = "BEAUTY"
    BEVERAGES = "BEVERAGES"
    BOOKS = "BOOKS"
    BREAD_BAKERY = "BREAD/BAKERY"
    CELEBRATION = "CELEBRATION"
    CLEANING = "CLEANING"
    DAIRY = "DAIRY"
    DELI = "DELI"
    EGGS = "EGGS"
    FROZEN_FOODS = "FROZEN FOODS"
    GROCERY_I = "GROCERY I"
    GROCERY_II = "GROCERY II"
    HARDWARE = "HARDWARE"
    HOME_AND_KITCHEN_I = "HOME AND KITCHEN I"
    HOME_AND_KITCHEN_II = "HOME AND KITCHEN II"
    HOME_APPLIANCES = "HOME APPLIANCES"
    HOME_CARE = "HOME CARE"
    LADIESWEAR = "LADIESWEAR"
    LAWN_AND_GARDEN = "LAWN AND GARDEN"
    LINGERIE = "LINGERIE"
    LIQUOR_WINE_BEER = "LIQUOR,WINE,BEER"
    MAGAZINES = "MAGAZINES"
    MEATS = "MEATS"
    PERSONAL_CARE = "PERSONAL CARE"
    PET_SUPPLIES = "PET SUPPLIES"
    PLAYERS_AND_ELECTRONICS = "PLAYERS AND ELECTRONICS"
    POULTRY = "POULTRY"
    PREPARED_FOODS = "PREPARED FOODS"
    PRODUCE = "PRODUCE"
    SCHOOL_AND_OFFICE_SUPPLIES = "SCHOOL AND OFFICE SUPPLIES"
    SEAFOOD = "SEAFOOD"



class Prediction(BaseModel):
    """
    Request payload for a single sales prediction.

    Attributes
    ----------
    id : int or None
        Optional identifier of the prediction. Default is None. Must be
        non-negative.
    date : date
        The date of the prediction.
    store_nbr : int
        The store number, between 1 and 54.
    family : Family
        The product family.
    onpromotion : int
        Number of items on promotion. Must be non-negative.
    """
    id: Annotated[int | None, Field(ge=0)] = None
    date: date
    store_nbr: Annotated[int, Field(ge=1, le=54)]
    family: Family
    onpromotion: Annotated[int, Field(ge=0)]
