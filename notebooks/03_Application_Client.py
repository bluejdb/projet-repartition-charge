#!/usr/bin/env python
# coding: utf-8

# # 03 – Application Client / Pipeline
# 
# Ce notebook transforme tout le travail de nettoyage et d’agrégation
# en un pipeline automatisé, réutilisable par un responsable de l’organisation.
# 
# L’objectif :
# - charger les données brutes,
# - appliquer un nettoyage complet,
# - calculer les indicateurs,
# - produire les agrégations par centre, phase et module,
# - exporter un fichier final exploitable dans Tableau.
# 
# Ce pipeline pourra être transformé en script .py et éventuellement en .exe.
# 

# In[1]:


import pandas as pd
import numpy as np


# # DÉFINITION DES FONCTIONS DU PIPELINE

# In[2]:


def load_data(filepath=r"C:\Users\Tenordem\Documents\projet-repartition-charge\data\raw\data_complet_v2.xlsx"):
    df = pd.read_excel(filepath)
    return df


# In[3]:


def clean_data(df):
    # Standardisation textes
    for col in ["Centre", "NOM_SI", "Types_phases", "utilisateur_id2"]:
        df[col] = df[col].astype(str).str.strip().str.upper()

    # Nettoyage centres
    df["Centre"] = df["Centre"].replace({
        "-": "INCONNU",
        "NAN": "INCONNU",
        "DEMO1": "INCONNU"
    })
    
    # Nettoyage phases
    df["Types_phases"] = df["Types_phases"].replace({
        "-": "INCONNU"
    })
    
    # Nettoyage charges
    for col in ["ChargeTotaleEstimee", "ChargeTotaleActualisee"]:
        df[col] = df[col].replace("-", np.nan)
        df[col] = df[col].replace("", np.nan)
        df[col] = df[col].astype(str).str.replace(",", ".", regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remplacement NaN charges
    df["ChargeTotaleEstimee"] = df["ChargeTotaleEstimee"].fillna(0)
    df["ChargeTotaleActualisee"] = df["ChargeTotaleActualisee"].fillna(0)
        
    # Nettoyage postes
    df["utilisateur_id2"] = df["utilisateur_id2"].replace("-", "INCONNU")
    
    return df


# In[4]:


def compute_indicators(df):
    df["EcartCharge"] = df["ChargeTotaleActualisee"] - df["ChargeTotaleEstimee"]
    
    df["TauxSurcharge"] = np.where(
        (df["ChargeTotaleEstimee"] == 0) & (df["ChargeTotaleActualisee"] == 0),
        0,
        np.where(
            df["ChargeTotaleEstimee"] == 0,
            np.nan,
            df["ChargeTotaleActualisee"] / df["ChargeTotaleEstimee"]
        )
    )
    
    df["TauxSurcharge_%"] = df["TauxSurcharge"] * 100
    return df


# In[5]:


def build_aggregations(df):
    
    # Par centre
    agg_centre = (
        df.groupby("Centre", as_index=False)
          .agg(
              ChargeEstimee=("ChargeTotaleEstimee", "sum"),
              ChargeReelle=("ChargeTotaleActualisee", "sum"),
              NbPostes=("utilisateur_id2", "nunique")
          )
    )
    agg_centre["TauxSurcharge"] = np.where(
        (agg_centre["ChargeEstimee"] == 0) & (agg_centre["ChargeReelle"] == 0),
        0,
        np.where(
            agg_centre["ChargeEstimee"] == 0,
            np.nan,
            agg_centre["ChargeReelle"] / agg_centre["ChargeEstimee"]
        )
    )
    agg_centre["TauxSurcharge_%"] = agg_centre["TauxSurcharge"] * 100
    
    # Par phase
    agg_phase = (
        df.groupby("Types_phases", as_index=False)
          .agg(
              ChargeEstimee=("ChargeTotaleEstimee", "sum"),
              ChargeReelle=("ChargeTotaleActualisee", "sum")
          )
    )
    agg_phase["TauxSurcharge"] = np.where(
        (agg_phase["ChargeEstimee"] == 0) & (agg_phase["ChargeReelle"] == 0),
        0,
        np.where(
            agg_phase["ChargeEstimee"] == 0,
            np.nan,
            agg_phase["ChargeReelle"] / agg_phase["ChargeEstimee"]
        )
    )
    agg_phase["TauxSurcharge_%"] = agg_phase["TauxSurcharge"] * 100
    
    # Par module
    agg_module = (
        df.groupby("NOM_SI", as_index=False)
          .agg(
              ChargeEstimee=("ChargeTotaleEstimee", "sum"),
              ChargeReelle=("ChargeTotaleActualisee", "sum"),
              NbPostes=("utilisateur_id2", "nunique")
          )
    )
    agg_module["TauxSurcharge"] = np.where(
        (agg_module["ChargeEstimee"] == 0) & (agg_module["ChargeReelle"] == 0),
        0,
        np.where(
            agg_module["ChargeEstimee"] == 0,
            np.nan,
            agg_module["ChargeReelle"] / agg_module["ChargeEstimee"]
        )
    )
    agg_module["TauxSurcharge_%"] = agg_module["TauxSurcharge"] * 100
    
    # Centre × Phase
    agg_centre_phase = (
        df.groupby(["Centre", "Types_phases"], as_index=False)
          .agg(
              ChargeEstimee=("ChargeTotaleEstimee", "sum"),
              ChargeReelle=("ChargeTotaleActualisee", "sum")
          )
    )
    agg_centre_phase["TauxSurcharge"] = np.where(
        (agg_centre_phase["ChargeEstimee"] == 0) & (agg_centre_phase["ChargeReelle"] == 0),
        0,
        np.where(
            agg_centre_phase["ChargeEstimee"] == 0,
            np.nan,
            agg_centre_phase["ChargeReelle"] / agg_centre_phase["ChargeEstimee"]
        )
    )
    agg_centre_phase["TauxSurcharge_%"] = agg_centre_phase["TauxSurcharge"] * 100
    
    # Module × Phase
    agg_module_phase = (
        df.groupby(["NOM_SI", "Types_phases"], as_index=False)
          .agg(
              ChargeEstimee=("ChargeTotaleEstimee", "sum"),
              ChargeReelle=("ChargeTotaleActualisee", "sum")
          )
    )
    agg_module_phase["TauxSurcharge"] = np.where(
        (agg_module_phase["ChargeEstimee"] == 0) & (agg_module_phase["ChargeReelle"] == 0),
        0,
        np.where(
            agg_module_phase["ChargeEstimee"] == 0,
            np.nan,
            agg_module_phase["ChargeReelle"] / agg_module_phase["ChargeEstimee"]
        )
    )
    agg_module_phase["TauxSurcharge_%"] = agg_module_phase["TauxSurcharge"] * 100
    
    return agg_centre, agg_phase, agg_module, agg_centre_phase, agg_module_phase


# In[7]:


def export_data(agg_centre, agg_phase, agg_module, agg_centre_phase, agg_module_phase,
                filepath=(r"C:\Users\Tenordem\Documents\projet-repartition-charge\data\processed\data_aggregations.xlsx")):
    
    with pd.ExcelWriter(filepath) as writer:
        agg_centre.to_excel(writer, sheet_name="par_centre", index=False)
        agg_phase.to_excel(writer, sheet_name="par_phase", index=False)
        agg_module.to_excel(writer, sheet_name="par_module", index=False)
        agg_centre_phase.to_excel(writer, sheet_name="par_centre_phase", index=False)
        agg_module_phase.to_excel(writer, sheet_name="par_module_phase", index=False)


# # PIPELINE PRINCIPAL (main)

# In[8]:


df = load_data()
df = clean_data(df)
df = compute_indicators(df)

agg_centre, agg_phase, agg_module, agg_centre_phase, agg_module_phase = build_aggregations(df)

export_data(agg_centre, agg_phase, agg_module, agg_centre_phase, agg_module_phase)

print("Pipeline terminé. Fichier exporté dans data/processed/data_aggregations.xlsx")


# In[ ]:




