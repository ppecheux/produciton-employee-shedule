CREATE TABLE IF NOT EXISTS activity
    (product varchar(80),
    activity_block_name varchar(80),
    activity_block_duration INTEGER,
    station_nb INTEGER,
    max_sequence_rank varchar(20),
    min_sequence_rank varchar(20),
    PRIMARY KEY(product, activity_block_name)
    );