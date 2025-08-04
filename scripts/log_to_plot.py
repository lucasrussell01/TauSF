import numpy as np
import matplotlib.pyplot as plt
import re
import mplhep as hep
import argparse
import os


plt.style.use(hep.style.CMS)
plt.rcParams.update({"font.size": 16})


def get_args():
    parser = argparse.ArgumentParser(description="Plot pre and post fit to a single pdf")
    parser.add_argument('--fit_dir', required=True, help='path to fit directory')
    parser.add_argument('--era', default='Run3', help='Era to use for the plots')
    return parser.parse_args()

args = get_args()
fit_dir = args.fit_dir
era = args.era


file = os.path.join(fit_dir, "fit_log.txt")


with open(file) as f:
    log = f.read()
    
blocks = log.split('best fit parameter values and profile-likelihood uncertainties:')

variations = ['Initial', 'Nominal', 'TES up', "TES down", "byErasAndBins frozen", "byErasAndBins and byBins frozen", "byErasAndBins, byBins, and byDM frozen", "No TES shift"]
DMs = ['DM0', 'DM1', 'DM2', 'DM10', 'DM11']
variations_to_plot = [ "No TES shift", 'TES up', "TES down", 'Nominal']
pT_bin_edges = np.array([20, 25, 30, 35, 40, 50, 60, 80, 100, 200])
pT_central = 0.5 * (pT_bin_edges[:-1] + pT_bin_edges[1:])

results_dict = {"Nominal": {}, "TES up": {}, "TES down": {}, "No TES shift": {}}

for block, variation in zip(blocks[1:], variations):
    block = block.split('Done in ')[0] # remove pointless text
    lines = block.splitlines()[1:]
    print(lines)
    # print(lines)
    # print('\n\n\n\n\n\n\n\n\n')
    if variation not in variations_to_plot:
        print("\n\nSkipping variation:", variation)
        continue

    print(f"\n\nVariation: {variation}")

    var_dict = {"DM0": {"nom":[], 'err_up':[], 'err_down':[]}, "DM1":  {"nom":[], 'err_up':[], 'err_down':[]}, "DM2":  {"nom":[], 'err_up':[], 'err_down':[]}, "DM10":  {"nom":[], 'err_up':[], 'err_down':[]}, "DM11":  {"nom":[], 'err_up':[], 'err_down':[]}}

    for DM in DMs:
        print('-'*100)
        for line in lines:
            match = re.search(rf"(rate_tauSF_{DM}_pT\d+to\d+_Run3_\w+)\s*:\s*\+([\d.]+)\s*-([\d.]+)/\+([\d.]+)", line)
            print(repr(line))
            if match:
                print("Read value for", match.group(1), ":", match.group(2), "+", match.group(4), "-", match.group(3))
                var_dict[DM]["nom"].append(float(match.group(2)))
                var_dict[DM]["err_up"].append(float(match.group(4)))
                var_dict[DM]["err_down"].append(float(match.group(3)))

        if (len(var_dict[DM]["nom"]) != len(pT_central)) or (len(var_dict[DM]["err_up"]) != len(pT_central)) or (len(var_dict[DM]["err_down"]) != len(pT_central)):
            raise ValueError(f"Missing entries for {DM} in variation {variation}")
    # store in output dictionary
    results_dict[variation] = var_dict



print('\n\n Results dictionary:')
print(results_dict)


