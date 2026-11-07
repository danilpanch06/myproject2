"""Точка входа: связывает модули и реализует главный цикл программы."""
from menu import show_menu, select_mode, mode_name
from validators import input_mass, input_w1, input_w2, input_temperature
from operations import water_mass, drying_time, drying_class


def main() -> None:
    """Главный сценарий: цикл расчётов до выбора выхода."""
    print("Вариант 10. Время сушки влажного материала.")
    while True:
        show_menu()
        k = select_mode()
        if k is None:
            print("Работа завершена.")
            break

        m = input_mass()
        w1 = input_w1()
        w2 = input_w2(w1)
        temp = input_temperature()

        m_water = water_mass(m, w1, w2)
        tau = drying_time(k, w1, w2)
        cls = drying_class(tau)

        print("\n--- Результаты расчёта ---")
        print(f"Материал: {mode_name(k)} (k = {k} 1/ч)")
        print(f"Масса материала: {m:.2f} кг")
        print(f"Влажность: w1 = {w1:.2f} %, w2 = {w2:.2f} %")
        print(f"Температура сушильного агента: {temp:.2f} °C")
        print(f"Масса удаляемой воды: {m_water:.2f} кг")
        print(f"Время сушки: {tau:.2f} ч")
        print(f"Класс: {cls}")


if __name__ == "__main__":
    main()
