from datetime import datetime, timezone
import json
import sqlite3
import sys
from typing import Iterator

import ballchasing


if len(sys.argv) == 1:
    print("Usage:")
    print("python main.py [api key] [group id] [optional db file name]")
    sys.exit()


api = ballchasing.Api(sys.argv[1])

db_name = "ballchasing.db"
if len(sys.argv) > 3:
    db_name = sys.argv[3]
db = sqlite3.connect(db_name)


def setup_db(db: sqlite3.Connection):
    with open("sql/setup.sql") as f:
        create_sql = f.read()

    db.executescript(create_sql)
    db.commit()


def _get_team_names(replay: dict) -> dict[str, str]:
    names = {"blue": "blue", "orange": "orange"}
    if "name" in replay["blue"]:
        names["blue"] = replay["blue"]["name"]

    if "name" in replay["orange"]:
        names["orange"] = replay["orange"]["name"]

    return names


def write_replay_to_db(db: sqlite3.Connection, replay: dict):
    team_names = _get_team_names(replay)

    winner = team_names["orange"]
    if (
        replay["blue"]["stats"]["core"]["goals"]
        > replay["orange"]["stats"]["core"]["goals"]
    ):
        winner = team_names["blue"]

    date = replay["date"]
    if replay["date_has_timezone"]:
        # convert to UTC
        date_parsed = datetime.strptime(
            replay["date"], "%Y-%m-%dT%H:%M:%S%z"
        ).astimezone(timezone.utc)
        date = date_parsed.strftime("%Y-%m-%dT%H:%M:%SZ")

    db.execute(
        """
        insert into replays (replay_id, replay_name, replay_date, overtime, duration, map_code, map_name, winner)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT DO NOTHING;
    """,
        (
            replay["id"],
            replay["title"],
            date,
            int(replay["overtime"]),
            replay["duration"],
            replay["map_code"],
            replay["map_name"],
            winner,
        ),
    )
    db.commit()

    _write_team_stats_to_db(db, replay, team_names)


