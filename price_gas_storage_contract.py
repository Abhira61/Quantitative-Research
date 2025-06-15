
def price_contract(injections,
                    withdrawals, 
                    prices, max_in,
                    max_out,
                    capacity,
                    cost_per_day):
    from datetime import datetime

    def get_date(d):
        return datetime.strptime(d, "%Y-%m-%d")

    dates = sorted(set([d for d, _ in injections + withdrawals]))
    gas = 0
    total = 0
    last_day = None

    for day in dates:
        if last_day:
            days_between = (get_date(day) - get_date(last_day)).days
            total -= gas * cost_per_day * days_between
        last_day = day

        price = prices.get(day)
        if not price:
            continue

        inject = sum(v for d, v in injections if d == day)
        takeout = sum(v for d, v in withdrawals if d == day)

        if inject > max_in:
            inject = max_in
        gas += inject
        total -= inject * price

        if takeout > max_out:
            takeout = max_out
        if takeout > gas:
            takeout = gas
        gas -= takeout
        total += takeout * price

        if gas > capacity:
            gas = capacity

    return round(total, 2)



inj = [("2025-07-01", 500), ("2025-07-03", 600)]
wd = [("2025-07-10", 700), ("2025-07-15", 300)]

price_data = {
    "2025-07-01": 8.5,
    "2025-07-03": 9.0,
    "2025-07-10": 11.0,
    "2025-07-15": 12.5
}


result = price_contract(
    injections=inj,
    withdrawals=wd,
    prices=price_data,
    max_in=2000,
    max_out=2000,
    capacity=3000,
    cost_per_day=0.01
)

print("Value:", result)
