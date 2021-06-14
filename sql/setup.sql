CREATE TABLE IF NOT EXISTS replays (
    replay_id text PRIMARY KEY,
    replay_name text NOT NULL,
    replay_date text NOT NULL,

    overtime integer NOT NULL,
    duration integer NOT NULL,
    map_code text NOT NULL,
    map_name text NOT NULL,
    winner text NOT NULL
);

CREATE TABLE IF NOT EXISTS player_stats (
    player_name text NOT NULL,
    team_name text NOT NULL,
    team_color text NOT NULL,
    replay_id text NOT NULL,

    -- core
    shots integer NOT NULL,
    shots_against integer NOT NULL,
    goals integer NOT NULL,
    goals_against integer NOT NULL,
    saves integer NOT NULL,
    assists integer NOT NULL,
    score integer NOT NULL,
    mvp integer NOT NULL,
    shooting_percentage real NOT NULL,

    -- boost
    bpm real NOT NULL,
    bcpm real NOT NULL,
    avg_amount real NOT NULL,
    amount_collected integer NOT NULL,
    amount_stolen integer NOT NULL,
    amount_collected_big integer NOT NULL,
    amount_stolen_big integer NOT NULL,
    amount_collected_small integer NOT NULL,
    amount_stolen_small integer NOT NULL,
    count_collected_big integer NOT NULL,
    count_stolen_big integer NOT NULL,
    count_collected_small integer NOT NULL,
    count_stolen_small integer NOT NULL,
    amount_overfill integer NOT NULL,
    amount_overfill_stolen integer NOT NULL,
    amount_used_while_supersonic integer NOT NULL,
    time_zero_boost real NOT NULL,
    percent_zero_boost real NOT NULL,
    time_full_boost real NOT NULL,
    percent_full_boost real NOT NULL,
    time_boost_0_25 real NOT NULL,
    time_boost_25_50 real NOT NULL,
    time_boost_50_75 real NOT NULL,
    time_boost_75_100 real NOT NULL,
    percent_boost_0_25 real NOT NULL,
    percent_boost_25_50 real NOT NULL,
    percent_boost_50_75 real NOT NULL,
    percent_boost_75_100 real NOT NULL,

    -- movement
    avg_speed integer NOT NULL,
    total_distance integer NOT NULL,
    time_supersonic_speed real NOT NULL,
    time_boost_speed real NOT NULL,
    time_slow_speed real NOT NULL,
    time_ground real NOT NULL,
    time_low_air real NOT NULL,
    time_high_air real NOT NULL,
    time_powerslide real NOT NULL,
    count_powerslide integer NOT NULL,
    avg_powerslide_duration real NOT NULL,
    avg_speed_percentage real NOT NULL,
    percent_slow_speed real NOT NULL,
    percent_boost_speed real NOT NULL,
    percent_supersonic_speed real NOT NULL,
    percent_ground real NOT NULL,
    percent_low_air real NOT NULL,
    percent_high_air real NOT NULL,

    -- positioning
    avg_distance_to_ball integer NOT NULL,
    avg_distance_to_ball_possession integer NOT NULL,
    avg_distance_to_ball_no_possession integer NOT NULL,
    avg_distance_to_mates integer NOT NULL,
    time_defensive_third real NOT NULL,
    time_neutral_third real NOT NULL,
    time_offensive_third real NOT NULL,
    time_defensive_half real NOT NULL,
    time_offensive_half real NOT NULL,
    time_behind_ball real NOT NULL,
    time_infront_ball real NOT NULL,
    time_most_back real NOT NULL,
    time_most_forward real NOT NULL,
    goals_against_while_last_defender integer NOT NULL,
    time_closest_to_ball real NOT NULL,
    time_farthest_from_ball real NOT NULL,
    percent_defensive_third real NOT NULL,
    percent_offensive_third real NOT NULL,
    percent_neutral_third real NOT NULL,
    percent_defensive_half real NOT NULL,
    percent_offensive_half real NOT NULL,
    percent_behind_ball real NOT NULL,
    percent_infront_ball real NOT NULL,
    percent_most_back real NOT NULL,
    percent_most_forward real NOT NULL,
    percent_closest_to_ball real NOT NULL,
    percent_farthest_from_ball real NOT NULL,

    -- demo
    demos_inflicted integer NOT NULL,
    demos_taken integer NOT NULL,

    PRIMARY KEY (player_name, replay_id),
    FOREIGN KEY (replay_id) REFERENCES replays(replay_id)
        ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS team_stats (
    team_name text NOT NULL,
    team_color text NOT NULL,
    replay_id text NOT NULL,

    --ball
    possession_time real NOT NULL,
    time_in_side real NOT NULL,

    -- core
    shots integer NOT NULL,
    shots_against integer NOT NULL,
    goals integer NOT NULL,
    goals_against integer NOT NULL,
    saves integer NOT NULL,
    assists integer NOT NULL,
    score integer NOT NULL,
    shooting_percentage real NOT NULL,

    -- boost
    bpm real NOT NULL,
    bcpm real NOT NULL,
    avg_amount real NOT NULL,
    amount_collected integer NOT NULL,
    amount_stolen integer NOT NULL,
    amount_collected_big integer NOT NULL,
    amount_stolen_big integer NOT NULL,
    amount_collected_small integer NOT NULL,
    amount_stolen_small integer NOT NULL,
    count_collected_big integer NOT NULL,
    count_stolen_big integer NOT NULL,
    count_collected_small integer NOT NULL,
    count_stolen_small integer NOT NULL,
    amount_overfill integer NOT NULL,
    amount_overfill_stolen integer NOT NULL,
    amount_used_while_supersonic integer NOT NULL,
    time_zero_boost real NOT NULL,
    time_full_boost real NOT NULL,
    time_boost_0_25 real NOT NULL,
    time_boost_25_50 real NOT NULL,
    time_boost_50_75 real NOT NULL,
    time_boost_75_100 real NOT NULL,

    -- movement
    total_distance integer NOT NULL,
    time_supersonic_speed real NOT NULL,
    time_boost_speed real NOT NULL,
    time_slow_speed real NOT NULL,
    time_ground real NOT NULL,
    time_low_air real NOT NULL,
    time_high_air real NOT NULL,
    time_powerslide real NOT NULL,
    count_powerslide integer NOT NULL,

    -- positioning
    time_defensive_third real NOT NULL,
    time_neutral_third real NOT NULL,
    time_offensive_third real NOT NULL,
    time_defensive_half real NOT NULL,
    time_offensive_half real NOT NULL,
    time_behind_ball real NOT NULL,
    time_infront_ball real NOT NULL,

    -- demo
    demos_inflicted integer NOT NULL,
    demos_taken integer NOT NULL,

    PRIMARY KEY (team_name, replay_id),
    FOREIGN KEY (replay_id) REFERENCES replays(replay_id)
        ON DELETE CASCADE ON UPDATE NO ACTION
);
