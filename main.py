import customtkinter as ctk
import numpy as np
from tkinter import messagebox, filedialog
from fpdf import FPDF
import threading
import time


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Health Analyzer - by Manu Mahadev")
app.state('zoomed')  # Full-screen


header_frame = ctk.CTkFrame(app, fg_color="#C8E6C9", corner_radius=20)
header_frame.pack(pady=20, padx=50, fill="x")

header_label = ctk.CTkLabel(header_frame, text="Health Risk Analyzer", font=("Poppins Bold", 28))
header_label.pack(pady=15)

subtitle_label = ctk.CTkLabel(header_frame, text="Insulin Resistance & Fatty Liver Index", font=("Poppins", 16))
subtitle_label.pack(pady=5)


tabview = ctk.CTkTabview(app, width=900)
tabview.pack(padx=50, pady=30, fill="both", expand=True)
tabview.add("Insulin Resistance")
tabview.add("Fatty Liver Index")


ins_tab = tabview.tab("Insulin Resistance")
ctk.CTkLabel(ins_tab, text="Insulin Resistance Calculator", font=("Poppins Bold", 18)).pack(pady=10)


bmi_mode_i = ctk.StringVar(value="bmi")
def switch_mode_i():
    if bmi_mode_i.get() == "bmi":
        bmi_entry_i.pack(pady=5)
        weight_entry_i.pack_forget()
        height_entry_i.pack_forget()
    else:
        bmi_entry_i.pack_forget()
        weight_entry_i.pack(pady=5)
        height_entry_i.pack(pady=5)

ctk.CTkRadioButton(ins_tab, text="Enter BMI", variable=bmi_mode_i, value="bmi", command=switch_mode_i).pack(side="left", padx=30, pady=5)
ctk.CTkRadioButton(ins_tab, text="Enter Height & Weight", variable=bmi_mode_i, value="hw", command=switch_mode_i).pack(side="left", padx=30, pady=5)


bmi_entry_i = ctk.CTkEntry(ins_tab, placeholder_text="BMI (kg/m²)")
bmi_entry_i.pack(pady=5)

weight_entry_i = ctk.CTkEntry(ins_tab, placeholder_text="Weight (kg)")
height_entry_i = ctk.CTkEntry(ins_tab, placeholder_text="Height (m)")

waist_entry_i = ctk.CTkEntry(ins_tab, placeholder_text="Waist Circumference (cm)")
waist_entry_i.pack(pady=5)
glucose_entry = ctk.CTkEntry(ins_tab, placeholder_text="Fasting Glucose (mg/dL)")
glucose_entry.pack(pady=5)
insulin_entry = ctk.CTkEntry(ins_tab, placeholder_text="Fasting Insulin (µU/mL)")
insulin_entry.pack(pady=5)


ins_result_label = ctk.CTkLabel(ins_tab, text="", font=("Poppins Bold", 16))
ins_result_label.pack(pady=10)

def animate_result(label, text, color="#1B5E20"):
    label.configure(text="", text_color=color)
    def anim():
        for i in range(len(text)):
            label.configure(text=text[:i+1])
            time.sleep(0.02)
    threading.Thread(target=anim).start()

def calc_insulin():
    try:
        if bmi_mode_i.get() == "bmi":
            bmi = float(bmi_entry_i.get())
        else:
            weight = float(weight_entry_i.get())
            height = float(height_entry_i.get())
            bmi = weight/(height**2)
        waist = float(waist_entry_i.get())
        glucose = float(glucose_entry.get())
        insulin = float(insulin_entry.get())
        homa_ir = (glucose*insulin)/405
        if homa_ir < 2.5:
            msg = "✅ Healthy insulin sensitivity"
            color = "#1B5E20"  # Green
        elif homa_ir < 4:
            msg = "⚠️ Early insulin resistance risk"
            color = "#FF8C00"  # Orange
        else:
            msg = "❌ High insulin resistance — consult doctor"
            color = "#B22222"  # Red
        animate_result(ins_result_label, f"HOMA-IR: {homa_ir:.2f}\n{msg}", color)
    except:
        messagebox.showerror("Error", "Enter valid numbers!")

