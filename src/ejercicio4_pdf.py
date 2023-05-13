import pandas as pd
import plotly.express as px
from fpdf import FPDF
import dataframe_image as dfi
from pandas import option_context

import ejercicio1
import ejercicio2
import ejercicio3
import ejercicio5_regresionLineal

def f():
    e1_top_vuln, e1_top_ip = ejercicio1.analysis()
    dfi.export(e1_top_vuln, "data/e1_top_vuln_2_pdf.png")
    e1_top_ip.index.name = None
    e1_top_ip = e1_top_ip.head(10)
    dfi.export(e1_top_ip, "data/e1_top_ip_2_pdf.png")
    e2 = ejercicio2.top_per()
    dfi.export(e2, "data/e2_2_pdf.png")
    e3 = ejercicio3.f()
    e3 = e3.head(10)
    with option_context('display.max_colwidth', 35):
        dfi.export(e3, "data/e3_2_pdf.png")

    e5_reg_lin = ejercicio5_regresionLineal.create_image()


    # margin = 10
    # page width = 210
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('arial', 'B', 24)
    pdf.cell(w=0, h=24, txt="Ejercicio 4: Informe", ln=1)
    pdf.set_font('arial', '', 12)
    pdf.cell(w=0, h=12, txt="Los dispositivos mas vulnerables:", ln=1)
    pdf.image("data/e1_top_vuln_2_pdf.png")
    pdf.cell(w=0, h=12, txt="Las IPs de origen mas problematicas", ln=1)
    pdf.image("data/e1_top_ip_2_pdf.png")
    pdf.add_page()
    pdf.cell(w=0, h=12, txt="Top dispositivos peligrosos", ln=1)
    pdf.image("data/e2_2_pdf.png")
    pdf.cell(w=0, h=12, txt="Los 10 vulnerabilidades mas recientes", ln=1)
    pdf.image("data/e3_2_pdf.png")
    pdf.add_page()
    pdf.cell(w=0, h=12, txt="Regresion Lineal de dispositivos", ln=1)
    pdf.image(e5_reg_lin, w=190)

    pdf.output("data/ejercicio_4_pdf.pdf")
    return "data/ejercicio_4_pdf.pdf"

#f()