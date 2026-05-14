# Élicitation des vraisemblances — Comment estimer P(E|H) pratiquement

L'estimation des vraisemblances P(E|H) et P(E|¬H) est **le cœur du travail analytique bayésien**. C'est ici que le raisonnement analytique se traduit en chiffres. Ce fichier expose une méthode structurée pour arriver à des estimations honnêtes.

---

## 1. La question fondamentale

Pour estimer P(E|H), l'analyste doit se poser une question précise et mentalement inconfortable :

> *"Si je savais avec certitude que H est vraie, à quel point serais-je surpris d'observer E ?"*

Pour P(E|¬H) :

> *"Si je savais avec certitude que H est fausse, à quel point serais-je surpris d'observer E ?"*

L'inconfort vient de ce qu'il faut **raisonner depuis la réalité d'une hypothèse qu'on ne croit peut-être pas** — y compris l'hypothèse adverse. C'est le cœur de l'honnêteté bayésienne.

---

## 2. Protocole en 4 questions

Pour toute observation E et toute hypothèse H, enchaîner ces quatre questions :

### Q1 — "Si H était vraie, E arriverait-il souvent, parfois, rarement ?"

C'est la question de P(E|H). Elle force à se demander : dans un monde où H est vraie, quelle est la fréquence de E ?

### Q2 — "Si H était fausse, E arriverait-il souvent, parfois, rarement ?"

C'est la question de P(E|¬H). Elle force à se demander : dans un monde où H est fausse, quelle est la fréquence de E ?

### Q3 — "E est-il plus probable sous H ou sous ¬H ?"

C'est la question du signe du BF. Selon la réponse :
- Sous H → BF > 1 → révision à la hausse
- Sous ¬H → BF < 1 → révision à la baisse
- Équivalent → BF ≈ 1 → pas de révision

### Q4 — "À quel point est-il plus probable sous l'un que sous l'autre ?"

C'est la magnitude du BF. *"2× plus probable ?"*, *"10× ?"*, *"à peine plus ?"*

---

## 3. Grille d'estimation directe

Si l'utilisateur ne sait pas par où commencer, proposer cette grille :

```
"Si H est vraie, E est..."

Quasi-certain        → P(E|H) ≈ 0.90–0.95
Très probable        → P(E|H) ≈ 0.75–0.89
Assez probable       → P(E|H) ≈ 0.55–0.74
Ni probable ni rare  → P(E|H) ≈ 0.35–0.54
Assez rare           → P(E|H) ≈ 0.15–0.34
Très rare            → P(E|H) ≈ 0.05–0.14
Quasi-impossible     → P(E|H) ≈ 0.01–0.04
```

Même grille pour P(E|¬H). Le BF en découle.

---

## 4. Typologies d'observations et BF typiques

### Observation diagnostique (BF fort)

E est très attendu sous H mais surprenant sous ¬H.

Exemple : *"Le CFO démissionne le jour même où des rumeurs de fraude circulent."*
- P(E|H fraude préparée) ≈ 0.80
- P(E|¬H fraude) ≈ 0.05
- BF = 16 → Fort

Ces observations sont précieuses. Elles révisent substantiellement.

### Observation confirmante mais non-distinctive (BF modéré)

E est attendu sous H mais aussi sous ¬H, juste un peu moins.

Exemple : *"Le PDG fait une interview positive sur l'avenir de l'entreprise."*
- P(E|H stabilité) ≈ 0.80
- P(E|¬H stabilité) ≈ 0.55
- BF = 1.45 → Anecdotique

Ces observations sont cohérentes avec H mais peu informatives.

### Observation compatible avec tout (BF ≈ 1)

E est tout aussi probable sous H que sous ¬H.

Exemple : *"Le bureau communique un rapport trimestriel standard."*
- P(E|H) ≈ 0.70, P(E|¬H) ≈ 0.70
- BF = 1.00 → Nul

Ne pas logger comme mise à jour.

### Observation surprise sous H (BF < 1)

E est inattendu sous H mais attendu sous ¬H.

Exemple : *"La fusion a été repoussée indéfiniment après une résolution du CA unanime."*
- P(E|H fusion imminente) ≈ 0.05
- P(E|¬H fusion) ≈ 0.80
- BF = 0.06 → Très fort contre H

---

## 5. Les pièges classiques d'élicitation

### Piège 1 : Confondre P(E|H) et P(H|E)

C'est l'erreur la plus courante. Quelqu'un dit *"Si je vois cet indicateur, H est probable à 80%"* — c'est P(H|E). Mais pour Bayes, il faut P(E|H) : si H est vraie, quelle est la probabilité que cet indicateur apparaisse ?

