from graphs import *
import pandas

# Nedelujoče povezave na gridih, drevesih in naključnih remove centered
cols = ["Random", "Centered"]
data_1 = {}
data_2 = {}
osnoven = generate_3d_grid(50, 50, 50)
osnoven_2 = generate_3d_grid(100, 100, 100)

data_1_bin = {}
data_2_bin = {}
osnoven_b = generate_binary(10)
osnoven_2_b = generate_binary(20)

for percent in [0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.2, 0.25, 0.5]:
    print('current grid for % ' + str(percent))               # Spremeni
    rand = remove_random(generate_3d_grid(50, 50, 50), percent)
    centered = remove_centered(generate_3d_grid(50, 50, 50), percent)
    data_1[percent] = [global_efficiency(rand, osnoven), global_efficiency(centered, osnoven)]
    df_1 = pandas.DataFrame.from_dict(data_1, orient='index')
    df_1.columns = cols
    df_1.to_csv('Data/global_3d_50.csv')

    random_2 = remove_random(generate_3d_grid(100, 100, 100), percent)
    centered_2 = remove_centered(generate_3d_grid(100, 100, 100), percent)
    data_2[percent] = [global_efficiency(random_2, osnoven_2), global_efficiency(centered_2, osnoven_2)]
    df_2 = pandas.DataFrame.from_dict(data_2, orient='index')
    df_2.columns = cols
    df_2.to_csv('Data/global_3d_100.csv')

    print('current tree for % ' + str(percent))             # Spremeni
    rand = remove_random(generate_binary(10), percent)
    centered = remove_centered(generate_binary(10), percent)
    data_1_bin[percent] = [global_efficiency(rand, osnoven_b), global_efficiency(centered, osnoven_b)]
    df_1_bin = pandas.DataFrame.from_dict(data_1_bin, orient='index')
    df_1_bin.columns = cols
    df_1_bin.to_csv('Data/global_bin_10.csv')

    random_2 = remove_random(generate_binary(20), percent)
    centered_2 = remove_centered(generate_binary(20), percent)
    data_2_bin[percent] = [global_efficiency(random_2, osnoven_2_b), global_efficiency(centered_2, osnoven_2_b)]
    df_2_bin = pandas.DataFrame.from_dict(data_2_bin, orient='index')
    df_2_bin.columns = cols
    df_2_bin.to_csv('Data/global_bin_10.csv')
