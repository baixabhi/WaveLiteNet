# **WaveLiteNet: Ultra-Lightweight Wavelet-Enhanced CNN for Chest Radiology Analysis**  

WaveLiteNet is an **optimized, ultra-lightweight deep learning model** designed for **efficient chest radiology analysis**. By integrating **MobileNetV2 optimizations** and **Dual Tree Wavelet Transformation (DTWT)**, it achieves **state-of-the-art (SOTA) performance** with significantly reduced computational complexity.  

## 🚀 **Key Features**  
 🔹 **Optimized MobileNetV2** → Reduced model parameters by **66.5%** (from **3.4M** to **1.14M**) while maintaining high accuracy.  
 🔹 **Dual Tree Wavelet Transformation (DTWT)** → Enhances feature extraction and suppresses noise for improved radiology image analysis.  
 🔹 **High Performance** → Achieved **96% accuracy** and **99.7% AUC**, outperforming SOTA models without losing essential diagnostic features.  
 🔹 **Edge-Ready & Lightweight** → Ideal for real-world deployment on resource-constrained devices.  

## 📁 **Project Structure**  
```plaintext
📂 WaveLiteNet
│── 📜 README.md                     # Project documentation
│── 📂 training                      # Model training script
│── 📂 preprocessing                 # preprocessing
│── 📜 test.py                       # Model evaluation script
│── 📂 model                         # WaveLiteNet architecture
│── 📂 dataset                       # Sample dataset for testing
│── 📂 experimental results          # Model predictions & evaluations
```
## 🔧 **Installation & Setup**  
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-username/WaveLiteNet.git
   cd WaveLiteNet
   ```
2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Training Script**  
   ```bash
   python train.py
   ```
4. **Evaluate the Model**  
   ```bash
   python test.py
   ```

## 📊 **Results & Performance**  
| Model      | Parameters | Accuracy | AUC  |  
|------------|------------|----------|------|  
| SOTA Model | 3.4M       | 95.5%    | 99.5% |  
| **WaveLiteNet** | **1.14M** | **96.0%** | **99.7%** |  

## 📌 **Future Improvements**  
✅ Further optimize computational efficiency for **real-time deployment**  
✅ Expand dataset for **robustness across multiple radiology conditions**  
✅ Explore **self-supervised learning** for enhanced feature learning  

## 🤝 **Contributing**  
Contributions are welcome! Feel free to open an issue or submit a pull request.  

## 📜 **License**  
This project is licensed under the **MIT License**.  
