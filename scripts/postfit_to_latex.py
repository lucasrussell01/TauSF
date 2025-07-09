import os
import re

fit_dir = '/vols/cms/lcr119/offline/HiggsCP/IDSFs/CMSSW_14_1_0_pre4/src/CombineHarvester/TauSF/outputs/FrozenQCD_HPS_SFs_Run3_2022EE/'


prefit_pdfs = sorted([f for f in os.listdir(os.path.join(fit_dir, 'prefit')) if f.endswith('.pdf')])
postfit_pdfs = sorted([f for f in os.listdir(os.path.join(fit_dir, 'postfit')) if f.endswith('.pdf')])

print(prefit_pdfs)
print(postfit_pdfs)

def write_figure(prefit_path, postfit_path, dm="NA", pT="NA", region="NA"):
    string = fr"""
\begin{{figure}}[htbp]
  \centering
  \begin{{subfigure}}[b]{{0.4\textwidth}}
    \includegraphics[width=\linewidth]{{{prefit_path}}}
    \caption{{PREFIT}}
  \end{{subfigure}}
  \hfill
  \begin{{subfigure}}[b]{{0.4\textwidth}}
    \includegraphics[width=\linewidth]{{{postfit_path}}}
    \caption{{POSTFIT}}
  \end{{subfigure}}
\end{{figure}}
"""
    return string


def map_bin_to_dm_pt_HPS(bin_number):
    if len(bin_number) == 1:
        dm = "$\mu\mu$"
        pt = "inclusive"
        region = 'Normalisation'
    elif len(bin_number) == 3:
        # Find DM
        if bin_number.startswith('1'):
            dm = "0"
        elif bin_number.startswith('2'):
            dm = "1"
        elif bin_number.startswith('3'):
            dm = "10"
        elif bin_number.startswith('4'):
            dm = "11"
        else:
            dm = "unknown"
        # Find pT range
        if bin_number.endswith('1'):
            pt = "20 to 25 GeV"
        elif bin_number.endswith('2'):
            pt = "25 to 30 GeV"
        elif bin_number.endswith('3'):
            pt = "30 to 35 GeV"
        elif bin_number.endswith('4'):
            pt = "35 to 40 GeV"
        elif bin_number.endswith('5'):
            pt = "40 to 50 GeV"
        elif bin_number.endswith('6'):
            pt = "50 to 60 GeV"
        elif bin_number.endswith('7'):
            pt = "60 to 80 GeV"
        elif bin_number.endswith('8'):
            pt = "80 to 100 GeV"
        elif bin_number.endswith('9'):
            pt = "100 to 200 GeV"
        else:
            pt = 'unknown'
        # determine region
        if bin_number[1] == '0':
            region = 'Signal'
        elif bin_number[1] == '1':
            region = 'High mT'
        else:
            region = 'unknown'
    return dm, pt, region

with open(os.path.join(fit_dir, "pre_post_plots.tex"), "w") as f:

    f.write("\\documentclass{article}\n\\usepackage{graphicx,subcaption}\n\\usepackage[paperwidth=22cm, paperheight=13cm, left=2cm, right=2cm, top=1cm, bottom=2cm]{geometry}\n\\begin{document}\n")

    for i, (pre,post) in enumerate(zip(prefit_pdfs, postfit_pdfs)):

        match = re.search(r"ztt_(mt|mm)_(\d+)", pre)
        if match:
            category = match.group(1)  # 'mt' or 'mm'
            number = match.group(2)    # the digits

            dm, pt, region = map_bin_to_dm_pt_HPS(number)
            # add section title
            if number == '0':
                f.write('\\section*{$\mu\mu$ normalisation region}')
            else:
                f.write(fr'\section*{{DM{dm} - {region} region - p$_T$ {pt}}}')

        f.write(write_figure(os.path.join(fit_dir, 'prefit', pre),
                            os.path.join(fit_dir, 'postfit', post),
                            dm, pt, region
                           ))


        f.write("\\clearpage\n")

    f.write(r"\end{document}")

os.system(f"pdflatex -output-directory={fit_dir} {os.path.join(fit_dir, 'pre_post_plots.tex')}")