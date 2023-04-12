pubsub_trigger = {
    "Pubsub trigger": [
        {"name": "topic", "type": "str"},
        {"name": "filter", "type": "str"},
    ]
}
clock_event = {"Clock event trigger": [{"name": "cron", "type": "str"}]}

mongo_bike_target_generator = {
    "Mongo bike target generator": [
        {"name": "dataset", "type": "str"},
        {"name": "query", "type": "str"},
        {"name": "include_areas", "type": "str"},  # TODO : List str
        {"name": "use_default_infield_filter", "type": "bool"},
        {"name": "use_default_recently_connected_filter", "type": "bool"},
    ]
}
mongo_trip_target_generator = {
    "Mongo trip target generator": [
        {"name": "query", "type": "str"},
        {"name": "include_areas", "type": "str"},  # TODO : List str
    ]
}
bigquery_bike_target_generator = {
    "Bigquery bike target generator": [
        {"name": "query", "type": "str"},
    ]
}

pubsub_user_target_generator = {
    "Pubsub user target generator": [{"name": "body_key", "type": "str"}]
}

pubsub_trip_target_generator = {
    "Pubsub trip target generator": [
        {
            "name": "body_key",
            "type": "str",
        }
    ]
}
pubsub_gcs_file_target_generator = {"Pubsub gcs file target generator": []}
pubsub_discount_target_generator = {
    "Pubsub discount target generator": [
        {
            "name": "user_id_key",
            "type": "str",
        },
        {
            "name": "pricing_id_key",
            "type": "str",
        },
    ]
}
pubsub_contract_target_generator = {
    "Pubsub contract target generator": [
        {
            "name": "body_key",
            "type": "str",
        }
    ]
}

trip_to_user_converter = {"Trip to user converter": []}
discount_to_user_converter = {"Discount to user converter": []}

bike_filter_last_n_bad_trip = {
    "Bike filter last n bad trips": [
        {"name": "nb_trips", "type": "int"},
        {"name": "query", "type": "str"},
    ]
}
bike_filter_volumetry_check = {
    "Bike filter volumetry check": [
        {"name": "dataset", "type": "str"},
        {"name": "max_ratio", "type": "int"},
        {"name": "query", "type": "str"},
        {"name": "include_areas", "type": "str"},  # TODO : List str
        {"name": "use_default_infield_filter", "type": "bool"},
        {"name": "use_default_recently_connected_filter", "type": "bool"},
    ]
}
bike_filter_current_battery = {
    "Bike filter current battery": [
        {"name": "min_battery", "type": "int"},
        {"name": "max_battery", "type": "int"},
        {"name": "previous_max_battery", "type": "int"},
        {"name": "previous_min_battery", "type": "int"},
        {"name": "include_temporal_decay", "type": "bool"},
    ]
}
bike_filter_current_state = {
    "Bike filter current state": [
        {"name": "dataset", "type": "str"},
        {"name": "query", "type": "str"},
        {"name": "include_areas", "type": "str"},
        {"name": "use_default_infield_filter", "type": "int"},
        {"name": "use_default_recently_connected_filter", "type": "bool"},
    ]
}
bike_filter_last_n_trips = {
    "Bike filter last n trips": [
        {"name": "nb_trips", "type": "int"},
        {"name": "only_distinct_users", "type": "str"},
        {"name": "last_trips_query", "type": "str"},
        {"name": "filtered_trips_query", "type": "str"},
    ]
}
trip_filter = {
    "Trip filter": [{"name": "is_maintenance_gratification", "type": "bool"}]
}
user_filter = {
    "User filter": [
        {"name": "max_gratification_points", "type": "int"},
        {"name": "min_gratification_points", "type": "int"},
        {"name": "include_scopes", "type": "str"},  # TODO: list str
        {"name": "include_areas", "type": "str"},
        {"name": "include_user_roles", "type": "str"},
        {"name": "exclude_user_roles", "type": "str"},
        {"name": "newsletter_opt_in", "type": "bool"},
    ]
}
discount_filter = {
    "Discount filter": [
        {"name": "pricing_id", "type": "str"},
        {"name": "current_status", "type": "int"},
        {"name": "previous_status", "type": "int"},
    ]
}
leasing_contract_filter = {
    "Leasing contract filter": [
        {"name": "current_status", "type": "int"},
        {"name": "previous_status", "type": "int"},
    ]
}
bike_last_contact_filter = {
    "Bike last contact filter": [{"name": "min_last_contact", "type": "int"}]
}
bike_gcp_filter = {
    "Bike gcp filter": [
        {"name": "query", "type": "str"},
        {"name": "mileage", "type": "int"},
    ]
}

