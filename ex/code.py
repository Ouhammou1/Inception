# %% [markdown]
# # Arbres de Décision - Fondements Mathématiques
# 
# ## 1. Importation des Bibliothèques
# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import math

# %% [markdown]
# ## 2. Fonctions Mathématiques de Base
# 
# ### 2.1 Calcul de l'Entropie
# %%
def calcul_entropie(labels):
    """
    Calcule l'entropie de Shannon d'un ensemble de labels
    
    Formule : H(S) = -∑ p_i * log₂(p_i)
    """
    n = len(labels)
    if n == 0:
        return 0
    
    # Calcul des proportions
    proportions = np.bincount(labels) / n
    
    # Éviter log(0)
    proportions = proportions[proportions > 0]
    
    # Calcul de l'entropie
    entropie = -np.sum(proportions * np.log2(proportions))
    
    return entropie

# Test de la fonction
test_labels = np.array([0, 0, 0, 1, 1, 1])
print(f"Entropie de l'ensemble test [0,0,0,1,1,1]: {calcul_entropie(test_labels):.4f}")

# %% [markdown]
# ### 2.2 Calcul de l'Impureté de Gini
# %%
def calcul_gini(labels):
    """
    Calcule l'impureté de Gini d'un ensemble de labels
    
    Formule : G(S) = 1 - ∑ p_i²
    """
    n = len(labels)
    if n == 0:
        return 0
    
    proportions = np.bincount(labels) / n
    gini = 1 - np.sum(proportions ** 2)
    
    return gini

# Test
print(f"Gini de l'ensemble test: {calcul_gini(test_labels):.4f}")

# %% [markdown]
# ### 2.3 Calcul du Gain d'Information
# %%
def gain_information(labels_parent, labels_enfants):
    """
    Calcule le gain d'information après une division
    
    Formule : Gain = Entropie(parent) - ∑ (|S_v|/|S|) * Entropie(S_v)
    """
    n_parent = len(labels_parent)
    entropie_parent = calcul_entropie(labels_parent)
    
    # Initialiser le gain
    gain = entropie_parent
    n_total = 0
    
    for labels_enfant in labels_enfants:
        n_enfant = len(labels_enfant)
        if n_enfant > 0:
            gain -= (n_enfant / n_parent) * calcul_entropie(labels_enfant)
        n_total += n_enfant
    
    return gain

# %% [markdown]
# ## 3. Exemple Pratique avec Iris Dataset
# %%
# Chargement des données
iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
class_names = iris.target_names

# Création d'un DataFrame pour analyse
df_iris = pd.DataFrame(X, columns=feature_names)
df_iris['target'] = y
df_iris['species'] = [class_names[i] for i in y]

print("=== Dataset Iris ===")
print(f"Nombre d'échantillons: {len(df_iris)}")
print(f"Nombre de features: {len(feature_names)}")
print(f"Classes: {class_names}")
print("\nPremières lignes:")
print(df_iris.head())

# %% [markdown]
# ## 4. Visualisation des Distributions
# %%
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
features = feature_names[:4]

for idx, feature in enumerate(features):
    ax = axes[idx // 2, idx % 2]
    for species in class_names:
        subset = df_iris[df_iris['species'] == species]
        ax.hist(subset[feature], alpha=0.5, label=species, bins=20)
    
    ax.set_xlabel(feature)
    ax.set_ylabel('Fréquence')
    ax.legend()
    ax.set_title(f'Distribution de {feature} par espèce')

plt.tight_layout()
plt.show()

# %% [markdown]
# ## 5. Calcul Manuel d'une Division Optimale
# %%
def trouver_meilleure_division(X, y, feature_index):
    """
    Trouve le meilleur seuil pour diviser les données sur un feature donné
    """
    valeurs = X[:, feature_index]
    labels = y
    
    # Trier les valeurs
    indices_tries = np.argsort(valeurs)
    valeurs_tries = valeurs[indices_tries]
    labels_tries = labels[indices_tries]
    
    meilleur_gain = -1
    meilleur_seuil = None
    meilleurs_labels_gauche = None
    meilleurs_labels_droite = None
    
    # Essayer tous les seuils possibles
    for i in range(1, len(valeurs_tries)):
        if valeurs_tries[i] != valeurs_tries[i-1]:
            seuil = (valeurs_tries[i] + valeurs_tries[i-1]) / 2
            
            # Séparer les labels
            labels_gauche = labels_tries[:i]
            labels_droite = labels_tries[i:]
            
            # Calculer le gain
            gain = gain_information(labels_tries, [labels_gauche, labels_droite])
            
            if gain > meilleur_gain:
                meilleur_gain = gain
                meilleur_seuil = seuil
                meilleurs_labels_gauche = labels_gauche
                meilleurs_labels_droite = labels_droite
    
    return meilleur_gain, meilleur_seuil, meilleurs_labels_gauche, meilleurs_labels_droite

# Test sur une feature
feature_idx = 0  # sepal length
gain, seuil, gauche, droite = trouver_meilleure_division(X, y, feature_idx)

print(f"=== Analyse pour {feature_names[feature_idx]} ===")
print(f"Meilleur seuil: {seuil:.2f}")
print(f"Gain d'information: {gain:.4f}")
print(f"Taille gauche: {len(gauche)}, Taille droite: {len(droite)}")
print(f"Distribution gauche: {np.bincount(gauche)}")
print(f"Distribution droite: {np.bincount(droite)}")

# %% [markdown]
# ## 6. Construction d'un Arbre de Décision avec scikit-learn
# %%
# Division des données
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Création de l'arbre avec critère d'entropie
arbre_entropie = DecisionTreeClassifier(
    criterion='entropy',
    max_depth=3,
    random_state=42
)

# Entraînement
arbre_entropie.fit(X_train, y_train)

# Prédictions
y_pred = arbre_entropie.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"=== Arbre avec critère Entropie ===")
print(f"Profondeur max: {arbre_entropie.get_depth()}")
print(f"Nombre de feuilles: {arbre_entropie.get_n_leaves()}")
print(f"Précision sur le test: {accuracy:.2%}")

