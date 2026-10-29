from plots2 import show_histogram_and_polygon
import stat_calc2 as sc2

# Вхідні дані Варіанта № 12
intervals = [
    (40, 42), (42, 44), (44, 46), (46, 48),
    (48, 50), (50, 52), (52, 54), (54, 56)
]
n_vals = [4, 9, 13, 24, 27, 16, 3, 3]


def main():
    print("ЛАБОРАТОРНА РОБОТА № 2")
    
    # 1. Перевірка умови суми та середини інтервалів
    n = sum(n_vals)
    print(f"1. Обсяг вибірки n = {n}")
    x_vals = [(a + b) / 2 for a, b in intervals]
    print(f"   Дискретний ряд x_i: {x_vals}")

    # 2. Розрахункова таблиця
    calc_df, summary = sc2.build_calc_table(intervals, x_vals, n_vals)
    print("\n2. Розрахункова таблиця (Таблиця 1.2):")
    print(calc_df.to_string(index=False))
    print(f"Контрольні суми: sum(n_i) = {summary['n']}, sum(n_i*x_i) = {summary['sum_nx']:.4f}, sum_quad = {summary['sum_quad']:.4f}")

    # 3. Точкові оцінки
    pe = sc2.calc_point_estimates(summary)
    print("\n3. Точкові оцінки параметрів розподілу:")
    print(f"   Вибіркове середнє x_bar = {pe['x_bar']:.4f} мА")
    print(f"   Вибіркова дисперсія d_bar = {pe['d_bar']:.4f} мА^2")
    print(f"   Виправлена дисперсія s^2 = {pe['s2']:.4f} мА^2")
    print(f"   Виправлене сер. квадр. відхилення s = {pe['s']:.4f} мА")

    # 4-6. Довірчі інтервали для gamma = 0.95
    ci_95 = sc2.calc_confidence_intervals(pe, n=n, gamma=0.95)
    print(f"\n4. Довірчий інтервал для m (gamma = 0.95, t = {ci_95['t_gamma']}):")
    print(f"   Стандартна похибка s/sqrt(n) = {ci_95['se']:.4f}")
    print(f"   Точність оцінки delta = {ci_95['delta']:.4f} мА")
    print(f"   Інтервал: {ci_95['m_interval'][0]:.4f} < m < {ci_95['m_interval'][1]:.4f} мА")
    print(f"   Відносна точність eps = {ci_95['eps']:.2f}%")

    print(f"\n5. Довірчий інтервал для дисперсії sigma^2 (chi1 = {ci_95['chi1']}, chi2 = {ci_95['chi2']}):")
    print(f"   Інтервал: {ci_95['sigma2_interval'][0]:.4f} < sigma^2 < {ci_95['sigma2_interval'][1]:.4f}")
    print(f"   Для sigma: {ci_95['sigma_interval'][0]:.4f} < sigma < {ci_95['sigma_interval'][1]:.4f} мА")

    left_arm = pe['s2'] - ci_95['sigma2_interval'][0]
    right_arm = ci_95['sigma2_interval'][1] - pe['s2']
    print(f"   Асиметрія інтервалу sigma^2: ліве плече = {left_arm:.4f}, праве плече = {right_arm:.4f} (праве довше у {right_arm / left_arm:.2f} разів)")

    print(f"\n6. Нормальне наближення (z = {ci_95['z_gamma']}):")
    print(f"   delta_z = {ci_95['delta_z']:.4f} мА, розбіжність з t-розподілом = {ci_95['diff_normal_pct']:.2f}%")

    # 7. Дослідження впливу надійності gamma = 0.90, 0.95, 0.99
    gamma_df = sc2.build_gamma_comparison_table(pe, n=n)
    print("\n7. Вплив надійності gamma на довірчі інтервали (Таблиця 1.3):")
    print(gamma_df.to_string(index=False))

    # 8. Необхідний обсяг вибірки для подвоєння точності
    n_new = 4 * n
    print(f"\n8. Необхідний обсяг вибірки для зменшення похибки delta вдвічі: n' = 4 * {n} = {n_new}")

    # Побудова графіка
    show_histogram_and_polygon(intervals, x_vals, n_vals, pe['x_bar'])


if __name__ == "__main__":
    main()