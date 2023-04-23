import collections
import itertools
import main
import copy
import networkx as nx
import random

from networkx import bipartite
from networkx.algorithms.bipartite import sets as bipartite_sets

roleStaffData = {
    "roles": [
        {
            "name": "lunch",
            "callTime": "10:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "MONDAY"
        },
        {
            "name": "lunch",
            "callTime": "10:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "MONDAY"
        },
        {
            "name": "lunch",
            "callTime": "10:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "TUESDAY"
        },
        {
            "name": "lunch",
            "callTime": "10:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "TUESDAY"
        },
        {
            "name": "lunch",
            "callTime": "10:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "WEDNESDAY"
        },
        {
            "name": "lunch",
            "callTime": "10:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "WEDNESDAY"
        },
        {
            "name": "lunch",
            "callTime": "10:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "THURSDAY"
        },
        {
            "name": "lunch",
            "callTime": "10:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "THURSDAY"
        },
        {
            "name": "lunch",
            "callTime": "10:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "FRIDAY"
        },
        {
            "name": "lunch",
            "callTime": "10:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "FRIDAY"
        },
        {
            "name": "brunch",
            "callTime": "10:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "brunch",
            "callTime": "10:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "brunch",
            "callTime": "10:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "brunch",
            "callTime": "10:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "brunch",
            "callTime": "10:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SUNDAY"
        },
        {
            "name": "brunch",
            "callTime": "10:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SUNDAY"
        },
        {
            "name": "brunch",
            "callTime": "10:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SUNDAY"
        },
        {
            "name": "brunchdoor",
            "callTime": "12:00",
            "qualifiedStaff": [
                "Glenn",
                "Rose",
                "Fernanda",
                "Mia"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "brunchdoor",
            "callTime": "12:00",
            "qualifiedStaff": [
                "Glenn",
                "Rose",
                "Fernanda",
                "Mia"
            ],
            "preferredStaff": [],
            "day": "SUNDAY"
        },
        {
            "name": "swing",
            "callTime": "13:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SUNDAY"
        },
        {
            "name": "shermans",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "MONDAY"
        },
        {
            "name": "shermans",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "TUESDAY"
        },
        {
            "name": "shermans",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "THURSDAY"
        },
        {
            "name": "shermans",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "FRIDAY"
        },
        {
            "name": "shermans",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "shermans",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "shermans",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SUNDAY"
        },
        {
            "name": "veranda",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "MONDAY"
        },
        {
            "name": "veranda",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "TUESDAY"
        },
        {
            "name": "veranda",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "WEDNESDAY"
        },
        {
            "name": "veranda",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "THURSDAY"
        },
        {
            "name": "veranda",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "FRIDAY"
        },
        {
            "name": "veranda",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "veranda",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SUNDAY"
        },
        {
            "name": "outside",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "MONDAY"
        },
        {
            "name": "outside",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "TUESDAY"
        },
        {
            "name": "outside",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "WEDNESDAY"
        },
        {
            "name": "outside",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "THURSDAY"
        },
        {
            "name": "outside",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "FRIDAY"
        },
        {
            "name": "outside",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "outside",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SUNDAY"
        },
        {
            "name": "bbar",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "MONDAY"
        },
        {
            "name": "bbar",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "TUESDAY"
        },
        {
            "name": "bbar",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "WEDNESDAY"
        },
        {
            "name": "bbar",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "THURSDAY"
        },
        {
            "name": "bbar",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "FRIDAY"
        },
        {
            "name": "bbar",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "bbar",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SUNDAY"
        },
        {
            "name": "vbar",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "MONDAY"
        },
        {
            "name": "vbar",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "TUESDAY"
        },
        {
            "name": "vbar",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "WEDNESDAY"
        },
        {
            "name": "vbar",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "THURSDAY"
        },
        {
            "name": "vbar",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "FRIDAY"
        },
        {
            "name": "vbar",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "vbar",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SUNDAY"
        },
        {
            "name": "front",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "MONDAY"
        },
        {
            "name": "front",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "TUESDAY"
        },
        {
            "name": "front",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "WEDNESDAY"
        },
        {
            "name": "front",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "THURSDAY"
        },
        {
            "name": "front",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "FRIDAY"
        },
        {
            "name": "front",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "front",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SUNDAY"
        },
        {
            "name": "uber",
            "callTime": "16:30",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [
                "Carlito"
            ],
            "day": "THURSDAY"
        },
        {
            "name": "door",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Kiki",
                "Glenn",
                "Rose",
                "Fernanda"
            ],
            "preferredStaff": [],
            "day": "SUNDAY"
        },
        {
            "name": "back",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "MONDAY"
        },
        {
            "name": "back",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "TUESDAY"
        },
        {
            "name": "back",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "WEDNESDAY"
        },
        {
            "name": "back",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "THURSDAY"
        },
        {
            "name": "back",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "FRIDAY"
        },
        {
            "name": "back",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "back",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SUNDAY"
        },
        {
            "name": "middle",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "MONDAY"
        },
        {
            "name": "middle",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "TUESDAY"
        },
        {
            "name": "middle",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "WEDNESDAY"
        },
        {
            "name": "middle",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "THURSDAY"
        },
        {
            "name": "middle",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "FRIDAY"
        },
        {
            "name": "middle",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "middle",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SUNDAY"
        },
        {
            "name": "shermans6pm",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "MONDAY"
        },
        {
            "name": "shermans6pm",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "TUESDAY"
        },
        {
            "name": "shermans6pm",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "WEDNESDAY"
        },
        {
            "name": "shermans6pm",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "THURSDAY"
        },
        {
            "name": "shermans6pm",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "FRIDAY"
        },
        {
            "name": "shermans6pm",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "FRIDAY"
        },
        {
            "name": "shermans6pm",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "shermans6pm",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        },
        {
            "name": "aux",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "THURSDAY"
        },
        {
            "name": "aux",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "FRIDAY"
        },
        {
            "name": "aux",
            "callTime": "18:00",
            "qualifiedStaff": [
                "Mia",
                "Rose",
                "Joshua",
                "Sil",
                "Lucas",
                "Ernesto",
                "Meagan",
                "Miroslava",
                "Emi",
                "Sofia",
                "Sonia",
                "Luca",
                "Annika",
                "Selvi",
                "Matthew",
                "Rosalie",
                "Michael",
                "Alivia",
                "Lily",
                "Madison",
                "Ilton"
            ],
            "preferredStaff": [],
            "day": "SATURDAY"
        }
    ],
    "staff": [
        {
            "name": "Mia",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [],
                "TUESDAY": [],
                "WEDNESDAY": [],
                "THURSDAY": [
                    "4:30 PM",
                    "6:00 PM"
                ],
                "FRIDAY": [
                    "10:00 AM",
                    "10:30 AM"
                ],
                "SATURDAY": [
                    "6:00 PM"
                ],
                "SUNDAY": []
            }
        },
        {
            "name": "Rose",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "TUESDAY": [],
                "WEDNESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "THURSDAY": [],
                "FRIDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ]
            }
        },
        {
            "name": "Joshua",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "TUESDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "WEDNESDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "THURSDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "FRIDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ]
            }
        },
        {
            "name": "Sil",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "4:30 PM",
                    "6:00 PM"
                ],
                "TUESDAY": [
                    "10:00 AM",
                    "10:30 AM"
                ],
                "WEDNESDAY": [
                    "4:30 PM",
                    "6:00 PM"
                ],
                "THURSDAY": [
                    "4:30 PM",
                    "6:00 PM"
                ],
                "FRIDAY": [
                    "4:30 PM",
                    "6:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ]
            }
        },
        {
            "name": "Lucas",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "TUESDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "WEDNESDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "THURSDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "FRIDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ]
            }
        },
        {
            "name": "Ernesto",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [],
                "TUESDAY": [],
                "WEDNESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "THURSDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "FRIDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ]
            }
        },
        {
            "name": "Meagan",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [],
                "TUESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "WEDNESDAY": [],
                "THURSDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "FRIDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ]
            }
        },
        {
            "name": "Miroslava",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [],
                "TUESDAY": [],
                "WEDNESDAY": [],
                "THURSDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "FRIDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ]
            }
        },
        {
            "name": "Emi",
            "maxShifts": 5,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "TUESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "WEDNESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "THURSDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "FRIDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ]
            }
        },
        {
            "name": "Sofia",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "TUESDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "WEDNESDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "THURSDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "FRIDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ]
            }
        },
        {
            "name": "Sonia",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "TUESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "WEDNESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "THURSDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "FRIDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SATURDAY": [],
                "SUNDAY": [
                    "4:30 PM",
                    "6:00 PM"
                ]
            }
        },
        {
            "name": "Luca",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "TUESDAY": [],
                "WEDNESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "THURSDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "FRIDAY": [],
                "SATURDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ]
            }
        },
        {
            "name": "Annika",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "TUESDAY": [],
                "WEDNESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "THURSDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "FRIDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ]
            }
        },
        {
            "name": "Selvi",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "TUESDAY": [
                    "10:00 AM",
                    "10:30 AM"
                ],
                "WEDNESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "THURSDAY": [],
                "FRIDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SATURDAY": [],
                "SUNDAY": [
                    "10:00 AM",
                    "10:30 AM"
                ]
            }
        },
        {
            "name": "Matthew",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "TUESDAY": [],
                "WEDNESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "THURSDAY": [],
                "FRIDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ]
            }
        },
        {
            "name": "Rosalie",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "10:30 AM"
                ],
                "TUESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "WEDNESDAY": [
                    "10:00 AM",
                    "10:30 AM"
                ],
                "THURSDAY": [],
                "FRIDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ]
            }
        },
        {
            "name": "Michael",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "TUESDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "WEDNESDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "THURSDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "FRIDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ]
            }
        },
        {
            "name": "Alivia",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "TUESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "WEDNESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "THURSDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "FRIDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "10:30 AM"
                ]
            }
        },
        {
            "name": "Lily",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "TUESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "WEDNESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "THURSDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "FRIDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SATURDAY": [],
                "SUNDAY": []
            }
        },
        {
            "name": "Madison",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "TUESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "WEDNESDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "THURSDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "FRIDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM",
                    "10:30 AM",
                    "12:00 PM"
                ],
                "SUNDAY": []
            }
        },
        {
            "name": "Ilton",
            "maxShifts": 4,
            "rolePreference": [],
            "doubles": None,
            "availability": {
                "MONDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "TUESDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "WEDNESDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "THURSDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "FRIDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "SATURDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ],
                "SUNDAY": [
                    "10:00 AM",
                    "10:30 AM",
                    "12:00 PM",
                    "1:00 PM",
                    "4:30 PM",
                    "6:00 PM"
                ]
            }
        }
    ]
}

