import requests as rs
from model.test1 import *

riot_id = 'Hide on bush'
tag = 'KR1'


def get_tier(queue, tier, division, lp) -> TierInfo:
    return TierInfo(
        queue=queue,
        tier=tier,
        division=division,
        lp=lp
    )


def get_tierdetal(queue, tier, division, lp, summonerName) -> TierInfo:
    return TierInfo(
        queue=queue,
        tier=tier,
        division=division,
        lp=lp,
        summonerName=summonerName
    )


def test(riot_id: str, tag: str) -> TierListInfo:
    api_key = 'RGAPI-e674eb69-7d34-41d9-adfb-e43ad16950ca'
    url = f'https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{riot_id}/{tag}?api_key={api_key}'
    res = rs.get(url).json()
    puu_id = res['puuid']

    # 소환사 ID
    summoner_url = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puu_id}?api_key={api_key}'
    summoner_res = rs.get(summoner_url).json()
    summoner_id = summoner_res['id']

    # 소환사 티어
    league_url = f'https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}'
    league_res = rs.get(league_url).json()

    tier_list = []
    for league in league_res:
        if league['queueType'] == 'RANKED_SOLO_5x5':
            queue = league['queueType']
            solo_rank_tier = league['tier']
            solo_rank_division = league['rank']
            solo_rank_lp = league['leaguePoints']

            tier = get_tier(queue, solo_rank_tier, solo_rank_division, solo_rank_lp)
            tier_list.append(tier)
        elif league['queueType'] == 'RANKED_FLEX_SR':
            queue = league['queueType']
            flex_rank_tier = league['tier']
            flex_rank_division = league['rank']
            flex_rank_lp = league['leaguePoints']

            flex_tier = get_tier(queue, flex_rank_tier, flex_rank_division, flex_rank_lp)
            tier_list.append(flex_tier)

    return TierListInfo(
        total_tier_list=tier_list
    )


def check(tier: str, division: str) -> tiercheck:
    api_key = 'RGAPI-e674eb69-7d34-41d9-adfb-e43ad16950ca'
    url = f'https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{tier}/{division}?page=1&api_key={api_key}'

    tierInfo = rs.get(url).json()

    tdList = []
    for tierInfodetail in tierInfo:
        queueType = tierInfodetail['queueType']
        tier = tierInfodetail['tier']
        rank = tierInfodetail['rank']
        leaguePoints = tierInfodetail['leaguePoints']
        summonerName = tierInfodetail['summonerName']
        tdList.append(get_tierdetal(queueType, tier, rank, leaguePoints, summonerName))
    # print(tdList)
    return tiercheck(
        totalchecklist=tdList
    )
