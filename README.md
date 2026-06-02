# 3D Sleep Topography Dashboard

An interactive, web-based 3D data visualization dashboard built with Three.js (WebGL) and Python. This platform maps multi-night sleep macro-architecture and continuous physiological signal trends using clinical polysomnography (PSG) datasets.

[View the Live Interactive Dashboard](https://mtsen1.github.io/3d-sleep-topography/)

---

##  Neurophysiological Validation

The final calibrated 3D terrain accurately mirrors human sleep architecture rules:
* **Homeostatic Sleep Pressure:** Visualized by the deep purple **N3 Slow-Wave Sleep** canyon consistently dominating the first third of every night (`H0`–`H3`).
* **Circadian REM Drive:** Exhibited by rolling **REM Coral** ridges that naturally lengthen, expand, and cluster closer together in the later hours of the morning (`H5`–`H8`).
* **Normal REM Latency:** The patient properly cycles through N1, N2, and N3 before ascending into their first brief REM period approximately 90 minutes after sleep onset.
* **Clinical Anomaly Detection:** Night 7 (the far back edge of the terrain) visually exposes an acute clinical disruption, displaying severe sleep fragmentation and near-total REM deprivation.

---


##  Technical Stack

* **Data Engineering Pipeline:** Python 3, Pandas, NumPy, SciPy (Signal Processing)
* **Frontend Graphics Engine:** Three.js (WebGL), JavaScript (ES6+), HTML5, CSS3


