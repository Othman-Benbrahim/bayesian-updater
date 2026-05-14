# Mise à jour multi-hypothèses — ACH-Bayes

Ce fichier décrit la procédure de mise à jour bayésienne simultanée de plusieurs hypothèses concurrentes, en s'appuyant sur la *Analysis of Competing Hypotheses* (Heuer, 1999) étendue à Bayes.

---

## 1. Pourquoi mettre à jour toutes les hypothèses ensemble

Dans *Signaux du Futur* et *Miroir Trans-échelle*, l'analyse produit typiquement 3 hypothèses concurrentes (H1, H2, H3) dont les probabilités somment à 1. Quand une nouvelle observation arrive, **toutes les hypothèses doivent être mises à jour ensemble**.

Raison mathématique : les posteriors doivent aussi sommer à 1. Mettre à jour H1 seule sans ajuster H2 et H3 brise cette contrainte.

Raison analytique : une observation diagnostique renforce H1 mécaniquement *aux dépens* de H2 et H3. Ne pas voir cet effet induit une analyse incohérente.

---

## 2. Procédure complète

### Étape 1 — Préparer le tableau de priors

Récupérer les trois hypothèses et leurs probabilités initiales.

```
Vérification : P(H1) + P(H2) + P(H3) = 1.00 (± 0.01)
```

Si les probabilités ne somment pas à 1, demander ajustement avant de continuer.

### Étape 2 — Délimiter l'observation

Formuler E avec précision. Si E est vague, demander reformulation.

Vérifier que E est observée (passé) et non une prédiction.

### Étape 3 — Éliciter P(E|Hk) pour chaque hypothèse

Pour chaque hypothèse Hk, appliquer le protocole d'élicitation (voir `elicitation-vraisemblances.md`) en maintenant la cohérence inter-hypothèses :

> *"Si j'estime que P(E|H1) = 0.85 (très probable sous H1), et que j'estime P(E|H2) = 0.85 aussi (très probable sous H2), alors E ne discrimine pas entre H1 et H2, peu importe sa valeur absolue."*

**Règle de cohérence** : les vraisemblances relatives importent autant que leurs valeurs absolues. L'agent peut demander :

> *"En supposant que ces trois hypothèses soient les seules possibles, quelle est celle sous laquelle E est le plus attendu ? Le moins attendu ?"*

### Étape 4 — Calculer les numérateurs

```
Pour chaque k :
  num_k = P(Hk) × P(E|Hk)
```

### Étape 5 — Calculer P(E) par normalisation

```
P(E) = Σ num_k = num_1 + num_2 + num_3
```

### Étape 6 — Calculer les posteriors

```
P(Hk|E) = num_k / P(E)
```

Vérification : Σ P(Hk|E) = 1.00

### Étape 7 — Calculer les Bayes Factors et Likelihood Ratios

Pour chaque hypothèse, calculer le rapport de vraisemblance par rapport à la "moyenne" des autres :

```
LR(Hk) = P(E|Hk) / P(E)_moyen_autres_hypothèses
```

Ou plus simplement, comparer les vraisemblances deux à deux :

```
BF(H1 vs H2) = P(E|H1) / P(E|H2)
BF(H1 vs H3) = P(E|H1) / P(E|H3)
```

---

## 3. Format de tableau standardisé

```
OBSERVATION : [E]

┌─────────────────────────┬────────┬──────────┬───────────────┬──────────┐
│ Hypothèse               │ Prior  │ P(E│Hk)  │ Prior×P(E│Hk) │ Post.    │
├─────────────────────────┼────────┼──────────┼───────────────┼──────────┤
│ H1 — [libellé court]    │ P₁     │ L₁       │ P₁ × L₁       │ P₁'      │
│ H2 — [libellé court]    │ P₂     │ L₂       │ P₂ × L₂       │ P₂'      │
│ H3 — [libellé court]    │ P₃     │ L₃       │ P₃ × L₃       │ P₃'      │
├─────────────────────────┼────────┼──────────┼───────────────┼──────────┤
│ TOTAL                   │ 1.000  │  —       │ = P(E)        │ ≈ 1.000  │
└─────────────────────────┴────────┴──────────┴───────────────┴──────────┘

Δ (variation de rang ou de dominance) : [commentaire]
BF(H1 vs H2) : L₁/L₂ = [valeur]  → [interprétation]
```

---

## 4. Exemple complet annoté

### Situation

Dossier : restructuration de l'entreprise X.

Hypothèses actuelles :
- H1 (cession/fusion) : P = 0.60
- H2 (restructuration interne) : P = 0.25
- H3 (scandale bloquant) : P = 0.15

Observation E : *"Le conseil d'administration a voté ce matin la suspension de toute décision stratégique pour 60 jours, sans communiqué."*

### Élicitation des vraisemblances

**P(E|H1 — cession imminente)** : si une cession était en cours, la suspension d'urgence suggère un accord en phase finale ou une contre-offre de dernière minute. L'absence de communiqué suggère confidentialité. *Assez probable.* → **0.65**

