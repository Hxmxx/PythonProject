def get_people():
    people = []
    print("입력을 종료하려면 빈 줄(Enter) 입력")

    while True:
        line = input("이름과 출생년도 입력 (예: 하민 08년생): ")
        if line.strip() == "":
            break

        try:
            name, year = line.split()
            year = year.replace("샌", "생")  # 오타 처리
            if not year.endswith("년생"):
                print("⚠️ '년생'으로 끝나지 않아요. 다시 입력해주세요.")
                continue

            year_num = int(year[:2])  # 예: '05년생' → 05
            # 2000년대 기준으로 해석
            full_year = 2000 + year_num if year_num <= 25 else 1900 + year_num

            people.append((name, full_year))

        except ValueError:
            print("⚠️ 올바른 형식이 아닙니다. 다시 입력해주세요.")

    return people

def main():
    people = get_people()
    people.sort(key=lambda x: x[1])  # 출생년도 기준 정렬

    print("\n📋 정렬된 명단:")
    for name, year in people:
        print(f"{name} - {year}년생")

main()