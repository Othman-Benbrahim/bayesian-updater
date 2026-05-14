# Théorie bayésienne — Formules, intuition, forme odds

Ce fichier expose le théorème de Bayes dans ses deux formes opératoires, l'intuition derrière chaque terme, l'échelle d'interprétation du Bayes Factor, et les propriétés clés pour l'usage analytique.

---

## 1. Le théorème de Bayes — Forme probabilité

### Formule

```
P(H|E) = P(H) × P(E|H) / P(E)
```

avec :

```
P(E) = P(H) × P(E|H) + P(¬H) × P(E|¬H)
```

### Les quatre termes

| Terme | Nom | Signification |
|-------|-----|--------------|
| P(H) | **Prior** | Probabilité de H *avant* d'observer E. État de connaissance initial. |
| P(E\|H) | **Vraisemblance** | Probabilité d'observer E *si H est vraie*. Pont entre hypothèse et observation. |
| P(E\|¬H) | **Vraisemblance contrefactuelle** | Probabilité d'observer E *si H est fausse*. |
| P(H\|E) | **Posterior** | Probabilité de H *après* avoir observé E. État de connaissance mis à jour. |
| P(E) | **Évidence marginale** | Probabilité totale d'observer E, toutes hypothèses confondues. Facteur de normalisation. |

### Intuition

Bayes dit : le posterior est proportionnel au prior multiplié par la vraisemblance.

En d'autres termes :
> *Ce que je croyais avant × À quel point cette observation est cohérente avec mon hypothèse = Ce que je dois croire maintenant.*

---

## 2. Le Bayes Factor — Mesure de la force de l'évidence

### Définition

```
BF(E) = P(E|H) / P(E|¬H)
```

Le Bayes Factor est le **rapport des vraisemblances**. Il mesure combien de fois l'observation E est plus probable sous H que sous ¬H.

- BF > 1 : E favorise H
- BF = 1 : E est neutre (ne révise pas)
- BF < 1 : E défavorise H (révise à la baisse)

### Avantage du Bayes Factor

Le BF est indépendant du prior. Il représente **le poids intrinsèque de l'observation**. Deux analystes avec des priors différents sur H voient le même BF — mais calculent des posteriors différents. Cette séparation entre *force de l'évidence* et *état initial de croyance* est fondamentale.

### Échelle de Jeffreys (1961)

| BF | Interprétation |
|----|---------------|
| 1 | Nul — observation neutre |
| 1–3 | Anecdotique — légère mise à jour |
| 3–10 | Modéré — révision significative |
| 10–30 | Fort — révision nette |
| 30–100 | Très fort — révision majeure |
| > 100 | Décisif — révision quasi-complète |

**Symétrie** : BF < 1 suit la même logique inversée. Un BF = 0.10 est aussi décisif contre H qu'un BF = 10 l'est pour H.

---

## 3. Le théorème de Bayes — Forme odds (recommandée pour usage séquentiel)

### Conversion probabilité ↔ odds

```
O(H) = P(H) / (1 − P(H))    ← odds à partir de probabilité
P(H) = O(H) / (1 + O(H))    ← probabilité à partir de odds
```

Exemples :

| P(H) | O(H) |
|------|------|
| 0.10 | 1/9 ≈ 0.111 |
| 0.25 | 1/3 ≈ 0.333 |
| 0.50 | 1.000 |
| 0.75 | 3.000 |
| 0.90 | 9.000 |

### Forme odds de Bayes

```
O(H|E) = O(H) × BF(E)
```

C'est tout. Le posterior en odds = le prior en odds × le Bayes Factor.

### Pourquoi la forme odds est supérieure pour les mises à jour séquentielles

Si plusieurs observations E₁, E₂, E₃ arrivent successivement (et sont *conditionnellement indépendantes* sachant H) :

```
O(H|E₁,E₂,E₃) = O(H) × BF(E₁) × BF(E₂) × BF(E₃)
```

Chaque nouvelle observation multiplie simplement les odds par son BF. Pas besoin de recalculer P(E) à chaque fois.

### Exemple complet en forme odds

Situation : P(H) = 0.60. Trois observations successives.

