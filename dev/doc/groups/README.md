Groups

group
    id --> long
    name --> string(20) (20 hex characters randomly generated)
    event_id --> long

event
    id --> long
    name --> string(128) (2014 Golden Globes)

category
    remove point_value
    add event_id

categories_events
    id --> long
    category_id --> long
    event_id --> long

categories_groups
    id --> long
    category_id --> long
    group_id --> long
    point_value --> long