INFINITY = float("inf")


def availabilityMatching(G, top_nodes=None):

    """Returns the maximum cardinality matching of the bipartite graph `G`.

    A matching is a set of edges that do not share any nodes. A maximum
    cardinality matching is a matching with the most edges possible. It
    is not always unique. Finding a matching in a bipartite graph can be
    treated as a networkx flow problem.

    The functions ``hopcroft_karp_matching`` and ``maximum_matching``
    are aliases of the same function.

    Parameters
    ----------
    G : NetworkX graph

      Undirected bipartite graph

    top_nodes : container of nodes

      Container with all nodes in one bipartite node set. If not supplied
      it will be computed. But if more than one solution exists an exception
      will be raised.

    Returns
    -------
    matches : dictionary

      The matching is returned as a dictionary, `matches`, such that
      ``matches[v] == w`` if node `v` is matched to node `w`. Unmatched
      nodes do not occur as a key in `matches`.

    Raises
    ------
    AmbiguousSolution
      Raised if the input bipartite graph is disconnected and no container
      with all nodes in one bipartite set is provided. When determining
      the nodes in each bipartite set more than one valid solution is
      possible if the input graph is disconnected.

    Notes
    -----
    This function is implemented with the `Hopcroft--Karp matching algorithm
    <https://en.wikipedia.org/wiki/Hopcroft%E2%80%93Karp_algorithm>`_ for
    bipartite graphs.

    See :mod:`bipartite documentation <networkx.algorithms.bipartite>`
    for further details on how bipartite graphs are handled in NetworkX.

    See Also
    --------
    maximum_matching
    hopcroft_karp_matching
    eppstein_matching

    References
    ----------
    .. [1] John E. Hopcroft and Richard M. Karp. "An n^{5 / 2} Algorithm for
       Maximum Matchings in Bipartite Graphs" In: **SIAM Journal of Computing**
       2.4 (1973), pp. 225--231. <https://doi.org/10.1137/0202019>.

    """

    # First we define some auxiliary search functions.
    #
    # If you are a human reading these auxiliary search functions, the "global"
    # variables `leftmatches`, `rightmatches`, `distances`, etc. are defined
    # below the functions, so that they are initialized close to the initial
    # invocation of the search functions.
    def breadth_first_search():
        for v in left:
            if leftmatches[v] is None:
                distances[v] = 0
                queue.append(v)
            else:
                distances[v] = INFINITY
        distances[None] = INFINITY
        while queue:
            v = queue.popleft()
            if distances[v] < distances[None]:
                for u in G[v]:
                    if distances[rightmatches[u]] is INFINITY:
                        distances[rightmatches[u]] = distances[v] + 1
                        queue.append(rightmatches[u])
        return distances[None] is not INFINITY

    def depth_first_search(v):
        if v is not None:
            for u in G[v]:
                if distances[rightmatches[u]] == distances[v] + 1:
                    if depth_first_search(rightmatches[u]):
                        rightmatches[u] = v
                        leftmatches[v] = u
                        return True
            distances[v] = INFINITY
            return None
        return True

    # Initialize the "global" variables that maintain state during the search.
    left, right = bipartite_sets(G, top_nodes)
    leftmatches = {v: None for v in left}
    rightmatches = {v: None for v in right}
    distances = {}
    queue = collections.deque()

    # Implementation note: this counter is incremented as pairs are matched but
    # it is currently not used elsewhere in the computation.
    num_matched_pairs = 0
    while breadth_first_search():
        for v in left:
            if leftmatches[v] is None:
                if depth_first_search(v):
                    num_matched_pairs += 1

    return rightmatches

