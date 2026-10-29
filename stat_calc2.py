import numpy as np
import pandas as pd

# Табличні критичні значення для n=99, k=98 (Додаток А методички)
CRITICAL_VALUES = {
    0.90: {
        't': 1.6606,
        'z': 1.6449,
        'chi1': 122.108,
        'chi2': 76.164
    },
    0.95: {
        't': 1.9845,
        'z': 1.9600,
        'chi1': 127.282,
        'chi2': 72.501
    },
    0.99: {
        't': 2.6269,
        'z': 2.5758,
        'chi1': 137.803,
        'chi2': 65.694
    }
}


def build_calc_table(intervals, x_vals, n_vals):
    """
    Складає розрахункову таблицю 1.2 відповідно до методички:
    i, інтервал, x_i, n_i, n_i * x_i, (x_i - x_bar), n_i * (x_i - x_bar)^2
    """
    n_total = sum(n_vals)
    prod_nx = [n * x for n, x in zip(n_vals, x_vals)]
    sum_prod_nx = sum(prod_nx)
    x_bar = sum_prod_nx / n_total

    diff_x = [round(x - x_bar, 4) for x in x_vals]
    quad_dev = [round(n * ((x - x_bar) ** 2), 4) for n, x in zip(n_vals, x_vals)]
    sum_quad = sum(quad_dev)

    df = pd.DataFrame({
        'i': list(range(1, len(x_vals) + 1)),
        'Інтервал': [f"{a}-{b}" for a, b in intervals],
        'x_i': x_vals,
        'n_i': n_vals,
        'n_i * x_i': prod_nx,
        'x_i - x_bar': diff_x,
        'n_i*(x_i - x_bar)^2': quad_dev
    })

    summary = {
        'n': n_total,
        'sum_nx': sum_prod_nx,
        'sum_quad': sum_quad,
        'x_bar': x_bar
    }
    return df, summary


def calc_point_estimates(summary):
    """Обчислює точкові оцінки: x_bar, d_bar, s^2, s."""
    n = summary['n']
    x_bar = summary['x_bar']
    d_bar = summary['sum_quad'] / n
    s2 = summary['sum_quad'] / (n - 1)
    s = np.sqrt(s2)
    return {
        'x_bar': x_bar,
        'd_bar': d_bar,
        's2': s2,
        's': s
    }


def calc_confidence_intervals(point_est, n=99, gamma=0.95):
    """Розраховує довірчі інтервали для m, sigma^2 та sigma."""
    crit = CRITICAL_VALUES[gamma]
    t_gamma = crit['t']
    chi1 = crit['chi1']
    chi2 = crit['chi2']
    z_gamma = crit['z']

    x_bar = point_est['x_bar']
    s = point_est['s']
    s2 = point_est['s2']

    # Похибка середнього
    se = s / np.sqrt(n)
    delta = t_gamma * se
    m_min = x_bar - delta
    m_max = x_bar + delta

    # Інтервал для дисперсії (чисельник = (n-1)*s^2 = sum_quad)
    numerator = (n - 1) * s2
    sigma2_min = numerator / chi1
    sigma2_max = numerator / chi2

    # Інтервал для середньоквадратичного відхилення
    sigma_min = np.sqrt(sigma2_min)
    sigma_max = np.sqrt(sigma2_max)

    # Відносна точність
    eps = (delta / x_bar) * 100

    # Нормальне наближення
    delta_z = z_gamma * se

    return {
        'gamma': gamma,
        't_gamma': t_gamma,
        'z_gamma': z_gamma,
        'se': se,
        'delta': delta,
        'm_interval': (m_min, m_max),
        'chi1': chi1,
        'chi2': chi2,
        'sigma2_interval': (sigma2_min, sigma2_max),
        'sigma_interval': (sigma_min, sigma_max),
        'eps': eps,
        'delta_z': delta_z,
        'diff_normal_pct': abs(delta - delta_z) / delta * 100
    }


def build_gamma_comparison_table(point_est, n=99):
    """Дослідження впливу надійності gamma = 0.90, 0.95, 0.99 (Таблиця 1.3)."""
    rows = []
    for g in [0.90, 0.95, 0.99]:
        res = calc_confidence_intervals(point_est, n=n, gamma=g)
        m_str = f"({res['m_interval'][0]:.4f}; {res['m_interval'][1]:.4f})"
        s2_str = f"({res['sigma2_interval'][0]:.4f}; {res['sigma2_interval'][1]:.4f})"
        rows.append({
            'gamma': g,
            't_gamma': res['t_gamma'],
            'delta': round(res['delta'], 4),
            'Довірчий інтервал для m': m_str,
            'Довірчий інтервал для sigma^2': s2_str
        })
    return pd.DataFrame(rows)