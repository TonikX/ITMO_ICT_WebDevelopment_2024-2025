SELECT_PROFIT_PER_ROOM_FOR_QUARTER = """
    SELECT 
        room_id,
        label,
        SUM(
            EXTRACT(
                DAY
                FROM (
                    LEAST(
                        b.check_out_date,
                        %(quarter_end)s::date + INTERVAL '1 DAY'
                    ) -
                    GREATEST(
                        b.check_in_date,
                         %(quarter_start)s
                    )
                )
            ) * rt.price_per_day
        ) AS profit
    FROM booking AS b
        JOIN room AS r ON b.room_id = r.id
        JOIN room_type AS rt ON r.room_type_id = rt.id
    WHERE b.check_out_date > %(quarter_start)s AND b.check_in_date <= %(quarter_end)s
    GROUP BY room_id, label;
"""
