import matplotlib.pyplot as plt


def show_histogram_and_polygon(intervals, x_vals, n_vals, x_bar, param_name="струм спрацювання реле, мА"):
    """
    Будує гістограму та полігон частот.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    # Межі інтервалів
    bin_edges = [inter[0] for inter in intervals] + [intervals[-1][1]]
    widths = [inter[1] - inter[0] for inter in intervals]
    lefts = [inter[0] for inter in intervals]

    # Гістограма
    ax.bar(
        lefts,
        n_vals,
        width=widths,
        align='edge',
        color="#9ecae1",
        edgecolor='black',
        alpha=0.75,
        label='Гістограма частот'
    )

    # Полігон частот
    ax.plot(
        x_vals,
        n_vals,
        marker='o',
        color='#cb181d',
        linewidth=2,
        label='Полігон частот'
    )

    # Підписи значень частот над точками
    for x, n in zip(x_vals, n_vals):
        ax.annotate(
            str(n),
            xy=(x, n),
            xytext=(0, 5),
            textcoords='offset points',
            ha='center',
            fontsize=10
        )

    # Вертикальна лінія вибіркового середнього
    ax.axvline(
        x_bar,
        color='black',
        linestyle='--',
        linewidth=1.5,
        label=f'Вибіркове середнє = {x_bar:.4f}'
    )

    ax.set_title(f'Гістограма та полігон частот (n = 99)', fontsize=12)
    ax.set_xlabel(param_name, fontsize=11)
    ax.set_ylabel('Частота $n_i$', fontsize=11)
    ax.set_xticks(bin_edges)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

    plt.tight_layout()
    plt.show()