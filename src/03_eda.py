import pandas as pd

df = pd.read_csv("data/wec_clean.csv", low_memory=False)

df["hour_numeric"] = pd.to_datetime(df["hour"], format="%H:%M:%S.%f").dt.hour + pd.to_datetime(df["hour"], format="%H:%M:%S.%f").dt.minute / 60
df["chuva"] = df["precipitation"] > 0

print("=" * 60)
print("ANÁLISE EXPLORATÓRIA (EDA)")
print("=" * 60)

print("\n--- Estatísticas descritivas ---")
print(df[["lap_time_s", "temperature", "precipitation", "windspeed"]].describe().round(2))

# ============================================================
# ANÁLISE POR CIRCUITO
# ============================================================

cols = ["lap_time_s", "hour_numeric", "temperature", "precipitation", "windspeed"]

for circuito, grupo in df.groupby("circuit"):
    print(f"\n{'=' * 40}")
    print(f"CIRCUITO: {circuito}")
    print(f"{'=' * 40}")

    print(f"  Voltas totais: {len(grupo)}")
    print(f"  Temperatura média: {grupo['temperature'].mean():.1f}°C")
    print(f"  Voltas com chuva: {grupo['chuva'].sum()} ({grupo['chuva'].mean()*100:.1f}%)")

    print("\n  Correlações com lap_time_s:")
    print(grupo[cols].corr()["lap_time_s"].drop("lap_time_s").round(3).to_string())

    if grupo["chuva"].any():
        print("\n  Seco vs Chuva:")
        print(grupo.groupby("chuva")["lap_time_s"].agg(["mean", "count"]).round(2))