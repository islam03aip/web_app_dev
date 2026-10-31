from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from django.db import connection, transaction

from hunting.models import HuntLog, WantedCriminal

CRIMINALS = [
    # name, nickname, reward, lat, lon, note, difficulty, armed, crew, escape
    ("", "Red Comet", 25000, 34.0522, -118.2437, "Last seen near a Los Angeles spaceport.", 8, True, True, True),
    ("Jet Marlowe", "Jet Black", 12000, 51.5074, -0.1278, "Docked at a London orbital yard.", 5, True, False, False),
    ("Faye Valentine", "Lucky Faye", 3000, None, None, "Rumored to be gambling on Ganymede.", 3, False, False, True),
    ("", "The Ghost", 60000, 35.6762, 139.6503, "Vanished in Neo-Tokyo's lower levels.", 10, True, True, True),
    ("Ed Wong", "Radical Ed", 500, 43.2389, 76.8897, "Hacking from an Almaty cafe.", 2, False, False, False),
    ("Vicious Hale", "Vicious", 45000, 48.8566, 2.3522, "Spotted near Paris syndicate HQ.", 9, True, True, False),
]

HUNTS = [  # (criminal index 1-based, success, notes)
    (1, False, "Target escaped through an asteroid field."),
    (1, False, "Ambushed by crew; retreated."),
    (1, True, "Captured at the refuelling station."),
    (2, False, "Lost the trail in the Thames docks."),
    (2, True, "Cornered in a cargo bay."),
    (3, False, "Fled through a casino back exit."),
    (4, False, "Vanished before the stakeout began."),
    (4, False, "Decoy ship led us into a trap."),
    (5, True, "Found by tracing his IP. Surrendered immediately."),
    (6, False, "Heavily armed escort; aborted."),
    (6, False, "Missed him by minutes in Paris."),
    (3, True, "Caught after she ran out of chips."),
]


class Command(BaseCommand):
    help = "Reset and prefill the database with 6 criminals and 12 hunt logs."

    @transaction.atomic
    def handle(self, *args, **options):
        tables = [HuntLog._meta.db_table, WantedCriminal._meta.db_table]
        sql = connection.ops.sql_flush(no_style(), tables, reset_sequences=True)
        connection.ops.execute_sql_flush(sql)  # ids restart at 1

        created = [WantedCriminal.objects.create(
            name=n, nickname=nick, reward=r, latitude=lat, longitude=lon,
            last_known_note=note, difficulty=d, armed=a, has_crew=c, escape_master=e)
            for n, nick, r, lat, lon, note, d, a, c, e in CRIMINALS]
        for idx, success, notes in HUNTS:
            HuntLog.objects.create(criminal=created[idx - 1], success=success, notes=notes)
        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(CRIMINALS)} criminals and {len(HUNTS)} hunt logs."))
