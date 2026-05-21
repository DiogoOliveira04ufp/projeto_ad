import pandas as pd
import numpy as np

# ============================================================
# CARREGAR OS DADOS
# ============================================================

df_wec = pd.read_csv("data/2012-2022_FIA_WEC_FULL_LAP_DATA.csv", low_memory=False)
df_weather = pd.read_csv("data/weather.csv")

# Strings vazias → NaN
df_wec.replace("", pd.NA, inplace=True)

# ============================================================
# LIMPEZA DO WEC
# ============================================================

# Remover duplicados
df_wec.drop_duplicates(inplace=True)

# Colunas com significado próprio no vazio
df_wec["crossing_finish_line_in_pit"] = df_wec["crossing_finish_line_in_pit"].fillna("No Pit")
df_wec["pit_time"] = df_wec["pit_time"].fillna(0)
df_wec["group"] = df_wec["group"].fillna("N/A")
df_wec["flag_at_fl"] = df_wec["flag_at_fl"].fillna("UNKNOWN")

# top_speed → imputar com a média
df_wec["top_speed"] = df_wec["top_speed"].fillna(df_wec["top_speed"].mean())

# Remover linhas sem tempo de volta
df_wec.dropna(subset=["lap_time_s"], inplace=True)

# Remover voltas com pit stop (distorcem os tempos)
df_wec = df_wec[df_wec["crossing_finish_line_in_pit"] == "No Pit"]

# Remover outliers extremos de lap_time_s via IQR
Q1 = df_wec["lap_time_s"].quantile(0.25)
Q3 = df_wec["lap_time_s"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
df_wec = df_wec[(df_wec["lap_time_s"] >= lower) & (df_wec["lap_time_s"] <= upper)]

# Remover classe com poucos dados
df_wec = df_wec[df_wec["class"] != "INNOVATIVE CAR"]

# ============================================================
# MERGE COM WEATHER
# ============================================================

df_wec = df_wec[df_wec["season"].isin(["2021", "2022", 2021, 2022])]

df_wec["season"] = df_wec["season"].astype(int)
df_wec["round"] = df_wec["round"].astype(int)
df_weather["season"] = df_weather["season"].astype(int)
df_weather["round"] = df_weather["round"].astype(int)

df_merged = pd.merge(df_wec, df_weather, on=["season", "round", "circuit"], how="left")

print(f"Linhas após merge: {len(df_merged)}")
print(f"Colunas após merge: {len(df_merged.columns)}")

# ============================================================
# GUARDAR
# ============================================================

df_merged.to_csv("data/wec_clean.csv", index=False)
print("✅ Dataset limpo guardado em: data/wec_clean.csv")