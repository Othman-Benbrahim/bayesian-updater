# Éthique et limites — Ce que Bayes ne peut pas faire

Ce fichier expose les limites structurelles de l'approche bayésienne, les risques d'usage abusif, et les garde-fous épistémiques à maintenir.

---

## 1. La sensibilité au prior — La limite fondamentale

### Le problème

Le résultat d'une mise à jour bayésienne dépend du prior. Deux analystes qui partagent les mêmes observations mais ont des priors différents arriveront à des posteriors différents — et tous deux auront correctement appliqué Bayes.

Cela n'est pas un défaut du théorème. C'est sa propriété fondamentale : **le prior encode l'état de connaissance initial, et cet état compte**.

Mais cela implique que la force apparente d'une mise à jour peut être gonflée ou dégonflée selon le prior choisi.

### Illustration

**Scénario A** : analyste prudent, P(H) = 0.30, BF = 5.
```
O(H)   = 0.30/0.70 = 0.429
O(H|E) = 0.429 × 5 = 2.14
P(H|E) = 2.14/3.14 = 0.68
```

**Scénario B** : analyste confiant, P(H) = 0.70, BF = 5.
```
O(H)   = 0.70/0.30 = 2.333
O(H|E) = 2.333 × 5 = 11.67
P(H|E) = 11.67/12.67 = 0.92
```

Même observation, même BF, posteriors très différents (0.68 vs 0.92). Ce n'est pas une erreur — c'est la propagation légitime d'états de connaissance initiaux différents.

### Conséquence pratique

Avant de partager ou comparer des analyses bayésiennes, **toujours afficher explicitement le prior** utilisé. Un posterior de 0.92 sans connaître le prior ne dit rien.

---

## 2. Le problème du prior subjectif

### Comment choisir le prior ?

C'est la question la plus délicate de l'analyse bayésienne. Plusieurs approches :

