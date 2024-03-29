import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

mtl_results = {}
stl_results = {}

stl_results["ERM"] = {
    "Big_Lips:Chubby": [(69.94, (69.57, 70.3)), (11.01, (10.56, 11.46)), (68.32, (67.94, 68.69)), (41.24, (40.53, 41.95))],
    "Bushy_Eyebrows:Blond_Hair":
        [(92.6, (92.39, 92.81)), (13.64, (5.36, 21.92)), (90.8, (90.57, 91.03)), (27.04, (16.94, 37.15))],
    "Wearing_Lipstick:Male": [
        (93.49, (93.3, 93.69)), (36.72, (28.78, 44.65)), (92.68, (92.47, 92.89)), (49.66, (41.63, 57.7))
    ],
    "Gray_Hair:Young": [(98.16, (98.05, 98.26)), (25.0, (15.0, 35.0)), (97.95, (97.84, 98.06)), (15.32, (7.09, 23.55))],
    "High_Cheekbones:Smiling":
        [(87.39, (87.12, 87.65)), (38.24, (36.79, 39.69)), (84.3, (84.01, 84.6)), (50.03, (48.6, 51.47))]
}

stl_results["RWY"] = {
    "Big_Lips:Chubby": [(69.58, (69.22, 69.95)), (49.31, (48.59, 50.03)), (67.44, (67.07, 67.82)), (57.85, (57.14, 58.57))],
    "Bushy_Eyebrows:Blond_Hair":
        [(91.57, (91.35, 91.79)), (30.0, (18.99, 41.01)), (75.64, (75.3, 75.98)), (67.32, (66.79, 67.86))],
    "Wearing_Lipstick:Male":
        [(93.59, (93.39, 93.78)), (33.87, (26.08, 41.66)), (92.68, (92.47, 92.89)), (34.0, (26.19, 41.81))],
    "Gray_Hair:Young": [(97.1, (96.96, 97.23)), (41.34, (30.07, 52.6)), (92.38, (92.17, 92.59)), (75.25, (74.33, 76.17))],
    "High_Cheekbones:Smiling":
        [(86.7, (86.43, 86.97)), (32.34, (30.94, 33.73)), (85.31, (85.02, 85.59)), (49.57, (48.19, 50.95))]
}

stl_results["SUBY"] = {
    "Big_Lips:Chubby": [(69.46, (69.09, 69.83)), (28.6, (27.95, 29.25)), (68.69, (68.32, 69.06)), (60.39, (59.69, 61.1))],
    "Bushy_Eyebrows:Blond_Hair":
        [(91.31, (91.08, 91.54)), (16.17, (7.54, 24.8)), (77.0, (76.66, 77.34)), (71.64, (71.22, 72.06))],
    "Wearing_Lipstick:Male":
        [(93.61, (93.42, 93.81)), (35.23, (27.37, 43.08)), (93.15, (92.95, 93.36)), (38.88, (30.86, 46.9))],
    "Gray_Hair:Young": [(95.93, (95.78, 96.09)), (41.15, (30.53, 51.76)), (93.0, (92.79, 93.2)), (74.1, (73.17, 75.03))],
    "High_Cheekbones:Smiling":
        [(87.67, (87.4, 87.93)), (38.49, (37.04, 39.95)), (85.13, (84.84, 85.41)), (51.95, (50.57, 53.33))]
}

stl_results["JTT"] = {
    "Big_Lips:Chubby": [(32.7, (32.33, 33.08)), (0.0, (0.0, 0.0)), (32.7, (32.33, 33.08)), (0.0, (0.0, 0.0))],
    "Bushy_Eyebrows:Blond_Hair":
        [(91.94, (91.72, 92.16)), (21.04, (11.22, 30.86)), (71.45, (71.09, 71.81)), (64.15, (63.71, 64.6))],
    "Wearing_Lipstick:Male": [
        (91.27, (91.05, 91.5)), (42.45, (34.32, 50.57)), (72.96, (72.6, 73.32)), (51.52, (49.32, 53.73))
    ],
    "Gray_Hair:Young": [(97.81, (97.69, 97.93)), (22.31, (12.82, 31.8)), (90.83, (90.6, 91.06)), (68.34, (67.53, 69.14))],
    "High_Cheekbones:Smiling":
        [(81.98, (81.67, 82.29)), (38.56, (37.11, 40.01)), (81.03, (80.72, 81.35)), (45.66, (44.34, 46.98))]
}

