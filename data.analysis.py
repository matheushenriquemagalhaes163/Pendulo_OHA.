import numpy
import pandas
from matplotlib import pyplot
from scipy.optimize import curve_fit


# ==============================
#  DEFINIÇÕES E AJUSTES
# ==============================


# MASSA DO PÊNDULO (EM kg) - INSIRA AQUI SEU VALOR REAL
MASSA = 0.27  # <-- TROQUE ESTE VALOR SE NECESSÁRIO


# Função do Oscilador Harmônico Amortecido (OHA)
def oha(t, A, b, w, p):
    # x(t) = A * e^(-b*t / (2*m)) * cos(w*t - p)
    return A * numpy.exp((-b * t) / (2 * MASSA)) * numpy.cos(w * t - p)




# ==============================
#  LEITURA DOS DADOS EXPERIMENTAIS
# ==============================
data = pandas.read_csv('dados.csv', header=None)
t = data[0]  # tempo (s)
x = data[1]  # posição (m)


# CENTRALIZAÇÃO DOS DADOS (remove deslocamento médio)
x_centralizado = x - x.mean()




# ==============================
#  AJUSTE DE CURVA
# ==============================
# curve_fit encontra os parâmetros ideais A, b, w e p
popt, pcov = curve_fit(oha, t, x_centralizado)


# ==============================
#  GRÁFICO
# ==============================
fig, ax = pyplot.subplots(figsize=(10, 7))


pyplot.plot(t, x_centralizado, 'bo', ms=2, label='Pontos amostrais (centralizados)')
pyplot.plot(t, oha(t, *popt), 'r', lw=2, label='Ajuste teórico (curve fit)')


pyplot.title('Oscilador Harmônico Amortecido - x(t)')
pyplot.xlabel('Tempo (s)')
pyplot.ylabel('Deslocamento x (m)')
pyplot.legend(loc='best')
pyplot.grid(True)




# ==============================
#  CÁLCULOS COMPLEMENTARES
# ==============================
A, b, w, p = popt
w0 = numpy.sqrt(w**2 + (b / (2*MASSA))**2)  # frequência natural não amortecida
Q = 1 / (1 - numpy.exp(-2*b*2*numpy.pi / w))  # fator de qualidade estimado


# ==============================
#  SALVA RESULTADOS
# ==============================
with open('parametros_eq.txt', 'w', encoding='utf-8') as par:
    par.write(f"A = {A}\n")
    par.write(f"b = {b}\n")
    par.write(f"w = {w}\n")
    par.write(f"w0 = {w0}\n")
    par.write(f"Fator de qualidade Q = {Q}\n")


print(f"Fator de qualidade Q = {Q}")
print(f"Frequência amortecida ω = {w} rad/s")
print(f"Frequência natural ω₀ = {w0} rad/s")


pyplot.show()