- **Prior informatif** : basé sur un base rate historique (recommandé).
- **Prior de consensus** : probabilité partagée par plusieurs analystes.
- **Prior non-informatif** : 0.50 (absence d'information préalable).
- **Prior propre** : honnête estimation personnelle.

En pratique, pour les dossiers politiques et stratégiques, le **prior informatif via base rate** est préférable. Voir `protocole-enregistrement.md` dans *Calibration Engine* pour la discipline de base rate.

### Le prior biaisé

Si le prior est lui-même biaisé (narrative attractor, biais de confirmation sur l'analyse initiale), la mise à jour bayésienne le **conserve et l'amplifie**. Bayes ne corrige pas les mauvais priors.

**Remédiation** : vérifier la source du prior avant d'appliquer la mise à jour. Si le prior vient d'une lecture symbolique pure (Fractales), traiter comme prior "à vérifier" et lui appliquer une incertitude plus large.

---

## 3. La dépendance entre observations

### Le risque

La mise à jour séquentielle (O(H|E₁,E₂,E₃) = O(H) × BF₁ × BF₂ × BF₃) suppose que E₁, E₂, E₃ sont **conditionnellement indépendants** sachant H.

Cette hypothèse est souvent violée :
- Plusieurs articles de presse basés sur la même source unique.
- Plusieurs indicateurs qui reflètent la même dynamique sous-jacente.
- Plusieurs signaux faibles produits par le même acteur.

Si les observations sont corrélées et qu'on les multiplie indépendamment, le BF effectif est surestimé.

### Règle de prudence

Si E₁ et E₂ viennent de sources liées, traiter comme une seule observation avec BF maximal = max(BF₁, BF₂) plutôt que BF₁ × BF₂.

---

## 4. Bayes n'est pas applicable à tout

### Cas 1 : Hypothèses non-exhaustives

Si les hypothèses ne couvrent pas l'espace des possibles (violation du MECE), le théorème des probabilités totales sous-estime P(E). Le posterior est biaisé.

**Signal d'alerte** : si une observation arrive qui ne rentre dans aucune des hypothèses existantes (BF ≈ 0 sur tout), il faut ajouter une nouvelle hypothèse H4.

### Cas 2 : Événements sans classe de référence

Pour les événements uniques ou sans précédent historique, les vraisemblances sont non-identifiables. Il est impossible d'estimer P(E|H) pour un événement qui n'a jamais eu lieu.

**Traitement** : utiliser le mode qualitatif (`raisonnement-qualitatif.md`) avec des intervalles larges et signaler l'incertitude profonde sur les vraisemblances.

### Cas 3 : Hypothèses symboliques (Fractales)

Un archétype ne peut pas être H dans une mise à jour bayésienne formelle. Ce n'est pas une hypothèse falsifiable. Seules les *prédictions dérivées* d'une lecture symbolique peuvent être intégrées.

### Cas 4 : Situations à changement structurel

Quand la structure du système change (ex : changement de régime politique, guerre, rupture technologique), les vraisemblances historiques ne s'appliquent plus. Un BF estimé à partir d'une période stable est invalide dans une période de turbulence.

**Traitement** : identifier explicitement les "ruptures de régime" et resetter les priors sur des bases nouvelles.

---

## 5. Le biais de confirmation bayésien

### Le mécanisme

Un analyste fortement convaincu de H peut inconsciemment :
- **Sur-estimer P(E|H)** : percevoir l'observation comme très attendue sous H.
- **Sous-estimer P(E|¬H)** : minimiser les raisons pour lesquelles E pourrait apparaître sous ¬H.

Résultat : BF artificiellement haut, posterior artificiellement fort.

Bayes ne protège pas contre ce biais — au contraire, il lui donne une **apparence de rigueur mathématique**.

### Remédiation

1. **Éliciter P(E|¬H) en premier** : forcer l'analyste à raisonner sur la meilleure hypothèse adverse avant de raisonner sur la sienne.
2. **Challenger les vraisemblances** : demander *"À quel point seriez-vous surpris si E apparaissait alors que H est fausse ?"*
3. **Analyse de sensibilité** : montrer comment le posterior change si P(E|¬H) est doublé. Si le posterior reste fort, l'analyse est robuste. Si le posterior s'effondre, le BF était fragile.

---

## 6. L'utilisation de Bayes comme autorité

### Le risque

Le formalisme bayésien (chiffres, tableau, BF) peut donner une **autorité illusoire** à une analyse qui repose sur des vraisemblances subjectives.

Un posterior de 0.84 produit par Bayes n'est pas plus objectif qu'une estimation directe de 0.84 — si les vraisemblances sont subjectives, le posterior l'est aussi. La rigueur du calcul ne compense pas l'arbitraire des inputs.

### Règle de communication

Toute analyse bayésienne partagée à un tiers doit inclure :
- Les priors utilisés.
- Les vraisemblances estimées.
- Une mention que les vraisemblances sont subjectives.
- Une analyse de sensibilité sur les paramètres clés.

Sans ces éléments, le posterior seul est trompeur.

---

## 7. Ce que le skill peut et ne peut pas promettre

| Ce que le skill fait | Ce qu'il ne fait pas |
|---------------------|---------------------|
| Appliquer formellement Bayes sur les inputs | Valider que les inputs sont corrects |
| Identifier la force de l'évidence (BF) | Estimer les vraisemblances à la place de l'analyste |
| Tracer les révisions pour audit futur | Corriger un prior biaisé |
| Signaler les résultats extrêmes pour vérification | Garantir que les hypothèses couvrent l'espace |
| Rendre la mise à jour transparente | Produire un posterior "objectif" |
| Connecter au Calibration Engine | Garantir l'amélioration prédictive |

---

## 8. Statut épistémique du skill

Le Bayesian Updater est un **outil de cohérence interne**. Il garantit que les révisions sont mathématiquement cohérentes avec les inputs fournis. Il ne garantit pas que ces inputs sont corrects, que les hypothèses sont exhaustives, ou que les posteriors correspondront aux fréquences futures.

Sa valeur est dans la **discipline** qu'il impose : expliciter le prior, expliciter les vraisemblances, calculer le posterior, tracer la révision. Cette discipline réduit les biais systématiques les plus grossiers (ancrage, récence, narrative attractor) sans les éliminer.

---

*« Bayes est une contrainte de cohérence, pas un oracle de vérité. Son usage honnête requiert d'admettre ce qu'on ne sait pas autant que ce qu'on sait. »*
