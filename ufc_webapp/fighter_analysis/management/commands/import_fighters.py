import pymongo
from datetime import datetime
from django.core.management.base import BaseCommand
from fighter_analysis.models import Fighter

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "ufc_analysis"
MONGO_COLLECTION = "fighters"

class Command(BaseCommand):
    help = "Imports fighters from MongoDB to django "

    def handle(self, *args, **options):
        client = pymongo.MongoClient(MONGO_URI)
        ufc_db = client[MONGO_DB]
        fighters = ufc_db[MONGO_COLLECTION]

        for fighter in fighters.find():
            try:
                slpm_float = float(fighter.get("SLpM", "0"))
                sapm_float = float(fighter.get("SApM", "0"))
                td_avg_float = float(fighter.get("TD_avg", "0"))
                sub_avg_float = float(fighter.get("sub_avg", "0"))
                ss_acc_int = int(fighter.get("SS_acc", "0%").strip("%"))
                ss_def_int = int(fighter.get("SS_def", "0%").strip("%"))
                td_acc_int = int(fighter.get("TD_acc", "0%").strip("%"))
                td_def_int = int(fighter.get("TD_def", "0%").strip("%"))

                dob_dt = None
                dob = fighter.get("dob")
                if dob:
                    try:
                        dob_dt = datetime.strptime(dob.strip(),"%b %d, %Y").date()
                    except ValueError:
                        dob_dt = None
            except (ValueError, TypeError) as e:
                self.stdout.write(f"Error parsing {fighter['name']}: {e}")
                continue

            Fighter.objects.update_or_create(
                name=fighter.get('name'),
                defaults={
                    'nickname': fighter.get('nickname'),
                    'dob': dob_dt,
                    'height': fighter.get('height'),
                    'weight': fighter.get('weight'),
                    'reach': fighter.get('reach'),
                    'stance': fighter.get('stance'),
                    'wins': fighter.get('wins', 0),
                    'losses': fighter.get('losses', 0),
                    'draws': fighter.get('draws', 0),
                    'record': fighter.get('record'),
                    'slpm': slpm_float,
                    'sapm': sapm_float,
                    'ss_acc': ss_acc_int,
                    'ss_def': ss_def_int,
                    'td_avg': td_avg_float,
                    'td_acc': td_acc_int,
                    'td_def': td_def_int,
                    'sub_avg': sub_avg_float,
                }
            )
        self.stdout.write(self.style.SUCCESS("Successfully imported fighters"))



