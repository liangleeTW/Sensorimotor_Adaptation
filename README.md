# Sensorimotor_Adaptation

![Experiment design](exp_flow.jpeg)


This repository contains the full experimental codebase for a **sensorimotor adaptation study** involving visual-proprioceptive calibration, sensory switching, and reaching under varying sensory contexts. The experimental logic follows the design shown below.

## Experimental Design

Participants undergo five sequential phases:

1. **Sensory Pre-Test**

   * Measures baseline alignment across sensory channels
   * Tasks: Visual (V), Proprioceptive (P), and Combined (VP) pointing
   * 40 trials per block

2. **Pre-Adaptation Phase**

   * 50 trials to establish reaching behavior before prism shift
   * Conducted under either **eyes open (EO)** or **eyes closed (EC)** conditions

3. **Adaptation Phase**

   * 100 trials under prism lens perturbation
   * Participants adapt to shifted visual feedback
   * Sensory context remains EO or EC depending on the group

4. **Sensory Post-Test**

   * Re-assessment of V/P/VP shifts after adaptation
   * Identical to the pre-test (40 trials per block)

5. **De-Adaptation & Re-Adaptation Phases**

   * Participants undergo de-adaptation (50 trials) and re-adaptation (100 trials)
   * Design allows investigation of learning retention and switching cost across contexts

The study includes four groups (repeat/switch × EO/EC), as shown in the figure.

---

## App Architecture

This application is built using **native Python with Tkinter**, enabling lightweight deployment without external front-end dependencies. Any Python installation with Tkinter support can run the experiment interface without requiring web servers or browsers.

### Why Tkinter?

* Lightweight & native to Python
* No need for Flask, Streamlit, or Electron
* Stable GUI across platforms (Windows, macOS, Linux)

---

## Hardware Integration

The experimental protocol includes **Arduino-controlled electrochromic film**, which temporarily blocks visual feedback before movement initiation, ensuring control over visual input during sensorimotor adaptation.

Communication with the Arduino is handled via **serial communication**.


![電路圖_english](https://github.com/user-attachments/assets/ee1ac387-cbbc-445b-9bcb-5035850359ff)


## 📂 Repository Structure

```
├── Pre_Adapt_De
│   └── main/
│       ├── main.ino               
│       ├── beep.wav                
│       └── main.py                 
├── Re_Adaptation
│   ├── shift_pilot_10pixel/
│   │   └── shift_pilot/
│   │       ├── shift_pilot.ino
│   │       ├── beep.wav
│   │       └── shift_pilot_10pixel.py
│   └── shift_pilot_smallrectangle/
│       └── shift_pilot/
│           ├── shift_pilot.ino
│           ├── beep.wav
│           ├── generate_new_shift_dot.ipynb
│           └── shift_pilot_smallrectangle.py
├── Sensory_PrePost/
│   └── prepost/
│       ├── prepost.ino
│       ├── beep.wav
│       ├── noice_generate.py
│       └── prepost.py
├── LICENSE
├── README.md
├── requirements.txt
```

---

## Dependencies

To run this experiment suite, first install the required Python packages. You can do this using the following command:

```bash
pip install -r requirements.txt
```

### Required Packages

* `pandas` — for data logging and CSV handling
* `pyserial` — for serial communication with Arduino
* `tkinter` — for GUI interface (comes built-in with most Python distributions)

> **Note**: `tkinter` is included by default in standard Python installations (e.g., Anaconda, python.org). If you're on Linux and it’s not installed, you may need to run:
> `sudo apt-get install python3-tk`

---

## Related Research Paper/Conference

This experiment is part of the study:

**Recommended Citation:**
Liang Lee, Yi-Zhen Hsu, Shang-Hua N. Lin, Ching-Po Lin, Li-Hung Chang. (2025).
*Investigating Implicit and Explicit Motor Adaptation Using Explainable Deep Learning Approach*.
**Taiwan Society of Cognitive Neuroscience Annual Meeting**.

**Award:** High Distinction Award, [Excellent Student Paper Competition](https://sites.google.com/view/tscn2025/%E5%84%AA%E7%A7%80%E5%AD%B8%E7%94%9F%E8%AB%96%E6%96%87%E7%AB%B6%E8%B3%BD%E6%B1%BA%E9%81%B8-student-paper-competition?authuser=0)

[Click to view/download presentation slides](https://drive.google.com/file/d/1CWUpuM9YRaO0eLdUGlJYUYY2jxPFlKBr/view?usp=sharing)

---
## Contributors

<a href="https://github.com/sizluluEZ"><img src="https://avatars.githubusercontent.com/u/132829530?v=4" width="50px;" alt="sizluluEZ"/></a>
<a href="https://github.com/liangleeTW"><img src="https://avatars.githubusercontent.com/u/52850586?v=4" width="50px;" alt="liangleeTW"/></a>

---

## License

This project is licensed under the **MIT License**. See [LICENSE](./LICENSE) for details.
