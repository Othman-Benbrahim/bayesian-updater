# Raisonnement bayésien qualitatif

Ce fichier décrit comment appliquer la *logique* bayésienne quand les chiffres précis ne sont pas disponibles ou pas fiables. L'objectif n'est pas de calculer un posterior exact, mais d'appliquer la discipline de pensée qui évite les erreurs grossières.

---

## 1. Pourquoi un mode qualitatif

Le mode quantitatif (Mode 1 et Mode 2 du SKILL.md) requiert des vraisemblances numériques. Dans certains cas, forcer un chiffre précis sur des bases insuffisantes produit une **fausse précision** plus dangereuse que l'incertitude explicite.

Le mode qualitatif est adapté quand :
- L'analyste ne peut pas estimer les vraisemblances avec une granularité > 0.20.
- L'observation est intrinsèquement ambigu (signaux mixtes).
- La situation est sans précédent historique clair.
- On veut faire un premier tri rapide avant de choisir les observations à formaliser.

---

## 2. Le test de la surprise — Méthode rapide

Pour chaque observation E sur un dossier comportant une hypothèse H :

**Question unique** : *"Est-ce que cette observation me surprend si H est vraie ? Est-ce qu'elle me surprend si H est fausse ?"*

Quatre réponses possibles :

| Surprenant si H vrai ? | Surprenant si H faux ? | Conclusion |
|------------------------|------------------------|-----------|
| Non | Oui | **E confirme H** → réviser à la hausse |
| Oui | Non | **E infirme H** → réviser à la baisse |
| Non | Non | **E est neutre** → ne pas réviser |
| Oui | Oui | **E est surprenant dans tous les cas** → signal fort, analyser séparément |

Le quatrième cas (surprenant partout) est un signal que les hypothèses actuelles ne couvrent peut-être pas la bonne situation. Envisager de réviser les hypothèses elles-mêmes, pas seulement leurs probabilités.

---

## 3. La hiérarchie de force qualitative

Quand on ne chiffre pas les vraisemblances, on peut quand même qualifier la force de la révision :

| Description | BF approximatif | Effet sur P(H) = 0.50 |
|-------------|----------------|----------------------|
| **Décisif contre toute attente** | > 50 | → > 0.98 |
| **Très fort** | 10–50 | → 0.91–0.98 |
| **Fort** | 4–10 | → 0.80–0.91 |
| **Modéré** | 2–4 | → 0.67–0.80 |
| **Faible** | 1.2–2 | → 0.55–0.67 |
| **Neutre** | ≈ 1 | → pas de révision |
| **Faible contre** | 0.5–0.83 | → 0.33–0.45 |
| **Fort contre** | 0.1–0.25 | → 0.09–0.20 |

---

## 4. Les quatre signaux qualitatifs clés

### Signal de type A — Indicateur de bascule déclenché

Un indicateur de bascule préalablement défini dans le log vient d'apparaître.

*Logique bayésienne* : l'indicateur a été choisi précisément parce qu'il était attendu sous H et non sous ¬H. Son apparition est donc diagnostique.

**Révision qualitative recommandée** : +0.10 à +0.25 selon la spécificité de l'indicateur.

*Exemple* : la démission d'un CFO prévue comme indicateur de la trajectoire "scandale" se produit → révision à la hausse sur H3 de l'ordre de +0.15.

### Signal de type B — Silence significatif

Un indicateur attendu *sous une hypothèse* aurait dû apparaître à cette date et n'apparaît pas.

*Logique bayésienne* : l'absence d'E attendu est une observation négative (voir `theorie-bayesienne.md` section 4.3).

**Révision qualitative recommandée** : −0.05 à −0.15 selon le délai et la certitude de l'attendu.

*Exemple* : l'accord de fusion aurait dû être annoncé avant fin du trimestre. Il ne l'est pas. → Révision à la baisse sur H1 de l'ordre de −0.10.

### Signal de type C — Dissonance narrative

L'observation contredit le récit dominant du dossier sans clairement valider une autre hypothèse.

*Logique bayésienne* : BF incertain mais probablement < 1 sur l'hypothèse dominante.

**Révision qualitative recommandée** : −0.05 à −0.10 sur H1 (hypothèse dominante), redistribution sur H2/H3.

### Signal de type D — Convergence multi-sources

Plusieurs sources indépendantes confirment simultanément le même signal.

*Logique bayésienne* : si les sources sont réellement indépendantes, les BF se multiplient.

**Révision qualitative recommandée** : proportionnelle au degré d'indépendance. Si 3 sources indépendantes chacune à BF ≈ 3, BF global ≈ 27 → Fort.

**Piège** : vérifier l'indépendance des sources. Si elles convergent toutes sur la même fuite, c'est une seule observation amplifiée, pas trois.

---

## 5. Le tableau qualitatif de mise à jour

Pour un usage rapide, sans calcul, sur une observation :

```
OBSERVATION : [E]

H1 — [libellé] :
  E était-il attendu sous H1 ? [Oui / Neutre / Non]
  → Révision : [Hausse / Neutre / Baisse]  Magnitude : [Faible / Modérée / Forte]

H2 — [libellé] :
  E était-il attendu sous H2 ? [...]
  → Révision : [...]  Magnitude : [...]

H3 — [libellé] :
  E était-il attendu sous H3 ? [...]
  → Révision : [...]  Magnitude : [...]

VERDICT GLOBAL :
  Hypothèse renforcée : [Hx]
  Hypothèse affaiblie  : [Hy]
  Hypothèse inchangée  : [Hz]
```

---

## 6. Règles de conversion qualitative → quantitative

Si après le tableau qualitatif l'utilisateur souhaite une mise à jour chiffrée approximative, appliquer ces conversions :

| Révision qualitative | Δ P approximatif (depuis P = 0.50) |
|---------------------|-----------------------------------|
| Forte hausse | +0.20 à +0.35 |
| Modérée hausse | +0.10 à +0.20 |
| Faible hausse | +0.03 à +0.10 |
| Neutre | 0 |
| Faible baisse | −0.03 à −0.10 |
| Modérée baisse | −0.10 à −0.20 |
| Forte baisse | −0.20 à −0.35 |

**Note** : ces Δ sont donnés autour de P = 0.50. Pour des priors éloignés de 0.50, l'effet est asymétrique (voir sensibilité au prior dans `ethique-limites.md`).

---

## 7. Quand passer du qualitatif au quantitatif

Règle de bascule : si l'observation a un impact potentiel qui changerait une décision, formaliser en Mode 1 ou Mode 2.

Questions pratiques :
- "Est-ce que cette révision change l'hypothèse dominante ?" → Formaliser.
- "Est-ce que cette révision dépasse ±0.15 ?" → Formaliser.
- "Est-ce que je veux logger cette révision dans Calibration Engine ?" → Formaliser (les logs qualitatifs ne sont pas scorables).

---

## 8. Bayes qualitatif comme hygiène mentale quotidienne

L'objectif du raisonnement qualitatif n'est pas de remplacer le calcul formel mais de rendre la **mise à jour un réflexe permanent** :

> À chaque nouvelle information, demander : *"Est-ce que ça confirme ou infirme mes hypothèses ? De combien ? Pourquoi ?"*

Ce réflexe, pratiqué systématiquement, évite les deux erreurs opposées :
- **La rigidité** : ne pas réviser du tout malgré des signaux forts.
- **La réactivité** : sur-réviser à chaque nouveau signal médiatique.

Tetlock a montré que les superforecasters révisent **fréquemment et modestement** plutôt que rarement et fortement. Le mode qualitatif encourage précisément ce pattern.
