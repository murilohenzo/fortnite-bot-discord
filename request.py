import json
import re
import requests
from humanize_datetime import Humanize

class FortniteClient(object):

    api_url = 'https://api.fortnitetracker.com/v1/profile/'
    api_token = 'c5e177c2-1263-4286-9e69-e738e98870ba'

    headers = {'Content-Type': 'application/json',
               'TRN-Api-Key': api_token
               }

    @staticmethod
    def response(platform, epic_name):
        platform = platform.lower()
        api_url = f'{FortniteClient.api_url}{platform}/{epic_name}'
        response = requests.get(api_url, headers=FortniteClient.headers)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return json.loads(response.content.decode('utf-8'))

    @staticmethod
    def get_account_info(platform, epic_name):
        data = FortniteClient.response(platform, epic_name)
        if len(data.keys()) == 1:
            return data
        elif len(data.keys()) > 1:
            stats = data['stats']
            account_status = {
                "epicName": data["epicUserHandle"],
                "platformNameLong": data["platformNameLong"],
                "status": {
                    "Matches Played": data['lifeTimeStats'][7]['value'],
                    "Wins":  data['lifeTimeStats'][8]['value'],
                    "Win%":  data['lifeTimeStats'][9]['value'],
                    "Kills": data['lifeTimeStats'][10]['value'],
                    "k/d": data['lifeTimeStats'][11]['value'],
                    "Score" :data['lifeTimeStats'][6]['value'],
                    "status by mode": [
                        {"solo": {
                            "kills": stats["p2"]["kills"]["value"],
                            "matches": stats["p2"]["matches"]["value"],
                            "k/d": stats["p2"]['kd']["value"],
                            "kills/Macth": stats["p2"]["kpg"]["value"],
                            "minutesPlayed": stats["p2"]["minutesPlayed"]["displayValue"],
                            "score": stats["p2"]["score"]["displayValue"],
                            "scorePerMatch": stats["p2"]["scorePerMatch"]["value"],
                            "wins": stats["p2"]["top1"]["value"],
                            "top5": stats["p2"]["top5"]["value"],
                            "top12": stats["p2"]["top12"]["value"]
                        },
                            "duo": {
                                "kills": stats["p10"]["kills"]["value"],
                                "matches": stats["p10"]["matches"]["value"],
                                "k/d": stats["p10"]['kd']["value"],
                                "kills/Macth": stats["p10"]["kpg"]["value"],
                                "minutesPlayed": stats["p10"]["minutesPlayed"]["displayValue"],
                                "score": stats["p10"]["score"]["displayValue"],
                                "scorePerMatch": stats["p10"]["scorePerMatch"]["value"],
                                "wins": stats["p10"]["top1"]["value"],
                                "top5": stats["p10"]["top5"]["value"],
                                "top12": stats["p10"]["top12"]["value"]
                            },
                            "squad": {
                                "kills": stats["p9"]["kills"]["value"],
                                "matches": stats["p9"]["matches"]["value"],
                                "k/d": stats["p9"]['kd']["value"],
                                "kills/Macth": stats["p9"]["kpg"]["value"],
                                "minutesPlayed": stats["p9"]["minutesPlayed"]["displayValue"],
                                "score": stats["p9"]["score"]["displayValue"],
                                "scorePerMatch": stats["p9"]["scorePerMatch"]["value"],
                                "wins": stats["p9"]["top1"]["value"],
                                "top5": stats["p9"]["top5"]["value"],
                                "top12": stats["p9"]["top12"]["value"]
                            }}
                    ]}
            }
            return account_status

    @staticmethod
    def recentmatches(platform, epic_name):
        data = FortniteClient.response(platform, epic_name)
        if len(data.keys()) == 1:
            return data
        elif len(data.keys()) > 1:
            rctm = []
            for idx in range(len(data['recentMatches'])):
                datetime_re = re.findall('(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})',
                                         data['recentMatches'][idx]['dateCollected'])
                data['recentMatches'][idx]['dateCollected'] = Humanize.trasnform(datetime_re[0])
                if data['recentMatches'][idx]['playlist'] == 'p2':
                    data['recentMatches'][idx]['playlist'] = 'solo'
                elif data['recentMatches'][idx]['playlist'] == 'p10':
                    data['recentMatches'][idx]['playlist'] = 'duo'
                elif data['recentMatches'][idx]['playlist'] == 'p9':
                    data['recentMatches'][idx]['playlist'] = 'squad'
                rctm.append(data['recentMatches'][idx])
            recentmatches = {
                "epicName": data["epicUserHandle"],
                "platformNameLong": data["platformNameLong"],
                "recentMatches": rctm
            }
            return recentmatches