def _insert_player_stat(
    db: sqlite3.Connection, replay_id: str, team_name: str, team_color: str, p: dict
):
    # skip any player who accidentally joined a game
    if p["stats"]["core"]["score"] == 0:
        return

    # this is not included in the payload if it is 0
    goals_against_while_last_defender = 0
    if "goals_against_while_last_defender" in p["stats"]["positioning"]:
        goals_against_while_last_defender = p["stats"]["positioning"][
            "goals_against_while_last_defender"
        ]

    db.execute(
        """
        insert into player_stats (player_name, team_name, team_color, replay_id, shots, shots_against, goals, goals_against, saves, assists, score, mvp, shooting_percentage, bpm, bcpm, avg_amount, amount_collected, amount_stolen, amount_collected_big, amount_stolen_big, amount_collected_small, amount_stolen_small, count_collected_big, count_stolen_big, count_collected_small, count_stolen_small, amount_overfill, amount_overfill_stolen, amount_used_while_supersonic, time_zero_boost, percent_zero_boost, time_full_boost, percent_full_boost, time_boost_0_25, time_boost_25_50, time_boost_50_75, time_boost_75_100, percent_boost_0_25, percent_boost_25_50, percent_boost_50_75, percent_boost_75_100, avg_speed, total_distance, time_supersonic_speed, time_boost_speed, time_slow_speed, time_ground, time_low_air, time_high_air, time_powerslide, count_powerslide, avg_powerslide_duration, avg_speed_percentage, percent_slow_speed, percent_boost_speed, percent_supersonic_speed, percent_ground, percent_low_air, percent_high_air, avg_distance_to_ball, avg_distance_to_ball_possession, avg_distance_to_ball_no_possession, avg_distance_to_mates, time_defensive_third, time_neutral_third, time_offensive_third, time_defensive_half, time_offensive_half, time_behind_ball, time_infront_ball, time_most_back, time_most_forward, goals_against_while_last_defender, time_closest_to_ball, time_farthest_from_ball, percent_defensive_third, percent_offensive_third, percent_neutral_third, percent_defensive_half, percent_offensive_half, percent_behind_ball, percent_infront_ball, percent_most_back, percent_most_forward, percent_closest_to_ball, percent_farthest_from_ball, demos_inflicted, demos_taken)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT DO NOTHING;
    """,
        (
            p["name"],
            team_name,
            team_color,
            replay_id,
            # core
            p["stats"]["core"]["shots"],
            p["stats"]["core"]["shots_against"],
            p["stats"]["core"]["goals"],
            p["stats"]["core"]["goals_against"],
            p["stats"]["core"]["saves"],
            p["stats"]["core"]["assists"],
            p["stats"]["core"]["score"],
            int(p["stats"]["core"]["mvp"]),
            p["stats"]["core"]["shooting_percentage"],
            # boost
            p["stats"]["boost"]["bpm"],
            p["stats"]["boost"]["bcpm"],
            p["stats"]["boost"]["avg_amount"],
            p["stats"]["boost"]["amount_collected"],
            p["stats"]["boost"]["amount_stolen"],
            p["stats"]["boost"]["amount_collected_big"],
            p["stats"]["boost"]["amount_stolen_big"],
            p["stats"]["boost"]["amount_collected_small"],
            p["stats"]["boost"]["amount_stolen_small"],
            p["stats"]["boost"]["count_collected_big"],
            p["stats"]["boost"]["count_stolen_big"],
            p["stats"]["boost"]["count_collected_small"],
            p["stats"]["boost"]["count_stolen_small"],
            p["stats"]["boost"]["amount_overfill"],
            p["stats"]["boost"]["amount_overfill_stolen"],
            p["stats"]["boost"]["amount_used_while_supersonic"],
            p["stats"]["boost"]["time_zero_boost"],
            p["stats"]["boost"]["percent_zero_boost"],
            p["stats"]["boost"]["time_full_boost"],
            p["stats"]["boost"]["percent_full_boost"],
            p["stats"]["boost"]["time_boost_0_25"],
            p["stats"]["boost"]["time_boost_25_50"],
            p["stats"]["boost"]["time_boost_50_75"],
            p["stats"]["boost"]["time_boost_75_100"],
            p["stats"]["boost"]["percent_boost_0_25"],
            p["stats"]["boost"]["percent_boost_25_50"],
            p["stats"]["boost"]["percent_boost_50_75"],
            p["stats"]["boost"]["percent_boost_75_100"],
            # movement
            p["stats"]["movement"]["avg_speed"],
            p["stats"]["movement"]["total_distance"],
            p["stats"]["movement"]["time_supersonic_speed"],
            p["stats"]["movement"]["time_boost_speed"],
            p["stats"]["movement"]["time_slow_speed"],
            p["stats"]["movement"]["time_ground"],
            p["stats"]["movement"]["time_low_air"],
            p["stats"]["movement"]["time_high_air"],
            p["stats"]["movement"]["time_powerslide"],
            p["stats"]["movement"]["count_powerslide"],
            p["stats"]["movement"]["avg_powerslide_duration"],
            p["stats"]["movement"]["avg_speed_percentage"],
            p["stats"]["movement"]["percent_slow_speed"],
            p["stats"]["movement"]["percent_boost_speed"],
            p["stats"]["movement"]["percent_supersonic_speed"],
            p["stats"]["movement"]["percent_ground"],
            p["stats"]["movement"]["percent_low_air"],
            p["stats"]["movement"]["percent_high_air"],
            # positioning
            p["stats"]["positioning"]["avg_distance_to_ball"],
            p["stats"]["positioning"]["avg_distance_to_ball_possession"],
            p["stats"]["positioning"]["avg_distance_to_ball_no_possession"],
            p["stats"]["positioning"]["avg_distance_to_mates"],
            p["stats"]["positioning"]["time_defensive_third"],
            p["stats"]["positioning"]["time_neutral_third"],
            p["stats"]["positioning"]["time_offensive_third"],
            p["stats"]["positioning"]["time_defensive_half"],
            p["stats"]["positioning"]["time_offensive_half"],
            p["stats"]["positioning"]["time_behind_ball"],
            p["stats"]["positioning"]["time_infront_ball"],
            p["stats"]["positioning"]["time_most_back"],
            p["stats"]["positioning"]["time_most_forward"],
            goals_against_while_last_defender,
            p["stats"]["positioning"]["time_closest_to_ball"],
            p["stats"]["positioning"]["time_farthest_from_ball"],
            p["stats"]["positioning"]["percent_defensive_third"],
            p["stats"]["positioning"]["percent_offensive_third"],
            p["stats"]["positioning"]["percent_neutral_third"],
            p["stats"]["positioning"]["percent_defensive_half"],
            p["stats"]["positioning"]["percent_offensive_half"],
            p["stats"]["positioning"]["percent_behind_ball"],
            p["stats"]["positioning"]["percent_infront_ball"],
            p["stats"]["positioning"]["percent_most_back"],
            p["stats"]["positioning"]["percent_most_forward"],
            p["stats"]["positioning"]["percent_closest_to_ball"],
            p["stats"]["positioning"]["percent_farthest_from_ball"],
            # demos
            p["stats"]["demo"]["inflicted"],
            p["stats"]["demo"]["taken"],
        ),
    )
    db.commit()