for DM in DMs:
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    low = np.min(results_dict["TES up"][DM]["nom"]) - 0.1
    high = np.max(results_dict["TES down"][DM]["nom"]) + 0.1

    # Nominal
    nom_values = results_dict["Nominal"][DM]["nom"]
    err_up = results_dict["Nominal"][DM]["err_up"]
    err_down = results_dict["Nominal"][DM]["err_down"]
    axs[0,0].axhline(1, color='lightgray', linestyle='--')
    axs[0,0].errorbar(pT_central, nom_values, xerr = [np.diff(pT_bin_edges)/2], yerr=[err_down, err_up], label="Nominal", fmt='o', capsize=5, markersize=4, color="black")
    axs[0,0].set_ylim(low, high)
    axs[0,0].set_xlim(20, 200)
    axs[0,0].set_xlabel(r"p$_T$ (GeV)")
    axs[0,0].set_ylabel("SF")
    axs[0,0].legend()

    # No TES shift
    nom_values = results_dict["No TES shift"][DM]["nom"]
    err_up = results_dict["No TES shift"][DM]["err_up"]
    err_down = results_dict["No TES shift"][DM]["err_down"]
    axs[0,1].axhline(1, color='lightgray', linestyle='--')
    axs[0,1].errorbar(pT_central, nom_values, xerr = [np.diff(pT_bin_edges)/2], yerr=[err_down, err_up], label="No TES shift", fmt='o', capsize=5, markersize=4, color="blue")
    axs[0,1].set_ylim(low, high)
    axs[0,1].set_xlim(20, 200)
    axs[0,1].set_xlabel(r"p$_T$ (GeV)")
    axs[0,1].set_ylabel("SF")
    axs[0,1].legend()

    #  TES UP
    nom_values = results_dict["TES up"][DM]["nom"]
    err_up = results_dict["TES up"][DM]["err_up"]
    err_down = results_dict["TES up"][DM]["err_down"]
    axs[1,0].axhline(1, color='lightgray', linestyle='--')
    axs[1,0].errorbar(pT_central, nom_values, xerr = [np.diff(pT_bin_edges)/2], yerr=[err_down, err_up], label="TES up", fmt='o', capsize=5, markersize=4, color="red")
    axs[1,0].set_ylim(low, high)
    axs[1,0].set_xlim(20, 200)
    axs[1,0].set_xlabel(r"p$_T$ (GeV)")
    axs[1,0].set_ylabel("SF")
    axs[1,0].legend()


    #  TES DOWN
    nom_values = results_dict["TES down"][DM]["nom"]
    err_up = results_dict["TES down"][DM]["err_up"]
    err_down = results_dict["TES down"][DM]["err_down"]
    axs[1,1].axhline(1, color='lightgray', linestyle='--')
    axs[1,1].errorbar(pT_central, nom_values, xerr = [np.diff(pT_bin_edges)/2], yerr=[err_down, err_up], label="TES down", fmt='o', capsize=5, markersize=4, color="orange")
    axs[1,1].set_ylim(low, high)
    axs[1,1].set_xlim(20, 200)
    axs[1,1].set_xlabel(r"p$_T$ (GeV)")
    axs[1,1].set_ylabel("SF")
    axs[1,1].legend()

    fig.suptitle(f"{DM} for {era}")

    fig.tight_layout()


    fig.subplots_adjust(hspace=0.25, wspace=0.15)

    os.makedirs(f"{fit_dir}/LUCAS_plots", exist_ok=True)
    plt.savefig(f"{fit_dir}/LUCAS_plots/summary_{DM}_SF_{era}_vars.png")


# # Plots with all variations in ratio
# for DM in DMs:
#     fig, (ax, ax_ratio) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [4, 1]}, sharex=True, figsize=(10, 8))

#     # have nominal SFs here
#     nom_values = results_dict["Nominal"][DM]["nom"]
#     err_up = results_dict["Nominal"][DM]["err_up"]
#     err_down = results_dict["Nominal"][DM]["err_down"]
#     ax.axhline(1, color='lightgray', linestyle='--')
#     ax.errorbar(pT_central, nom_values, xerr = [np.diff(pT_bin_edges)/2], yerr=[err_down, err_up], label="Nominal", fmt='o', capsize=5, markersize=4, color="black")


#     ax_ratio.set_xlabel(r"p$_T$ (GeV)")
#     ax.set_ylabel("SF")
#     ax_ratio.set_ylabel("Ratio to Nominal")

#     fig.subplots_adjust(hspace=0.05)
#     plt.savefig(f"{DM}_SF_{era}.png")

