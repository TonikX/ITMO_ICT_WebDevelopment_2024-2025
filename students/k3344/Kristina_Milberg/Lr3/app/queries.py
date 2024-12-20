def get_user_month_transaction_sum(user: int, month: int) -> str:
    if month not in range(1, 13):
        raise ValueError("Invalid month")
    return f"""
select total_owe, sum(amount) as total_paid
from app_order

    left join (select app_order.id, sum(price_per_unit * quantity) as total_owe
    from app_order
    left join main.app_batchproduct ab on app_order.id = ab.batch_id
    where app_order.broker_id = '{user}'
    group by app_order.id)
    left join (select *
    from app_transaction
    where strftime('%m'
    , date) = {month}) at
on app_order.id = at.order_id
"""