backend_bike_action_generator = {
    "Backend bike action generator": [
        {
            "name": "target_maintenance_state",
            "type": "str",
        },
        {
            "name": "target_out_of_order",
            "type": "bool",
        },
        {
            "name": "enable_state_improvement",
            "type": "bool",
        },
        {
            "name": "disabler__time_after_ras",
            "type": "int",
        },
        {
            "name": "disabler__nb_trips_since_last_issue",
            "type": "int",
        },
        {
            "name": "create_issue",
            "type": "bool",
        },
        {
            "name": "issue_label",
            "type": "str",
        },
        {
            "name": "issue_locale",
            "type": "str",
        },
        {
            "name": "issue_type",
            "type": "str",
        },
        {
            "name": "issue_level",
            "type": "str",
        },
    ]
}
trip_traces_generator = {"Trip traces generator": []}
processed_gcs_traces_generator = {"Processed GCS traces generator": []}
email_action_generator = {
    "Email action generator": [
        {
            "name": "template_name",
            "type": "str",
        },
        {
            "name": "sender_email",
            "type": "str",
        },
        {
            "name": "email_subject",
            "type": "str",
        },
        {"name": "locale", "type": "str"},
        {
            "name": "version",
            "type": "str",
        },
    ]
}
slack_action_generator = {
    "Slack action generator": [
        {
            "name": "message_body",
            "type": "str",
        },
        {
            "name": "channel_id",
            "type": "str",
        },
        {
            "name": "as_user",
            "type": bool,
        },
    ]
}
user_metadata_action_generator = {"User metadata action generator": []}
user_discount_action_generator = {"User discount action generator": []}
bike_metadata_generator = {"Bike metadata generator": []}
contract_metadata_generator = {"Contract metadata generator": []}

backend_actioner = {"Backend actioner": []}
email_actioner = {"Email actioner": []}
slack_actioner = {"Slack actioner": []}

TRIGGERS = [pubsub_trigger, clock_event]
TARGET_GENERATORS = [
    mongo_bike_target_generator,
    mongo_trip_target_generator,
    bigquery_bike_target_generator,
    pubsub_user_target_generator,
    pubsub_trip_target_generator,
    pubsub_gcs_file_target_generator,
    pubsub_discount_target_generator,
    pubsub_contract_target_generator,
]
CONVERTERS = [trip_to_user_converter, discount_to_user_converter]
TARGET_FILTERS = [
    bike_filter_last_n_bad_trip,
    bike_filter_volumetry_check,
    bike_filter_current_battery,
    bike_filter_current_state,
    bike_filter_last_n_trips,
    trip_filter,
    user_filter,
    discount_filter,
    leasing_contract_filter,
    bike_last_contact_filter,
    bike_gcp_filter,
]
DATA_GENERATORS = [
    backend_bike_action_generator,
    trip_traces_generator,
    processed_gcs_traces_generator,
    email_action_generator,
    slack_action_generator,
    user_metadata_action_generator,
    user_discount_action_generator,
    bike_metadata_generator,
    contract_metadata_generator,
]

ACTIONERS = [backend_actioner, email_actioner, slack_actioner]