Ce renversement s'appelle le **sophisme du procureur** (prosecutor's fallacy) en droit.

### Piège 2 : Ancrage sur P(E|H) uniquement

L'analyste estime P(E|H) mais "oublie" d'estimer P(E|¬H) avec la même rigueur. La vraisemblance contrefactuelle est souvent sous-estimée, produisant des BF artificiellement forts.

**Remédiation** : toujours éliciter les deux vraisemblances *indépendamment*, dans l'ordre suivant : d'abord P(E|¬H) (la plus difficile à penser), puis P(E|H).

### Piège 3 : Base rate neglect via les vraisemblances

Si E est un événement rare en général (ex : coup d'État), les vraisemblances P(E|H) et P(E|¬H) doivent toutes deux être basses. L'analyste qui affecte P(E|H) = 0.80 pour un événement rare sans réfléchir à P(E|¬H) commet une erreur de calibration.

**Remédiation** : avant d'estimer les vraisemblances, demander *"À quelle fréquence E arrive-t-il en général dans des situations similaires ?"*

### Piège 4 : Corrélation entre observations

Si deux observations E₁ et E₂ viennent de la même source (ex : deux articles issus de la même fuite), appliquer le BF des deux séparément surestime l'évidence. Elles ne sont pas conditionnellement indépendantes.

**Remédiation** : identifier la source commune. Si les observations partagent une source unique, traiter l'ensemble comme une seule observation et affecter un BF unique.

---

## 6. Questions d'aide à l'élicitation (guide conversationnel)

L'agent peut aider l'utilisateur avec ces questions :

**Pour P(E|H) :**
- *"Dans un monde où H est certainement vraie, combien de fois sur 100 situations similaires observeriez-vous E ?"*
- *"Si vous regardiez 100 cas historiques où H était vraie, dans combien de cas E était-il présent ?"*
- *"Est-ce que H 'prédit' E, ou est-ce qu'E est compatible avec H sans être prédit par elle ?"*

**Pour P(E|¬H) :**
- *"Dans un monde où H est certainement fausse, combien de fois observeriez-vous quand même E ?"*
- *"Quelles sont les raisons pour lesquelles E pourrait apparaître même si H est fausse ?"*
- *"Est-ce qu'E a des causes alternatives à H ?"*

**Pour vérification de cohérence :**
- *"P(E|H) / P(E|¬H) = BF. Ce ratio vous semble-t-il juste intuitivement ?"*
- *"Si vous voyiez cet événement E 10 fois dans un dossier, combien de fois serait-ce parce que H est vraie ?"*

---

## 7. Vraisemblances qualitatives et conversion numérique

Quand l'utilisateur ne peut pas donner un chiffre précis, il peut utiliser des **étiquettes qualitatives** que l'agent convertit en intervalles numériques :

| Étiquette qualitative | Intervalle numérique |
|----------------------|---------------------|
| "Quasi-certain" | 0.90–0.97 |
| "Très probable" | 0.75–0.89 |
| "Plutôt probable" | 0.55–0.74 |
| "Incertain" | 0.35–0.54 |
| "Plutôt improbable" | 0.15–0.34 |
| "Rare" | 0.05–0.14 |
| "Quasi-impossible" | 0.01–0.04 |

Pour la mise à jour, l'agent prend les **milieux des intervalles** et calcule le BF. Si le BF est robuste aux variations dans l'intervalle (ex : BF reste entre 3 et 10 quelle que soit la valeur dans l'intervalle), la mise à jour est fiable. Si le BF est très sensible, l'agent signale l'incertitude sur les vraisemblances.

---

## 8. Analyse de sensibilité des vraisemblances

Pour les dossiers importants, tester la robustesse du résultat par analyse de sensibilité :

```
Scenario pessimiste (vraisemblances moins diagnostiques) :
  P(E|H)  = 0.55  (vs 0.85 dans le scénario nominal)
  P(E|¬H) = 0.35  (vs 0.15 dans le scénario nominal)
  BF = 0.55/0.35 = 1.57  → Anecdotique
  Posterior : 0.70 (vs 0.84 dans le nominal)

Scenario optimiste (vraisemblances plus diagnostiques) :
  P(E|H)  = 0.95
  P(E|¬H) = 0.10
  BF = 9.50  → Fort
  Posterior : 0.93 (vs 0.84 dans le nominal)
```

Si le posterior varie de 0.70 à 0.93 selon les vraisemblances, la conclusion qualitative reste la même (H est favorable) mais la précision est faible. À signaler.