# %% [markdown]
# ## 7. Visualisation de l'Arbre
# %%
plt.figure(figsize=(15, 8))
plot_tree(
    arbre_entropie,
    feature_names=feature_names,
    class_names=class_names,
    filled=True,
    rounded=True,
    fontsize=10
)
plt.title("Arbre de Décision - Iris Dataset (Entropie)")
plt.show()

# %% [markdown]
# ## 8. Matrice de Confusion
# %%
# Matrice de confusion
conf_matrix = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Prédictions')
plt.ylabel('Vraies valeurs')
plt.title('Matrice de Confusion')
plt.show()

# %% [markdown]
# ## 9. Comparaison des Critères : Entropie vs Gini
# %%
# Création d'un arbre avec critère Gini
arbre_gini = DecisionTreeClassifier(
    criterion='gini',
    max_depth=3,
    random_state=42
)
arbre_gini.fit(X_train, y_train)

# Évaluation
y_pred_gini = arbre_gini.predict(X_test)
accuracy_gini = accuracy_score(y_test, y_pred_gini)

print("=== Comparaison des Critères ===")
print(f"Entropie - Précision: {accuracy:.2%}")
print(f"Gini - Précision: {accuracy_gini:.2%}")

# %% [markdown]
# ## 10. Analyse de l'Importance des Features
# %%
importances_entropie = arbre_entropie.feature_importances_
importances_gini = arbre_gini.feature_importances_

df_importances = pd.DataFrame({
    'Feature': feature_names,
    'Importance_Entropie': importances_entropie,
    'Importance_Gini': importances_gini
}).sort_values('Importance_Entropie', ascending=False)

print("=== Importance des Features ===")
print(df_importances)

# Visualisation
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].barh(df_importances['Feature'], df_importances['Importance_Entropie'])
axes[0].set_xlabel('Importance')
axes[0].set_title('Importance des Features (Entropie)')

axes[1].barh(df_importances['Feature'], df_importances['Importance_Gini'])
axes[1].set_xlabel('Importance')
axes[1].set_title('Importance des Features (Gini)')

plt.tight_layout()
plt.show()

# %% [markdown]
# ## 11. Effet de la Profondeur Maximale
# %%
profondeurs = range(1, 10)
scores_train = []
scores_test = []

for depth in profondeurs:
    arbre = DecisionTreeClassifier(
        criterion='entropy',
        max_depth=depth,
        random_state=42
    )
    arbre.fit(X_train, y_train)
    
    scores_train.append(accuracy_score(y_train, arbre.predict(X_train)))
    scores_test.append(accuracy_score(y_test, arbre.predict(X_test)))

# Visualisation
plt.figure(figsize=(10, 6))
plt.plot(profondeurs, scores_train, 'o-', label='Train', linewidth=2)
plt.plot(profondeurs, scores_test, 's-', label='Test', linewidth=2)
plt.xlabel('Profondeur maximale')
plt.ylabel('Précision')
plt.title('Effet de la profondeur sur la performance')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# %% [markdown]
# ## 12. Exemple de Prédiction
# %%
# Création d'un exemple fictif
exemple = np.array([[5.1, 3.5, 1.4, 0.2]])  # Setosa