mtl_results["ERM"] = {
    "Pairing_1":
        {
            "Big_Lips:Chubby":
                [(70.6, (70.24, 70.97)), (15.35, (14.84, 15.87)), (66.92, (66.54, 67.29)), (59.01, (58.4, 59.61))],
            "Bushy_Eyebrows:Blond_Hair":
                [(92.76, (92.55, 92.97)), (11.75, (4.0, 19.49)), (88.63, (88.37, 88.88)), (39.17, (28.13, 50.2))]
        },
    "Pairing_2":
        {
            "Wearing_Lipstick:Male":
                [(93.64, (93.44, 93.83)), (31.19, (23.54, 38.83)), (93.6, (93.4, 93.79)), (45.95, (37.78, 54.13))],
            "Gray_Hair:Young":
                [(98.17, (98.06, 98.27)), (26.3, (16.14, 36.46)), (96.93, (96.79, 97.07)), (40.88, (29.78, 51.99))]
        },
    "Pairing_3":
        {
            "High_Cheekbones:Smiling":
                [(87.75, (87.48, 88.01)), (36.44, (35.0, 37.88)), (84.83, (84.55, 85.12)), (53.1, (51.72, 54.47))],
            "Wearing_Lipstick:Male":
                [(94.01, (93.82, 94.2)), (32.04, (24.4, 39.68)), (93.2, (93.0, 93.41)), (42.49, (34.35, 50.63))]
        }
}

mtl_results["RWY"] = {
    "Pairing_1":
        {
            "Big_Lips:Chubby":
                [(69.65, (69.28, 70.02)), (28.98, (28.33, 29.63)), (66.06, (65.68, 66.44)), (58.87, (58.16, 59.58))],
            "Bushy_Eyebrows:Blond_Hair":
                [(88.79, (88.53, 89.04)), (41.49, (30.25, 52.73)), (80.75, (80.43, 81.06)), (73.53, (72.82, 74.24))]
        },
    "Pairing_2":
        {
            "Wearing_Lipstick:Male":
                [(92.5, (92.29, 92.71)), (30.74, (23.18, 38.31)), (85.83, (85.55, 86.1)), (42.61, (41.24, 43.97))],
            "Gray_Hair:Young":
                [(93.63, (93.44, 93.83)), (71.95, (70.99, 72.9)), (92.83, (92.62, 93.04)), (51.11, (42.89, 59.32))]
        },
    "Pairing_3":
        {
            "High_Cheekbones:Smiling":
                [(86.73, (86.46, 87.0)), (35.02, (33.59, 36.44)), (92.37, (92.16, 92.58)), (50.87, (48.66, 53.07))],
            "Wearing_Lipstick:Male":
                [(93.45, (93.25, 93.65)), (38.02, (30.06, 45.99)), (92.65, (92.45, 92.86)), (77.04, (76.31, 77.76))]
        }
}

mtl_results["SUBY"] = {
    "Pairing_1":
        {
            "Big_Lips:Chubby":
                [(67.33, (66.96, 67.71)), (47.29, (46.58, 48.01)), (64.07, (63.68, 64.45)), (61.45, (60.84, 62.05))],
            "Bushy_Eyebrows:Blond_Hair":
                [(84.37, (84.08, 84.66)), (44.82, (33.07, 56.57)), (79.56, (79.24, 79.88)), (72.23, (71.51, 72.96))]
        },
    "Pairing_2":
        {
            "Wearing_Lipstick:Male":
                [(92.27, (92.05, 92.48)), (51.03, (49.73, 52.34)), (92.13, (91.92, 92.35)), (55.18, (52.98, 57.37))],
            "Gray_Hair:Young":
                [(91.33, (91.11, 91.56)), (69.41, (68.43, 70.39)), (90.89, (90.66, 91.12)), (68.42, (67.61, 69.23))]
        },
    "Pairing_3":
        {
            "High_Cheekbones:Smiling":
                [(87.64, (87.37, 87.9)), (41.07, (39.6, 42.54)), (83.96, (83.67, 84.26)), (52.36, (51.03, 53.7))],
            "Wearing_Lipstick:Male":
                [(93.96, (93.77, 94.15)), (36.83, (28.88, 44.79)), (93.25, (93.05, 93.45)), (52.56, (44.37, 60.76))]
        }
}

mtl_results["JTT"] = {
    "Pairing_1":
        {
            "Big_Lips:Chubby":
                [(61.14, (60.75, 61.53)), (54.02, (53.48, 54.57)), (60.03, (59.63, 60.42)), (50.47, (49.93, 51.02))],
            "Bushy_Eyebrows:Blond_Hair":
                [(72.96, (72.6, 73.31)), (67.3, (66.86, 67.74)), (77.42, (77.09, 77.76)), (68.85, (68.11, 69.6))]
        },
    "Pairing_2":
        {
            "Wearing_Lipstick:Male":
                [(91.36, (91.13, 91.58)), (41.09, (32.98, 49.2)), (76.79, (76.45, 77.12)), (51.79, (43.59, 59.99))],
            "Gray_Hair:Young":
                [(96.48, (96.34, 96.63)), (41.59, (30.23, 52.94)), (86.85, (86.58, 87.12)), (61.31, (60.46, 62.15))]
        },
    "Pairing_3":
        {
            "High_Cheekbones:Smiling":
                [(83.72, (83.43, 84.02)), (36.23, (34.8, 37.66)), (82.99, (82.69, 83.29)), (82.99, (82.69, 83.29))],
            "Wearing_Lipstick:Male":
                [(92.91, (92.7, 93.11)), (33.32, (25.54, 41.1)), (91.28, (91.05, 91.5)), (51.11, (48.9, 53.31))]
        }
}


