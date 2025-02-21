# **WaveLiteNet: Ultra-Lightweight Wavelet-Enhanced CNN for Chest Radiology Analysis**  

WaveLiteNet is an **optimized, ultra-lightweight deep learning model** designed for **efficient chest radiology analysis**. By integrating **MobileNetV2 optimizations** and **Dual Tree Wavelet Transformation (DTWT)**, it achieves **state-of-the-art (SOTA) performance** with significantly reduced computational complexity.  

## 🚀 **Key Features**  
- 🔹 **Optimized MobileNetV2** → Reduced model parameters by **66.5%** (from **3.4M** to **1.14M**) while maintaining high accuracy.  
- 🔹 **Dual Tree Wavelet Transformation (DTWT)** → Enhances feature extraction and suppresses noise for improved radiology image analysis.  
- 🔹 **High Performance** → Achieved **96% accuracy** and **99.7% AUC**, outperforming SOTA models without losing essential diagnostic features.  
- 🔹 **Edge-Ready & Lightweight** → Ideal for real-world deployment on resource-constrained devices.  

## 📁 **Project Structure**  
```plaintext
📂 WaveLiteNet
│── 📜 README.md        # Project documentation
│── 📜 requirements.txt  # Dependencies
│── 📜 train.py         # Model training script
│── 📜 test.py          # Model evaluation script
│── 📜 model.py         # WaveLiteNet architecture
│── 📂 dataset          # Sample dataset for testing
│── 📂 results          # Model predictions & evaluations
