

from code1.test1 import *
from model.test1 import *
from fastapi import *


router = APIRouter(prefix="/summoner")

@router.get(

    path='/tier',
    response_model=TierListInfo
)
def summoner_tier(
        riot_id:str,
        tag:str
) -> TierListInfo:
    return test(riot_id,tag)

@router.get(

    path='/tiercheck',
    response_model=tiercheck
)
def tier_check(
        tier:str,
        division:str
) -> tiercheck:
    return check(tier,division)



