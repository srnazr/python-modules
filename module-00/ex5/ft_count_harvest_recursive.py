def ft_recursive_days(days: int, counter: int) -> None:
    if counter >= days:
        print("Harvest time!")
        return
    print("Day", counter + 1)
    ft_recursive_days(days, counter + 1)


def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))
    ft_recursive_days(days, 0)
