from datetime import date

from dateutil import parser


def time_from_index(time):
    # suppose all restaurants start working at 10 am
    t_end = str((time % 2) * 30)
    if time == 23:
        print(f'{10 + time // 2}:{t_end.zfill(2)}')
    return f'{10 + time // 2}:{t_end.zfill(2)}'


def parse_or_return(dirty_date):
    if type(dirty_date) == date:
        return dirty_date
    return parser.parse(dirty_date)


def check_if_can_book(table, date_reserve, time_start, time_end):
    booked_times = list(table.reservation_set \
                        .filter(dt_reservation=date_reserve) \
                        .values_list('time_start', 'time_end'))
    if len(booked_times) == 0:
        return True

    times = [i for i in range(25)]

    for (t_start, t_end) in booked_times:
        for busy_time in range(t_start, t_end):
            try:
                times.remove(busy_time)
            except ValueError:
                return False

    try:
        index_t_start = times.index(time_start)
        index_t_end = times.index(time_end)
    except ValueError:
        return False

    return index_t_end - index_t_start == time_end - time_start
