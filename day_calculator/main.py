from datetime import datetime, timedelta

n = int(input('1: 날짜±n 연산 / 2: D-day 연산: '))

if n == 1:
    기준날짜 = input("기준 날짜를 입력하세요 (예: 2025-04-20): ")
    일수 = int(input("며칠을 더하거나 뺄까요? (예: +5 또는 -10): "))

    # 문자열 → 날짜 형식 변환
    기준날짜_dt = datetime.strptime(기준날짜, "%Y-%m-%d")

    # 날짜 계산
    계산된_날짜 = 기준날짜_dt + timedelta(days=일수)

    # 결과 출력
    print("계산된 날짜:", 계산된_날짜.strftime("%Y-%m-%d"))
elif n == 2:
    # A날 입력
    a날_입력 = input("A 날짜를 입력하세요 (예: 2025-04-20 또는 1(오늘 날짜로 지정됩니다.): ").strip().lower()

    # A날 처리
    if a날_입력 in ['today', '오늘', 'now', '1']:
        a날_dt = datetime.today()
        print(f"A 날짜가 오늘 날짜로 설정되었습니다: {a날_dt.strftime('%Y-%m-%d')}")
    else:
        a날_dt = datetime.strptime(a날_입력, "%Y-%m-%d")

    # B날 입력
    b날_입력 = input("B 날짜를 입력하세요 (예: 2025-04-25): ").strip()
    b날_dt = datetime.strptime(b날_입력, "%Y-%m-%d")

    # 당일 포함 여부
    include_today = input("당일 포함할까요? (1 or y/0 or n): ").strip().lower()

    # 날짜 차이 계산
    delta = abs((b날_dt - a날_dt).days)

    # 당일 포함 처리
    if include_today == '1' or include_today == 'y':
        delta += 1

    # 출력
    print(f"A날과 B날 사이의 차이는 {delta}일입니다.")