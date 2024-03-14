import pandas as pd

# Lire les fichiers CSV pour chaque type d'information
meps_data = pd.read_csv("meps.csv")
meps_info_data = pd.read_csv("meps_information.csv")
meps_vote_data = pd.read_csv("meps_vote_information.csv")
european_procedures_data = pd.read_csv("european_procedures.csv")

# Fusionner les données en fonction des clés de relation appropriées
# Assurez-vous d'avoir des colonnes de clés communes entre les fichiers pour effectuer la fusion
merged_data = pd.merge(meps_data, meps_info_data, on="key_column")
merged_data = pd.merge(merged_data, meps_vote_data, on="key_column")
merged_data = pd.merge(merged_data, european_procedures_data, on="key_column")

# Exporter les données fusionnées vers un fichier CSV
merged_data.to_csv("merged_data.csv", index=False)

meps_data <- pd.read_csv("chemin_absolu/meps.csv")

