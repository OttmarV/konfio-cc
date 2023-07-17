from matplotlib import pyplot as plt


def plot_moving_average(df):
    print("Plotting dataframe")

    plt.style.use("dark_background")
    plt.semilogy(df["date"], df["price"], color="grey")
    plt.semilogy(df["date"], df["5_day_ma"], color="purple")
    plt.xticks(rotation=-25)
    plt.savefig(f"./q1_2022.png")
    # plt.show()
