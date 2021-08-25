from collections import namedtuple
from datetime import datetime, timedelta

stage = namedtuple(
    "stage",
    [
        "interval",
        "name",
    ],
)

normal_timings = [
    stage(timedelta(minutes=20), "Initial 1"),
    stage(timedelta(minutes=45), "Initial 2"),
    stage(timedelta(hours=2), "Initial 3"),
    stage(timedelta(hours=4), "Apprentice 1"),
    stage(timedelta(hours=8), "Apprentice 2"),
    stage(timedelta(days=1), "Apprentice 3"),
    stage(timedelta(days=2), "Apprentice 4"),
    stage(timedelta(weeks=1), "Guru 1"),
    stage(timedelta(weeks=2), "Guru 2"),
    stage(timedelta(weeks=4), "Master"),
    stage(timedelta(weeks=8), "Enlightened"),
]

accelerated_timings = [
    stage(timedelta(minutes=10), "Initial 1(accelerated)"),
    stage(timedelta(minutes=30), "Initial 2 (accelerated)"),
    stage(timedelta(hours=1), "Initial 3 (accelerated)"),
    stage(timedelta(hours=2), "Apprentice 1 (accelerated)"),
    stage(timedelta(hours=4), "Apprentice 2 (accelerated)"),
    stage(timedelta(hours=8), "Apprentice 3 (accelerated)"),
    stage(timedelta(days=1), "Apprentice 4 (accelerated)"),
    stage(timedelta(days=3), "Guru 1 (accelerated)"),
    stage(timedelta(weeks=1), "Guru 2 (accelerated)"),
    stage(timedelta(weeks=2), "Master (accelerated)"),
    stage(timedelta(weeks=4), "Enlightened (accelerated)"),
]


def correct_answer(current_stage, accelerated):
    new_stage = current_stage
    if current_stage < (len(accelerated_timings) - 1):
        new_stage += 1

    interval = (
        accelerated_timings[new_stage].interval
        if accelerated
        else normal_timings[new_stage].interval
    )

    return new_stage, datetime.now() + interval


def incorrect_answer(current_stage, incorrect_answers_before_correct, accelerated):
    srs_penalty_factor = 2 if (current_stage > 6) else 1
    new_stage = current_stage - (
        incorrect_answers_before_correct // 2 * srs_penalty_factor
    )
    new_stage = max(new_stage, 0)

    interval = (
        accelerated_timings[new_stage].interval
        if accelerated
        else normal_timings[new_stage].interval
    )

    return new_stage, datetime.now() + interval
