class DefaultConfig(object):
    SCHEMA = {
        "roles": [
            {
                "name": str(),
                "callTime": str(),
                "day": str(),
                "qualifiedStaff": [
                    str()
                ]
            }
        ],
        "staff": [
            {
                "name": str(),
                "maxShifts": int(),
                "availability": {
                    "MONDAY": [
                        str()
                    ],
                    "TUESDAY": [
                        str()
                    ],
                    "WEDNESDAY": [
                        str()
                    ],
                    "THURSDAY": [
                        str()
                    ],
                    "FRIDAY": [
                        str()
                    ],
                    "SATURDAY": [
                        str()
                    ],
                    "SUNDAY": [
                        str()
                    ]
                }
            }
        ]
    }