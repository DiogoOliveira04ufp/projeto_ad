import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv("data/wec_clean.csv", low_memory=False)
os.makedirs("plots", exist_ok=True)
sns.set_theme(style="whitegrid")

# --- Gráfico 1: Histograma de lap_time_s ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df["lap_time_s"], bins=60, color="steelblue", edgecolor="white")
ax.set_title("Distribuição dos Tempos de Volta", fontweight="bold")
ax.set_xlabel("Tempo de Volta (segundos)")
ax.set_ylabel("Número de Voltas")
plt.tight_layout()
plt.savefig("plots/01_histograma_lap_time.png")
plt.close()

# --- Gráfico 2: Bar chart — tempo médio por fabricante ---
media = df.groupby("manufacturer")["lap_time_s"].mean().sort_values()
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(media.index, media.values, color="steelblue")
ax.set_title("Tempo Médio de Volta por Fabricante", fontweight="bold")
ax.set_xlabel("Tempo Médio (segundos)")
for bar, val in zip(bars, media.values):
    ax.text(val + 0.5, bar.get_y() + bar.get_height() / 2, f"{val:.1f}s", va="center", fontsize=9)
plt.tight_layout()
plt.savefig("plots/02_barras_fabricante.png")
plt.close()

# --- Gráfico 3: Scatter — temperatura vs lap_time_s ---
fig, ax = plt.subplots(figsize=(10, 6))
classes = df["class"].unique()
cores = sns.color_palette("tab10", len(classes))
for classe, cor in zip(classes, cores):
    sub = df[df["class"] == classe]
    ax.scatter(sub["temperature"], sub["lap_time_s"], label=classe, alpha=0.3, s=10, color=cor)
ax.set_title("Temperatura vs Tempo de Volta por Classe", fontweight="bold")
ax.set_xlabel("Temperatura (°C)")
ax.set_ylabel("Tempo de Volta (segundos)")
ax.legend(title="Classe", markerscale=2)
plt.tight_layout()
plt.savefig("plots/03_scatter_temperatura_laptime.png")
plt.close()

# --- Gráfico 4: Boxplot — lap_time_s com e sem chuva ---
df["Condição"] = df["precipitation"].apply(lambda x: "Chuva" if x > 0 else "Seco")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df, x="Condição", y="lap_time_s", palette=["steelblue", "salmon"], ax=ax)
ax.set_title("Tempos de Volta: Seco vs Chuva", fontweight="bold")
ax.set_ylabel("Tempo de Volta (segundos)")
plt.tight_layout()
plt.savefig("plots/04_boxplot_chuva_seco.png")
plt.close()

# --- Gráfico 5: Heatmap de correlações ---
cols = ["lap_time_s", "top_speed", "kph", "temperature", "precipitation", "windspeed"]
fig, ax = plt.subplots(figsize=(9, 7))
sns.heatmap(df[cols].corr().round(2), annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, ax=ax)
ax.set_title("Heatmap de Correlações", fontweight="bold")
plt.tight_layout()
plt.savefig("plots/05_heatmap_correlacoes.png")
plt.close()

print("✅ 5 gráficos guardados na pasta plots/")