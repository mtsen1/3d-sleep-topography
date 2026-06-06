# 3D Sleep Topography Dashboard

An interactive, web-based 3D data visualization dashboard built with Three.js (WebGL) and Python. This platform maps the multi-night sleep macroarchitecture and continuous physiological signal trends from data collected from study participants using Apple Watches and Dreem 2 EEG headbands.

[View the Live Interactive Dashboard](https://mtsen1.github.io/3d-sleep-topography/)

---

##  Neurophysiological Validation

The final calibrated 3D terrain accurately mirrors human sleep architecture rules:
* **Homeostatic Sleep Pressure:** Visualized by the deep purple **N3 Deep Sleep** canyon consistently dominating the first third of every night (`H0`–`H3`).
* **Circadian REM Drive:** Exhibited by rolling **REM** ridges that naturally lengthen, expand, and cluster closer together in the later hours of the morning (`H5`–`H8`).
* **Normal REM Latency:** The patient properly cycles through N1, N2, and N3 before ascending into their first brief REM period approximately 90 minutes after sleep onset.

---


##  Technical Stack

* **Data Engineering Pipeline:** Python 3, Pandas, NumPy, SciPy (Signal Processing)
* **Frontend Graphics Engine:** Three.js (WebGL), JavaScript (ES6+), HTML5, CSS3

---


## References
Song, T. (2026). A Multi-Night Instantaneous Heart Rate and Accelerometry Dataset with EEG Sleep Stage Labels (version 1.0.0). PhysioNet. RRID:SCR_007345. https://doi.org/10.13026/a0sy-7t69

Song, T.-A., Zhang, Y., Zhou, Z., Hou, L., Malekzadeh, M., Behzad, A., & Dutta, J. (2025). AI-driven sleep staging using instantaneous heart rate and accelerometry: Insights from an Apple Watch study. IEEE Transactions on Biomedical Engineering. https://doi.org/10.1109/TBME.2025.3612158

Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220. RRID:SCR_007345.