**P(E|H2 — restructuration interne)** : une restructuration interne n'implique pas habituellement de suspension d'urgence. Ce serait surprenant. → **0.15**

**P(E|H3 — scandale bloquant)** : si un scandale était en gestation, une suspension d'urgence "pour examiner la situation" est très typique. Très attendu. → **0.88**

### Calcul

```
num_H1 = 0.60 × 0.65 = 0.390
num_H2 = 0.25 × 0.15 = 0.038
num_H3 = 0.15 × 0.88 = 0.132

P(E) = 0.390 + 0.038 + 0.132 = 0.560

P(H1|E) = 0.390 / 0.560 = 0.696
P(H2|E) = 0.038 / 0.560 = 0.068
P(H3|E) = 0.132 / 0.560 = 0.236
```

### Tableau

```
┌─────────────────────────────┬────────┬──────────┬─────────────┬─────────┐
│ Hypothèse                   │ Prior  │ P(E│Hk)  │ Num.        │ Post.   │
├─────────────────────────────┼────────┼──────────┼─────────────┼─────────┤
│ H1 — Cession / fusion       │ 0.600  │ 0.65     │ 0.390       │ 0.696   │
│ H2 — Restructuration interne│ 0.250  │ 0.15     │ 0.038       │ 0.068   │
│ H3 — Scandale bloquant      │ 0.150  │ 0.88     │ 0.132       │ 0.236   │
├─────────────────────────────┼────────┼──────────┼─────────────┼─────────┤
│ TOTAL                       │ 1.000  │  —       │ 0.560       │ 1.000   │
└─────────────────────────────┴────────┴──────────┴─────────────┴─────────┘
```

### Lecture

```
Δ rankings : H2 s'effondre (0.25 → 0.07). H3 gagne en proportion
(0.15 → 0.24) malgré son prior faible, car très diagnostique de E.
H1 reste dominante mais H3 mérite maintenant une attention réelle.

BF(H3 vs H2) = 0.88 / 0.15 = 5.9 → Modéré/Fort en faveur de H3 vs H2
BF(H1 vs H3) = 0.65 / 0.88 = 0.74 → Légèrement en faveur de H3 sur H1

CONCLUSION : E renforce H1 en termes absolus mais révèle surtout
l'incompatibilité de H2. H3 devient une hypothèse à prendre au sérieux.
Recommandation : monitorer les indicateurs spécifiques à H3 (enquête,
audits, fuites internes).
```

---

## 5. Cas à quatre hypothèses et plus

Le tableau s'étend naturellement à 4, 5 hypothèses. Règle pratique : au-delà de 4, regrouper les hypothèses mineures (P < 0.05) dans une catégorie "Autre" pour éviter la dilution analytique.

---

## 6. Mise à jour séquentielle multi-hypothèses

Si plusieurs observations E₁, E₂, E₃ arrivent successivement, le posterior de chaque mise à jour devient le prior de la suivante :

```
Cycle 1 : priors P(Hk) → observation E₁ → posteriors P(Hk|E₁)
Cycle 2 : priors = P(Hk|E₁) → observation E₂ → posteriors P(Hk|E₁,E₂)
...
```

Condition d'indépendance conditionnelle à vérifier entre observations.

---

## 7. Pièges spécifiques au multi-hypothèses

### Piège : "L'hypothèse nulle" oubliée

Si H1 + H2 + H3 ne couvrent pas l'espace des possibles (ex : un événement imprévu arrive hors de ces trois scénarios), le tableau de Bayes ne peut pas le capturer. Toujours vérifier que les hypothèses couvrent bien l'espace (MECE : mutuellement exclusives, collectivement exhaustives).

### Piège : Vraisemblances identiques

Si P(E|H1) = P(E|H2) = P(E|H3) = même valeur, la mise à jour ne change rien aux proportions (seuls les totaux bougent). Vérifier que cela est vraiment l'estimation de l'analyste avant de conclure que l'observation est neutre.

### Piège : Révision de l'hypothèse dominante vers 0.99+

Si après une mise à jour multi-hypothèses une hypothèse atteint 0.97 ou plus, l'agent signale :

> *"Résultat très fort. Vérifier les vraisemblances avant de conclure."*

L'analyste peut être victime du narrative attractor ou de la conjonction P(E|Hk) élevée + prior élevé qui produit une convergence artificielle.

---

## 8. Connexion avec ACH de Heuer

La *Analysis of Competing Hypotheses* de Heuer (1999) construit une matrice observations × hypothèses et note chaque cellule (+, −, neutre). Le tableau ACH-Bayes que ce skill produit est une **version quantitative** de cette matrice : les vraisemblances P(E|Hk) remplacent les notations qualitatives et permettent un calcul exact.

Les deux approches se complètent : l'ACH qualitatif est utile pour un premier balayage rapide, le tableau bayésien pour la mise à jour formelle.