calc_btn_i = ctk.CTkButton(ins_tab, text="Calculate", command=calc_insulin)
calc_btn_i.pack(pady=5)


fli_tab = tabview.tab("Fatty Liver Index")
ctk.CTkLabel(fli_tab, text="Fatty Liver Index Calculator", font=("Poppins Bold", 18)).pack(pady=10)

bmi_mode_f = ctk.StringVar(value="bmi")
def switch_mode_f():
    if bmi_mode_f.get() == "bmi":
        bmi_entry_f.pack(pady=5)
        weight_entry_f.pack_forget()
        height_entry_f.pack_forget()
    else:
        bmi_entry_f.pack_forget()
        weight_entry_f.pack(pady=5)
        height_entry_f.pack(pady=5)

ctk.CTkRadioButton(fli_tab, text="Enter BMI", variable=bmi_mode_f, value="bmi", command=switch_mode_f).pack(side="left", padx=30, pady=5)
ctk.CTkRadioButton(fli_tab, text="Enter Height & Weight", variable=bmi_mode_f, value="hw", command=switch_mode_f).pack(side="left", padx=30, pady=5)

bmi_entry_f = ctk.CTkEntry(fli_tab, placeholder_text="BMI (kg/m²)")
bmi_entry_f.pack(pady=5)

weight_entry_f = ctk.CTkEntry(fli_tab, placeholder_text="Weight (kg)")
height_entry_f = ctk.CTkEntry(fli_tab, placeholder_text="Height (m)")

waist_entry_f = ctk.CTkEntry(fli_tab, placeholder_text="Waist Circumference (cm)")
waist_entry_f.pack(pady=5)
trig_entry = ctk.CTkEntry(fli_tab, placeholder_text="Triglycerides (mg/dL)")
trig_entry.pack(pady=5)
ggt_entry = ctk.CTkEntry(fli_tab, placeholder_text="GGT (U/L)")
ggt_entry.pack(pady=5)

fli_result_label = ctk.CTkLabel(fli_tab, text="", font=("Poppins Bold", 16))
fli_result_label.pack(pady=10)

def calc_fli():
    try:
        if bmi_mode_f.get() == "bmi":
            bmi = float(bmi_entry_f.get())
        else:
            weight = float(weight_entry_f.get())
            height = float(height_entry_f.get())
            bmi = weight/(height**2)
        waist = float(waist_entry_f.get())
        trig = float(trig_entry.get())
        ggt = float(ggt_entry.get())
        L = 0.953*np.log(trig)+0.139*bmi+0.718*np.log(ggt)+0.053*waist-15.745
        fli = (np.exp(L)/(1+np.exp(L)))*100
        if fli < 30:
            msg = "✅ Fatty liver unlikely"
            color = "#1B5E20"
        elif fli < 60:
            msg = "⚠️ Moderate fatty liver risk"
            color = "#FF8C00"
        else:
            msg = "❌ High probability of fatty liver"
            color = "#B22222"
        animate_result(fli_result_label, f"FLI: {fli:.2f}\n{msg}", color)
    except:
        messagebox.showerror("Error", "Enter valid numbers!")

calc_btn_f = ctk.CTkButton(fli_tab, text="Calculate", command=calc_fli)
calc_btn_f.pack(pady=5)


def save_pdf():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
    if file_path:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0,10,"Health Risk Report", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0,10,f"HOMA-IR Results:\n{ins_result_label.cget('text')}\n\n")
        pdf.multi_cell(0,10,f"FLI Results:\n{fli_result_label.cget('text')}\n\n")
        pdf.output(file_path)
        messagebox.showinfo("PDF Saved", f"Report saved at {file_path}")

pdf_btn = ctk.CTkButton(app, text="Download PDF Report", command=save_pdf)
pdf_btn.pack(pady=10)

switch_mode_i()
switch_mode_f()

app.mainloop()
