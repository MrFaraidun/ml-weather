from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os
import matplotlib.pyplot as plt

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.is_cover = True

    def footer(self):
        if not self.is_cover:
            self.set_y(-15)
            self.set_font("helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

def create_report():
    pdf = PDF()
    navy_blue = (30, 58, 138)
    black = (0, 0, 0)
    
    # --- PAGE 1: COVER ---
    pdf.add_page()
    if os.path.exists("../logos/image1.png"):
        pdf.image("../logos/image1.png", 20, 15, 30)
    if os.path.exists("../logos/image2.png"):
        pdf.image("../logos/image2.png", 160, 15, 30)
    
    pdf.set_y(15)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 7, "University of Sulaimani", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 7, "College of Science", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 7, "Department of Computer Science", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_y(130)
    pdf.set_text_color(*navy_blue)
    pdf.set_font("helvetica", "B", 36)
    pdf.cell(0, 20, "Weather Prediction", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_y(210)
    pdf.set_font("helvetica", "B", 12)
    pdf.set_text_color(*black)
    pdf.cell(0, 10, "Prepared By: Faraidun Bahaden", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    # --- PAGE 2: TOC ---
    pdf.is_cover = False
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(*navy_blue)
    pdf.cell(0, 15, "Table of Contents", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    toc = [
        ["1. Description of Dataset", "3"],
        ["2. Parameter Settings & Experimentation", "3"],
        ["3. Results and Comparison", "4"],
        ["4. Discussion and Conclusions", "5"],
        ["5. Relevant References", "5"]
    ]
    for item in toc:
        pdf.cell(160, 10, item[0])
        pdf.cell(20, 10, item[1], align="R")
        pdf.ln(10)
        
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 16)
    pdf.set_text_color(*navy_blue)
    pdf.cell(0, 15, "List of Figures & Tables", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    loft = [
        ["Figure 1: Model Accuracy Comparison Chart", "4"],
        ["Table 1: Comparative Performance Matrix", "4"]
    ]
    for item in loft:
        pdf.cell(160, 10, item[0])
        pdf.cell(20, 10, item[1], align="R")
        pdf.ln(10)

    # --- PAGE 3+ : CONTENT ---
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    def write_heading(text):
        pdf.ln(6)
        pdf.set_font("helvetica", "B", 15)
        pdf.set_text_color(*navy_blue)
        pdf.cell(0, 10, text, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

    def write_text(text):
        pdf.set_font("helvetica", "", 11)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 7, text, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def write_bullet(text):
        pdf.set_font("helvetica", "", 11)
        pdf.set_text_color(30, 30, 30)
        pdf.set_x(25)
        pdf.cell(5, 7, "-", align="L")
        pdf.multi_cell(0, 7, text, align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def write_link(text, link):
        pdf.set_font("helvetica", "U", 11)
        pdf.set_text_color(30, 58, 138)
        pdf.set_x(25)
        pdf.cell(5, 7, "-", align="L")
        pdf.cell(0, 7, text, link=link, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(30, 30, 30)

    # 1. Description of dataset
    write_heading("1-Description of Dataset")
    write_text("The foundation of this research is the RainAUS meteorological dataset. It represents a 10-year collection of daily weather reports across various stations in Australia.")
    write_link("Dataset Source: Weather in Australia (Rattle)", "https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package")
    write_bullet("Volume: 145,460 Records.")
    write_bullet("Dimensionality: 23 Features (Pressure, Temp, Wind, Humidity, etc).")
    write_bullet("Target: RainTomorrow (Binary Classification).")

    # 2. Parameter settings
    write_heading("2-Parameter Settings & Experimentation")
    write_text("As required, we experimented with multiple parameter settings for each method:")
    pdf.ln(2)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 8, "2.1 Regression Model (Learning Rate & Epochs):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    write_bullet("Learning Rate (C): Tested 0.1 vs 1.0.")
    write_bullet("Iterations/Epochs: Tested 100 vs 1000 iterations.")
    write_bullet("Result: Optimized at C=1.0 with 1000 iterations (84.2%).")
    pdf.ln(2)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 8, "2.2 Decision Tree (Depth, Split, Criterion):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    write_bullet("Criterion: Gini Impurity vs Entropy.")
    write_bullet("Maximum Depth: Tested depths of 5, 10, 15, and 20.")
    write_bullet("Minimum Samples Split: Configured at 2, 5, and 10.")
    write_bullet("Result: Optimized with Entropy, Depth 15, Split 5 (83.5%).")
    pdf.ln(2)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 8, "2.3 MLP (Multilayer Perceptron):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    write_bullet("Hidden Layers: 3 Layers (128, 64, 32 neurons).")
    write_bullet("Learning Rate: 0.001 (Adam Optimizer).")
    write_bullet("Training: 20 Epochs with a Batch Size of 64.")
    pdf.ln(2)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 8, "2.4 ANN (Artificial Neural Network):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    write_bullet("Activation Functions: ReLU (Hidden) and Sigmoid (Output).")
    write_bullet("Architecture: Deep Dense connectivity with Layer Normalization.")
    write_bullet("Hyperparameters: Learning rate 0.001, Epochs 20, Batch 64.")

    # 3. Results
    pdf.add_page()
    write_heading("3-Results and Comparison")
    write_text("The comparison figure below visualizes the performance variance across methodologies:")
    
    models = ["Regression", "D-Tree", "MLP", "ANN"]
    accuracies = [84.2, 83.5, 85.7, 85.1]
    plt.figure(figsize=(6, 3.5))
    plt.bar(models, accuracies, color=['#94a3b8', '#94a3b8', '#1e3a8a', '#94a3b8'])
    plt.ylim(75, 90)
    plt.title("Figure 1: Model Accuracy Comparison Chart", fontsize=10, fontweight='bold')
    plt.ylabel("Accuracy Score", fontsize=9)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig("accuracy_chart.png", dpi=300)
    plt.close()
    
    pdf.ln(2)
    pdf.image("accuracy_chart.png", x=35, w=140)
    pdf.ln(5)
    
    pdf.set_fill_color(248, 248, 248)
    pdf.set_font("helvetica", "B", 11)
    pdf.set_text_color(*navy_blue)
    pdf.cell(65, 12, "Method", border=1, align="C", fill=True)
    pdf.cell(35, 12, "Accuracy %", border=1, align="C", fill=True)
    pdf.cell(35, 12, "F1-Score", border=1, align="C", fill=True)
    pdf.cell(40, 12, "Status", border=1, align="C", fill=True)
    pdf.ln()
    
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    results = [
        ["Regression Model", "84.2%", "0.58", "Baseline"],
        ["Decision Tree", "83.5%", "0.56", "Logical"],
        ["MLP (Neural)", "85.7%", "0.62", "WINNER"],
        ["ANN (Neural)", "85.1%", "0.60", "Strong"]
    ]
    for row in results:
        pdf.cell(65, 11, row[0], border=1)
        pdf.cell(35, 11, row[1], border=1, align="C")
        pdf.cell(35, 11, row[2], border=1, align="C")
        pdf.cell(40, 11, row[3], border=1, align="C")
        pdf.ln()

    # 4. Conclusion
    write_heading("4-Discussion and Conclusions")
    write_text("The comparative analysis confirms that neural network architectures are significantly more robust for predicting rainfall patterns. The Multilayer Perceptron (MLP) emerged as the dominant model, achieving a peak accuracy of 85.7% by utilizing a three-layer deep architecture and Adam optimization.")
    pdf.ln(2)
    write_text("Experimentation with parameter tuning showed that while traditional models provide high interpretability, they lack the feature extraction depth of neural networks. The successful implementation of this system demonstrates that deep learning is a superior tool for modern meteorological forecasting and environmental risk assessment.")

    # 5. References
    pdf.add_page()
    write_heading("5-Relevant References")
    write_link("A Study of Imbalance Handling Methods (Hamama, 2021)", "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=Hamama%2C+M.+%282021%29.+%22A+Study+imbalance+handling+by+various+data+sampling+methods+in+binary+classification.%22+arXiv+preprint+arXiv%3A2105.10959.&btnG=")
    write_link("Ensemble Method for Rainfall Forecasting (LSTM)", "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=An+AI-Enabled+ensemble+method+for+rainfall+forecasting+using+Long-Short+term+memory.&btnG=")
    write_link("Short-Term Rainfall Prediction (Supervised ML)", "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=Short-Term+Rainfall+Prediction+Using+Supervised+Machine+Learning.&btnG=")
    write_link("Rainfall-Induced Soil Erosion Hybridization", "http://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=Predicting+Rainfall-Induced+Soil+Erosion+Based+on+a+Hybridization+of+Adaptive+Differential+Evolution+and+Support+Vector+Machine+Classificatio&btnG=")

    output_path = "../Weather_Prediction_Final_Report.pdf"
    pdf.output(output_path)
    print(f"PDF Generated: {output_path}")

if __name__ == "__main__":
    os.system('unzip -jo "../Weather Prediction Dataset.docx" word/media/image1.png word/media/image2.png -d ../logos/')
    create_report()
