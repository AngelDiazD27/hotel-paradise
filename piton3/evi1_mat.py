import matplotlib.pyplot as plt

"""Datos organizados"""
data = {
    "roles": (['Rol1', 'Rol2', 'Rol3'], [3500, 5600, 6800]),
    "industrias": (['Tecnología', 'Finanzas', 'Salud', 'Retail'], [30, 25, 20, 25]),
    "años": (['2017', '2018', '2019', '2020', '2021'], [3.0, 3.5, 4.2, 4.8, 5.5])
}

fig, axs = plt.subplots(1, 3, figsize=(12, 4))

"""Grafica de barras"""
axs[0].bar(*data["roles"], color=['blue', 'green', 'orange'])
axs[0].set_title('Compensación Promedio por Rol')
axs[0].set_xlabel('Rol')
axs[0].set_ylabel('Compensación Promedio (USD)')

"""Grafica de pastel"""
axs[1].pie(
    data["industrias"][1],
    labels=data["industrias"][0],
    autopct='%1.0f%%',
    colors=['blue', 'green', 'orange', 'purple']
)
axs[1].set_title('Horas Trabajadas por Industria')

"""Grafica de líneas"""
axs[2].plot(*data["años"], marker='o', color='blue')
axs[2].set_title('Evolución de Antigüedad')
axs[2].set_xlabel('Año')
axs[2].set_ylabel('Antigüedad Promedio (años)')

plt.tight_layout()
plt.show()