def numberOfDaysCouldWork(staff):
    days = 0
    for times in staff.availability.values():
        if times != []:
            days += 1
    if days == 0:
        #don't want someone with no availability to work
        days = -10
    return days


roleCollection = [main.parseRole(role) for role in roleStaffData["roles"]]
staffCollection = [main.parseStaff(staff) for staff in roleStaffData["staff"]]


staffByShifts = {}
for staff in staffCollection:
    #makes sure shifts remaining aligns with a staff's indicated availability
    shiftsRemaining = min(staff.maxShifts, numberOfDaysCouldWork(staff))
    staffByShifts.setdefault(shiftsRemaining, [])
    staffByShifts[shiftsRemaining].append(staff)
maxRemainingShift = max(staffByShifts)

staffNodes = []
for role in roleCollection:
    staff = random.choice(staffByShifts[maxRemainingShift])
    #move staff to lower key, possibly remove key and update max
    #if that was the last staff with that number of shifts remaining
    staffByShifts[maxRemainingShift].remove(staff)
    staffByShifts.setdefault(maxRemainingShift-1, [])
    staffByShifts[maxRemainingShift-1].append(staff)
    if staffByShifts[maxRemainingShift] == []:
        del staffByShifts[maxRemainingShift]
        maxRemainingShift -= 1
    staffNodes.append(copy.deepcopy(staff))


Bgraph = nx.Graph()
Bgraph.add_nodes_from(staffNodes, bipartite=0)
Bgraph.add_nodes_from(roleCollection, bipartite=1)

roleStaffConnections_Availablity = []
for staff in staffNodes:
    for role in roleCollection:
        if staff.isAvailableFor_CallTime(role):
            roleStaffConnections_Availablity.append((role, staff))
Bgraph.add_edges_from(roleStaffConnections_Availablity)

top_nodes = {n for n, d in Bgraph.nodes(data=True) if d["bipartite"] == 0}


availabilityMatching(Bgraph)