prediction = arbre_entropie.predict(exemple)
probabilites = arbre_entropie.predict_proba(exemple)

print("=== Prédiction pour un exemple ===")
print(f"Features: {exemple[0]}")
print(f"Classe prédite: {class_names[prediction[0]]}")
print("\nProbabilités par classe:")
for i, classe in enumerate(class_names):
    print(f"  {classe}: {probabilites[0][i]:.1%}")

# %% [markdown]
# ## 13. Fonction Interactive de Simulation
# %%
def simuler_arbre_manuel():
    """
    Simulation interactive d'un arbre de décision simple
    """
    print("\n" + "="*50)
    print("SIMULATION D'ARBRE DE DÉCISION MANUEL")
    print("="*50)
    
    # Exemple simple
    print("\nExemple: Décision 'Sortir dehors'")
    print("Features: [Température, Pluie, Humidité]")
    
    # Règles simples
    temp = float(input("\nTempérature (°C): "))
    pluie = input("Pluie? (oui/non): ").lower()
    humidite = float(input("Humidité (%): "))
    
    # Arbre de décision manuel
    decision = "Reste à la maison"
    
    if pluie == 'non':
        if temp > 20:
            if humidite < 80:
                decision = "Sortir dehors"
            else:
                decision = "Reste à la maison"
        elif temp > 15:
            decision = "Peut-être sortir"
        else:
            decision = "Reste à la maison"
    
    print(f"\nDécision: {decision}")

# Exécuter la simulation
simuler_arbre_manuel()

# %% [markdown]
# ## 14. Conclusion Mathématique
# %%
print("\n" + "="*60)
print("RÉSUMÉ MATHÉMATIQUE DES ARBRES DE DÉCISION")
print("="*60)

print("\n1. MESURES D'IMPURETÉ:")
print("   • Entropie: H(S) = -∑ p_i × log₂(p_i)")
print("   • Gini: G(S) = 1 - ∑ p_i²")
print("   • Erreur de classification: E(S) = 1 - max(p_i)")

print("\n2. GAIN D'INFORMATION:")
print("   • Gain(S, A) = Entropie(S) - ∑ (|S_v|/|S|) × Entropie(S_v)")
print("   • Gain Ratio = Gain(S, A) / SplitInfo(S, A)")

print("\n3. ALGORITHME (ID3/CART):")
print("   • Choisir l'attribut avec le gain maximal")
print("   • Diviser récursivement")
print("   • Critères d'arrêt: profondeur max, min samples, pureté")

print("\n4. COMPLEXITÉ:")
print("   • Construction: O(n × m × log(n))")
print("   • Prédiction: O(profondeur)")

# %% [markdown]
# ## 15. Exercices Pratiques
# %%
def exercice_1():
    """Exercice sur le calcul d'entropie"""
    print("\nExercice 1: Calcul d'Entropie")
    print("Calculer l'entropie pour les ensembles suivants:")
    
    ensembles = [
        ([0, 0, 0, 0, 0], "Ensemble pur classe 0"),
        ([0, 0, 0, 1, 1], "Mixte"),
        ([0, 1, 2, 0, 1, 2], "Trois classes équilibrées")
    ]
    
    for labels, description in ensembles:
        entropie = calcul_entropie(np.array(labels))
        print(f"\n{description}: {labels}")
        print(f"Entropie calculée: {entropie:.4f}")
        print(f"Théorique: {calcul_entropie(np.array(labels)):.4f}")

def exercice_2():
    """Exercice sur le gain d'information"""
    print("\n\nExercice 2: Gain d'Information")
    
    # Données d'exemple
    labels_parent = np.array([0, 0, 0, 1, 1, 1])
    labels_gauche = np.array([0, 0, 0])
    labels_droite = np.array([1, 1, 1])
    
    gain = gain_information(labels_parent, [labels_gauche, labels_droite])
    
    print(f"Parent: {labels_parent}")
    print(f"Gauche: {labels_gauche}")
    print(f"Droite: {labels_droite}")
    print(f"\nEntropie parent: {calcul_entropie(labels_parent):.4f}")
    print(f"Entropie gauche: {calcul_entropie(labels_gauche):.4f}")
    print(f"Entropie droite: {calcul_entropie(labels_droite):.4f}")
    print(f"\nGain d'information: {gain:.4f}")

# Exécution des exercices
exercice_1()
exercice_2()

print("\n" + "="*60)
print("NOTEBOOK TERMINÉ - ARBRES DE DÉCISION")
print("="*60)