def _insert_team_stat(db: sqlite3.Connection, replay_id: str, team_name: str, t: dict):
    db.execute(
        """
        insert into team_stats (team_name, team_color, replay_id, possession_time, time_in_side, shots, shots_against, goals, goals_against, saves, assists, score, shooting_percentage, bpm, bcpm, avg_amount, amount_collected, amount_stolen, amount_collected_big, amount_stolen_big, amount_collected_small, amount_stolen_small, count_collected_big, count_stolen_big, count_collected_small, count_stolen_small, amount_overfill, amount_overfill_stolen, amount_used_while_supersonic, time_zero_boost, time_full_boost, time_boost_0_25, time_boost_25_50, time_boost_50_75, time_boost_75_100, total_distance, time_supersonic_speed, time_boost_speed, time_slow_speed, time_ground, time_low_air, time_high_air, time_powerslide, count_powerslide, time_defensive_third, time_neutral_third, time_offensive_third, time_defensive_half, time_offensive_half, time_behind_ball, time_infront_ball, demos_inflicted, demos_taken)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT DO NOTHING;
    """,
        (
            team_name,
            t["color"],
            replay_id,
            # ball
            t["stats"]["ball"]["possession_time"],
            t["stats"]["ball"]["time_in_side"],
            # core
            t["stats"]["core"]["shots"],
            t["stats"]["core"]["shots_against"],
            t["stats"]["core"]["goals"],
            t["stats"]["core"]["goals_against"],
            t["stats"]["core"]["saves"],
            t["stats"]["core"]["assists"],
            t["stats"]["core"]["score"],
            t["stats"]["core"]["shooting_percentage"],
            # boost
            t["stats"]["boost"]["bpm"],
            t["stats"]["boost"]["bcpm"],
            t["stats"]["boost"]["avg_amount"],
            t["stats"]["boost"]["amount_collected"],
            t["stats"]["boost"]["amount_stolen"],
            t["stats"]["boost"]["amount_collected_big"],
            t["stats"]["boost"]["amount_stolen_big"],
            t["stats"]["boost"]["amount_collected_small"],
            t["stats"]["boost"]["amount_stolen_small"],
            t["stats"]["boost"]["count_collected_big"],
            t["stats"]["boost"]["count_stolen_big"],
            t["stats"]["boost"]["count_collected_small"],
            t["stats"]["boost"]["count_stolen_small"],
            t["stats"]["boost"]["amount_overfill"],
            t["stats"]["boost"]["amount_overfill_stolen"],
            t["stats"]["boost"]["amount_used_while_supersonic"],
            t["stats"]["boost"]["time_zero_boost"],
            t["stats"]["boost"]["time_full_boost"],
            t["stats"]["boost"]["time_boost_0_25"],
            t["stats"]["boost"]["time_boost_25_50"],
            t["stats"]["boost"]["time_boost_50_75"],
            t["stats"]["boost"]["time_boost_75_100"],
            # movement
            t["stats"]["movement"]["total_distance"],
            t["stats"]["movement"]["time_supersonic_speed"],
            t["stats"]["movement"]["time_boost_speed"],
            t["stats"]["movement"]["time_slow_speed"],
            t["stats"]["movement"]["time_ground"],
            t["stats"]["movement"]["time_low_air"],
            t["stats"]["movement"]["time_high_air"],
            t["stats"]["movement"]["time_powerslide"],
            t["stats"]["movement"]["count_powerslide"],
            # positioning
            t["stats"]["positioning"]["time_defensive_third"],
            t["stats"]["positioning"]["time_neutral_third"],
            t["stats"]["positioning"]["time_offensive_third"],
            t["stats"]["positioning"]["time_defensive_half"],
            t["stats"]["positioning"]["time_offensive_half"],
            t["stats"]["positioning"]["time_behind_ball"],
            t["stats"]["positioning"]["time_infront_ball"],
            # demos
            t["stats"]["demo"]["inflicted"],
            t["stats"]["demo"]["taken"],
        ),
    )
    db.commit()


def _write_team_stats_to_db(db: sqlite3.Connection, replay: dict, team_names: dict):
    for team_color in ["blue", "orange"]:
        _insert_team_stat(
            db,
            replay["id"],
            team_names[team_color],
            replay[team_color],
        )

        for p in replay[team_color]["players"]:
            _insert_player_stat(
                db, replay["id"], team_names[team_color], team_color, p
            )


def get_group_replays(
    api: ballchasing.Api, group_id: str, deep: bool = False
) -> Iterator[dict]:
    """
    Fix for the built in ballchasing func. The one in the library doesn't pass deep
        down recursively.

    Finds all replays in a group, including child groups.
    :param group_id: the base group id.
    :param deep: whether or not to get full stats for each replay (will be much slower).
    :return: an iterator over all the replays in the group.
    """
    child_groups = api.get_groups(group=group_id)
    for child in child_groups:
        for replay in get_group_replays(api, child["id"], deep=deep):
            yield replay
    for replay in api.get_replays(group_id=group_id, deep=deep):
        yield replay


if __name__ == "__main__":
    setup_db(db)

    replays = get_group_replays(api, sys.argv[2], deep=True)

    for replay in replays:
        try:
            write_replay_to_db(db, replay)
        except Exception as e:
            print(json.dumps(replay))
            raise e