def mtl_stl_results(stl_dict, mtl_dict, group_acc=True):
    mtl_acc = 0
    stl_acc = 0

    mtl_se = 0
    stl_se = 0

    for pairing_num in mtl_dict.keys():
        for task_name in mtl_dict[pairing_num]:

            mtl_results = mtl_dict[pairing_num][task_name]
            stl_results = stl_dict[task_name]

            if group_acc:
                mtl_acc += mtl_results[3][0]
                stl_acc += stl_results[3][0]

                mtl_wg_std = mtl_results[3][1][1] - mtl_results[3][1][0]
                mtl_wg_std /= 2

                stl_wg_std = stl_results[3][1][1] - stl_results[3][1][0]
                stl_wg_std /= 2

                mtl_se += mtl_wg_std**2
                stl_se += stl_wg_std**2

            else:
                mtl_acc += mtl_results[2][0]
                stl_acc += stl_results[2][0]

                mtl_avg_std = mtl_results[2][1][1] - mtl_results[2][1][0]
                mtl_avg_std /= 2

                stl_avg_std = stl_results[2][1][1] - stl_results[2][1][0]
                stl_avg_std /= 2

                mtl_se += mtl_avg_std**2
                stl_se += stl_avg_std**2

    mtl_acc /= (len(mtl_dict.keys()) * 2)
    stl_acc /= (len(mtl_dict.keys()) * 2)

    mtl_se = np.sqrt(mtl_se) / (len(mtl_dict.keys()) * 2)
    stl_se = np.sqrt(stl_se) / (len(mtl_dict.keys()) * 2)

    return stl_acc, stl_se, mtl_acc, mtl_se


def make_mtl_stl_plot(group_acc=True):
    erm_gains = mtl_stl_results(stl_results["ERM"], mtl_results["ERM"], group_acc)
    rwy_gains = mtl_stl_results(stl_results["RWY"], mtl_results["RWY"], group_acc)
    suby_gains = mtl_stl_results(stl_results["SUBY"], mtl_results["SUBY"], group_acc)
    jtt_gains = mtl_stl_results(stl_results["JTT"], mtl_results["JTT"], group_acc)

    y_label = "Mean Worst Group Accuracy Across Tasks" if group_acc else "Mean Average Accuracy Across Tasks"

    opt_data = [
        [erm_gains[0], erm_gains[1], 'STL', 'ERM'], [erm_gains[2], erm_gains[3], 'MTL', 'ERM'],
        [rwy_gains[0], rwy_gains[1], 'STL', 'RWY'], [rwy_gains[2], rwy_gains[3], 'MTL', 'RWY'],
        [suby_gains[0], suby_gains[1], 'STL', 'SUBY'], [suby_gains[2], suby_gains[3], 'MTL', 'SUBY'],
        [jtt_gains[0], jtt_gains[1], 'STL', 'JTT'], [jtt_gains[2], jtt_gains[3], 'MTL', 'JTT']
    ]

    avg_opt_df = pd.DataFrame(opt_data, columns=[y_label, "SE", 'Learning Type', 'Optimization Procedure'])
    plt.figure(figsize=(14, 10))
    sns.barplot(x='Optimization Procedure', y=y_label, hue='Learning Type', data=avg_opt_df)

    bar_indices = np.array([0, 1, 2, 3])
    bar_indices = np.repeat(bar_indices, 2)

    width = .25
    add = np.array([-1 * width, width])
    add = np.tile(add, 4)
    x = bar_indices + add

    plt.errorbar(x=x, y=avg_opt_df[y_label], yerr=avg_opt_df['SE'], fmt='none', c='black', capsize=2)

    os.makedirs(os.path.join("./plots", "mtl_vs_stl"), exist_ok=True)
    plt.title(f"STL vs MTL Comparison")
    plt.savefig(f"./plots/mtl_vs_stl/optimization_comparison_group_acc{str(group_acc)}.png")
    plt.close()


make_mtl_stl_plot(group_acc=True)
make_mtl_stl_plot(group_acc=False)
