budget = 200_000
size_counts = {
    "XL": 11,
    "2XL": 1,
    "3XL": 1,
    "5XL": 2,
    "6XL": 1
}
unit_prices = {
    "XL": 18300,
    "2XL": 19900,
    "3XL": 22800,
    "5XL": 24900,
    "6XL": 24900
}

sorted_sizes = sorted(unit_prices.items(), key=lambda x: -x[1])

allocation = {}
remaining_budget = budget

for size, price in sorted_sizes:
    total_count = size_counts.get(size, 0)
    covered = 0
    while covered < total_count and remaining_budget >= price:
        covered += 1
        remaining_budget -= price
    allocation[size] = {
        "unit_price": price,
        "total": total_count,
        "covered": covered,
        "personal": total_count - covered,
        "covered_cost": covered * price
    }

for size in allocation:
    info = allocation[size]
    print(f"{size}: 총 {info['total']}벌, 예산 지원 {info['covered']}벌, 사비 구매 {info['personal']}벌, 예산 사용 {info['covered_cost']}원")

print(f"\n총 예산 사용: {budget - remaining_budget}원")
print(f"남은 예산: {remaining_budget}원")