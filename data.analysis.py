import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

# ------------------------------
# VALORES EXPERIMENTAIS
# ------------------------------
m = 0.27       # massa em kg
L = 0.56       # comprimento do fio em metros
g = 9.81       # aceleração da gravidade em m/s²

# ------------------------------
# FUNÇÃO DO OHA COM AMORTECIMENTO
# x(t) = A * exp(-b*t/(2*m)) * cos(w*t - phi)
# ------------------------------
def oha(t, a, b, w, phi):
    return a * np.exp(-b*t/(2*m)) * np.cos(w*t - phi)

# ------------------------------
# LEITURA DOS DADOS
# ------------------------------
# Se t estiver em frames, converta para segundos usando FPS
# Exemplo: t = frame_number / FPS
data = pd.read_csv('dados.csv', header=None)
t = data[0].values  # tempo em segundos
x = data[1].values  # posição em metros

# ------------------------------
# PALPITES INICIAIS PARA O AJUSTE
# ------------------------------
A_guess = max(x)
b_guess = 0.1
w_guess = np.sqrt(g / L)  # frequência aproximada do pêndulo
phi_guess = 0
p0 = [A_guess, b_guess, w_guess, phi_guess]

# ------------------------------
# AJUSTE DA CURVA
# ------------------------------
popt, pcov = curve_fit(oha, t, x, p0=p0)
A_fit, b_fit, w_fit, phi_fit = popt

# Frequência teórica do pêndulo simples
omega0 = np.sqrt(g / L)

# Fator de qualidade simplificado
Q = w_fit / b_fit

# ------------------------------
# PLOT DOS RESULTADOS
# ------------------------------
plt.figure(figsize=(10,7))
plt.plot(t, x, 'bo', ms=2, label='Pontos amostrais')
plt.plot(t, oha(t, *popt), 'r-', label='Ajuste OHA')
plt.title('Oscilação do Pêndulo')
plt.xlabel('Tempo t (s)')
plt.ylabel('Posição x (m)')
plt.legend()
plt.grid(True)
plt.show()

# ------------------------------
# SALVANDO PARÂMETROS EM ARQUIVO
# ------------------------------
with open('parametros_eq.txt', 'w') as par:
    par.write(f"A = {A_fit:.5f} m\n")
    par.write(f"b = {b_fit:.5f} kg/s\n")
    par.write(f"w = {w_fit:.5f} rad/s\n")
    par.write(f"phi = {phi_fit:.5f} rad\n")
    par.write(f"Frequência teórica w0 = {omega0:.5f} rad/s\n")
    par.write(f"Fator de qualidade Q = {Q:.5f}\n")

# ------------------------------
# PRINT NO TERMINAL
# ------------------------------
print("------ RESULTADOS ------")
print(f"A = {A_fit:.5f} m")
print(f"b = {b_fit:.5f} kg/s")
print(f"w = {w_fit:.5f} rad/s")
print(f"phi = {phi_fit:.5f} rad")
print(f"Frequência teórica w0 = {omega0:.5f} rad/s")
print(f"Fator de qualidade Q = {Q:.5f}")
