import sqlite3
import matplotlib
import matplotlib.pyplot as plt


db = sqlite3.connect('season11_master.db')


def plot_win_percentage_vs_shooting_percentage(db: sqlite3.Connection):
    shooting_percentage = list(range(0, 2500, 10))
    win_percentage = []

    for x in shooting_percentage:
        cur = db.cursor()

        cur.execute(f"""
            SELECT CAST(wins AS FLOAT) / (wins + losses)
                FROM (
                    SELECT t.team_name as name,
                    sum(case when r.winner = t.team_name Then 1 else 0 end) as wins,
                    sum(case when r.winner != t.team_name Then 1 else 0 end) as losses
                    FROM team_stats as t
                    INNER JOIN replays as r ON t.replay_id = r.replay_id
                    WHERE t.amount_used_while_supersonic > {x}
                );
        """)

        win_percentage.append(cur.fetchone()[0])

        cur.close()

    plt.plot(shooting_percentage, win_percentage)
    plt.show()


matplotlib.use('TkAgg')
plot_win_percentage_vs_shooting_percentage(db)
