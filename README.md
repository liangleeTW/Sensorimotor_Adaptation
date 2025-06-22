# Sensorimotor_Adaptation

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

---

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

## License

This project is licensed under the **MIT License**. See [LICENSE](./LICENSE) for details.