```
O(H) initial         = 0.60/0.40  = 1.500

Observation E₁ :  BF = 3.40
O(H|E₁)             = 1.500 × 3.40  = 5.100
P(H|E₁)             = 5.100/6.100   = 0.836

Observation E₂ :  BF = 0.40  (observation défavorable)
O(H|E₁,E₂)          = 5.100 × 0.40  = 2.040
P(H|E₁,E₂)          = 2.040/3.040   = 0.671

Observation E₃ :  BF = 8.00  (observation forte)
O(H|E₁,E₂,E₃)       = 2.040 × 8.00  = 16.320
P(H|E₁,E₂,E₃)       = 16.320/17.320 = 0.942
```

---

## 4. Propriétés clés

### 4.1 La sensibilité au prior

Plus le prior est extrême (proche de 0 ou 1), moins une observation même forte peut réviser.

**Exemple** : P(H) = 0.01, BF = 100.

```
O(H)   = 0.01/0.99 = 0.0101
O(H|E) = 0.0101 × 100 = 1.01
P(H|E) = 1.01/2.01 = 0.502
```

Malgré un BF de 100 (décisif sur l'échelle de Jeffreys), une hypothèse initiale à 1% n'atteint que 50% après l'observation. C'est le fondement de l'**asymétrie de révision** : il est très difficile de passer de "presque impossible" à "probable" en une seule observation.

### 4.2 L'indépendance conditionnelle

La multiplication des BF séquentiels suppose que les observations sont **conditionnellement indépendantes** sachant H, c'est-à-dire que chaque observation apporte une information nouvelle indépendante.

Si les observations sont corrélées (ex : plusieurs articles de presse basés sur la même source unique), les multiplier surestime la force de l'évidence. L'agent doit signaler ce risque.

### 4.3 L'observation neutre

Une observation a un BF = 1 (et donc ne révise pas) quand P(E|H) = P(E|¬H). C'est le cas d'une observation "compatible avec tout" : elle ne discrimine pas.

**Exemple** : "Le PDG a mangé au restaurant aujourd'hui." Compatible avec H et ¬H de manière équivalente — BF ≈ 1, pas de révision.

### 4.4 L'observation négative

L'absence d'un événement attendu est aussi une observation. Si un indicateur de bascule *devrait* s'être déclenché à cette date et ne l'a pas fait, c'est une information :

```
E = "l'indicateur n'est pas apparu à l'horizon prévu"
P(E|H)    = 1 − P(indicateur | H)  ← faible si H prédit l'indicateur
P(E|¬H)   = 1 − P(indicateur | ¬H) ← plus élevé si ¬H ne le prédit pas
```

---

## 5. Les cas limites

### Prior à 0 ou 1

Mathématiquement, si P(H) = 0, alors P(H|E) = 0 quelles que soient les preuves. Un prior à 0 signifie une impossibilité absolue — aucune preuve ne peut changer cela. C'est précisément pourquoi les priors à 0 et 1 sont **interdits** en pratique analytique (voir `protocole-enregistrement.md` dans *Calibration Engine*).

### Vraisemblances à 0 ou 1

De même, P(E|H) = 0 signifierait "E est impossible si H est vraie", ce qui permettrait d'exclure H définitivement si E est observé (BF = 0). Ces extrêmes sont possibles logiquement mais rares en pratique.

---

## 6. Le logarithme des Bayes Factors

Pour les mises à jour séquentielles sur de longues séries, il est pratique de travailler en log-BF :

```
log(O(H|E₁,E₂,...,Eₙ)) = log(O(H)) + Σ log(BF(Eₖ))
```

Avantage : les additions remplacent les multiplications, ce qui évite les underflows numériques.

Unité : **ban** (log en base 10) ou **nat** (log naturel). Un ban = 10 décibans.

Un BF de 10 = 1 ban. Un BF de 100 = 2 bans. Un BF de 3.16 = 0.5 ban (demi-ban).

---

## Références

- Bayes, T., & Price, R. (1763). An Essay towards solving a Problem in the Doctrine of Chances. *Philosophical Transactions of the Royal Society*, 53, 370-418.
- Jeffreys, H. (1961). *Theory of Probability* (3rd ed.). Oxford University Press.
- Good, I. J. (1950). *Probability and the Weighing of Evidence*. Griffin.
- Jaynes, E. T. (2003). *Probability Theory: The Logic of Science*. Cambridge University Press.
- Kass, R. E., & Raftery, A. E. (1995). Bayes factors. *Journal of the American Statistical Association*, 90(430), 773-795.
