import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


mtl_results = {}
stl_results = {}

stl_results["ERM"] = {"Big_Lips:Chubby": [(69.93, (69.57, 70.30)), (11.27, (10.81, 11.72)), (68.32, (67.94, 68.69)), (41.26, (40.55, 41.97))],
    "Bushy_Eyebrows:Blond_Hair":
        [(92.60, (92.39, 92.81)), (15.64, (7.12, 24.15)), (90.62, (90.39, 90.85)), (32.82, (21.81, 43.83))]}

stl_results["RWY"] = {"Big_Lips:Chubby": [(69.52, (69.15,69.89)), (49.34, (48.62,50.06)), (67.39, (67.01,67.76)), (57.85, (57.13,58.56))],
    "Bushy_Eyebrows:Blond_Hair": [(91.56, (91.33,91.78)), (30.30, (20.50,42.27)), (75.28, (74.93,75.62)), (66.92, (66.39,67.46))]}

stl_results["SUBY"] = {"Big_Lips:Chubby": [(69.45, (69.08,69.82)), (28.90, (28.24,29.55)), (68.68, (68.31,69.05)), (60.39, (59.68,61.09))],
     "Bushy_Eyebrows:Blond_Hair": [(91.30, (91.08,91.53)), (21.36, (11.75,30.98)), (76.99, (76.66,77.33)), (71.63, (71.21,72.05))]}

stl_results["JTT"] = {"Big_Lips:Chubby": [(32.7, (32.33,33.08)), (0.01, (0.0,0.01)), (32.7, (32.33,33.08)), (0.01, (0.0,0.01))],
    "Bushy_Eyebrows:Blond_Hair": [(91.93, (91.71,92.15)), (22.80, (12.96,32.63)), (71.35, (70.99,71.71)), (64.07, (63.62,64.52))]}


mtl_results["ERM"] = {
    "Big_Lips:Chubby": [(70.6, (70.24, 70.97)), (15.49, (14.97, 16.02)), (66.9, (66.53, 67.28)), (58.84, (58.23, 59.45))],
    "Bushy_Eyebrows:Blond_Hair":
        [(92.76, (92.55, 92.96)), (14.2, (6.02, 22.39)), (88.52, (88.27, 88.78)), (41.41, (29.86, 52.96))]
}

mtl_results["RWY"] = {
    "Big_Lips:Chubby": [(69.63, (69.26,70.0)), (29.8, (29.14,30.45)), (66.05, (65.68,66.43)), (58.84, (58.13,59.55))],
    "Bushy_Eyebrows:Blond_Hair":
        [(88.31, (88.05,88.56)), (44.27, (32.62,55.92)), (80.63, (80.31,80.95)), (73.52, (72.8,74.23))]
}

mtl_results["SUBY"] = {
    "Big_Lips:Chubby": [(67.32, (66.95,67.7)), (47.35, (46.63,48.07)), (64.06, (63.68,64.45)), (61.44, (60.84,62.04))],
    "Bushy_Eyebrows:Blond_Hair":
        [(84.35, (84.06,84.65)), (45.7, (34.02,57.39)), (79.48,(79.15,79.8)), (72.22, (71.5,72.95))]
}

mtl_results["JTT"] = {
    "Big_Lips:Chubby": [(61.1, (60.71,61.49)), (53.97, (53.42,54.52)), (59.93, (59.54,60.33)), (50.46, (49.9,51.01))],
    "Bushy_Eyebrows:Blond_Hair":
        [(72.9, (72.55,73.26)), (67.22, (66.79,67.66)), (77.24, (76.91,77.58)), (68.85, (68.1,69.6))]
}


def make_plot(wg_acc = True):

    plt.figure(figsize=(12, 7))
    avg_opt_data = []

    y_label = "Mean Worst Group Accuracy Across Tasks" if wg_acc else "Mean Average Accuracy Across Tasks"

    for opt_type in mtl_results.keys():
        
        avg_mtl = 0
        avg_stl = 0

        for task_name in mtl_results[opt_type]:

            mtl_res = mtl_results[opt_type][task_name]
            stl_res = stl_results[opt_type][task_name]

            if wg_acc:
                avg_mtl += mtl_res[3][0]
                avg_stl += stl_res[3][0]
            else:
                avg_mtl += mtl_res[2][0]
                avg_stl += stl_res[2][0]
                

        avg_mtl /= len(mtl_results[opt_type])
        avg_stl /= len(mtl_results[opt_type])

        avg_opt_data.append([avg_stl, "STL", opt_type])
        avg_opt_data.append([avg_mtl, "MTL", opt_type])


    avg_opt_df = pd.DataFrame(avg_opt_data, columns=[y_label, 'Learning Type', 'Optimization Procedure'])


    sns.barplot(x = 'Optimization Procedure',
            y = y_label,
            hue = 'Learning Type',
            data = avg_opt_df)

            
    plt.title(f"STL vs MTL Comparison")
    plt.savefig(f"./plots/stl_mtl_comparison_wg_{wg_acc}.png")
    plt.close()

make_plot(wg_acc = True)
make_plot(wg_acc = False)