import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv("data/wec_clean.csv", low_memory=False)
os.makedirs("plots", exist_ok=True)
sns.set_theme(style="whitegrid")

df["hour_numeric"] = pd.to_datetime(df["hour"], format="%H:%M:%S.%f").dt.hour + pd.to_datetime(df["hour"], format="%H:%M:%S.%f").dt.minute / 60
df["chuva"] = df["precipitation"] > 0
df["Condição"] = df["chuva"].map({True: "Chuva", False: "Seco"})

# --- Gráfico 1: Heatmap de correlações globais ---
cols = ["lap_time_s", "temperature", "precipitation", "windspeed", "hour_numeric"]
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(df[cols].corr().round(2), annot=True, fmt=".2f",
            cmap="coolwarm", linewidths=0.5, ax=ax)
ax.set_title("Heatmap de Correlações — Clima vs Tempos de Volta", fontweight="bold")
plt.tight_layout()
plt.savefig("plots/01_heatmap_correlacoes.png")
plt.close()

# --- Gráfico 2: Scatter temperatura vs lap_time por circuito ---
circuitos = df["circuit"].unique()
n = len(circuitos)
fig, axes = plt.subplots(2, (n + 1) // 2, figsize=(16, 10))
axes = axes.flatten()
for i, circuito in enumerate(circuitos):
    sub = df[df["circuit"] == circuito]
    axes[i].scatter(sub["temperature"], sub["lap_time_s"], alpha=0.2, s=8, color="steelblue")
    axes[i].set_title(circuito[:25], fontweight="bold", fontsize=9)
    axes[i].set_xlabel("Temperatura (°C)", fontsize=8)
    axes[i].set_ylabel("Lap Time (s)", fontsize=8)
for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)
plt.suptitle("Temperatura vs Tempo de Volta por Circuito", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("plots/02_scatter_temperatura_por_circuito.png")
plt.close()

# --- Gráfico 3: Scatter vento vs lap_time por circuito ---
fig, axes = plt.subplots(2, (n + 1) // 2, figsize=(16, 10))
axes = axes.flatten()
for i, circuito in enumerate(circuitos):
    sub = df[df["circuit"] == circuito]
    axes[i].scatter(sub["windspeed"], sub["lap_time_s"], alpha=0.2, s=8, color="darkorange")
    axes[i].set_title(circuito[:25], fontweight="bold", fontsize=9)
    axes[i].set_xlabel("Vento (kph)", fontsize=8)
    axes[i].set_ylabel("Lap Time (s)", fontsize=8)
for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)
plt.suptitle("Velocidade do Vento vs Tempo de Volta por Circuito", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("plots/03_scatter_vento_por_circuito.png")
plt.close()

# --- Gráfico 4: Boxplot seco vs chuva por circuito ---
circuitos_com_chuva = df[df["Condição"] == "Chuva"]["circuit"].unique()
df_chuva = df[df["circuit"].isin(circuitos_com_chuva)]
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=df_chuva, x="circuit", y="lap_time_s", hue="Condição",
            palette=["steelblue", "salmon"], ax=ax)
ax.set_title("Tempos de Volta: Seco vs Chuva por Circuito", fontweight="bold")
ax.set_xlabel("Circuito")
ax.set_ylabel("Tempo de Volta (segundos)")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("plots/04_boxplot_seco_chuva_por_circuito.png")
plt.close()

# --- Gráfico 5: Evolução da temperatura ao longo das corridas ---
fig, axes = plt.subplots(2, (n + 1) // 2, figsize=(16, 10))
axes = axes.flatten()
for i, circuito in enumerate(circuitos):
    sub = df[df["circuit"] == circuito].sort_values("hour_numeric")
    temp_hora = sub.groupby("hour_numeric")["temperature"].mean()
    axes[i].plot(temp_hora.index, temp_hora.values, color="tomato", linewidth=1.5)
    axes[i].set_title(circuito[:25], fontweight="bold", fontsize=9)
    axes[i].set_xlabel("Hora da Corrida", fontsize=8)
    axes[i].set_ylabel("Temperatura (°C)", fontsize=8)
for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)
plt.suptitle("Evolução da Temperatura ao Longo das Corridas", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("plots/05_temperatura_por_hora.png")
plt.close()

print("✅ 5 gráficos guardados na pasta plots/")