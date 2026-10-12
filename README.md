# 📐 Bayesian Updater — Skill de mise à jour probabiliste

> *"Une nouvelle information ne remplace pas l'analyse précédente. Elle la corrige, proportionnellement à sa force."*

Un skill Claude qui applique formellement le **théorème de Bayes** à la mise à jour d'hypothèses analytiques. Quand une observation nouvelle arrive, ce skill calcule le posterior (par un script déterministe, `scripts/bayes.py`), quantifie la force de l'évidence (Bayes Factor, relatif à une alternative explicite), et préserve la trace de chaque révision. Il transforme la mise à jour intuitive — souvent biaisée — en opération mathématiquement contrôlée.

---

## Positionnement

Presque tous les analystes révisent leurs opinions quand de nouvelles informations arrivent. Presque aucun ne le fait formellement. Résultat : des révisions sous-estimées (biais d'ancrage), des révisions sur-estimées (biais de récence), ou des remplacements complets de l'analyse — sans trace, sans justification.

Le Bayesian Updater impose la discipline suivante :

> Donner son prior → estimer la vraisemblance de l'observation sous chaque hypothèse → calculer le posterior → tracer la révision.

Cette discipline vise un comportement que la recherche associe à la précision prédictive : les prévisionnistes les plus précis du Good Judgment Project révisent souvent et par petits pas (Atanasov et al., 2020). Le skill n'en garantit pas le bénéfice : il rend les révisions explicites, cohérentes avec leurs inputs et auditables.

---

## Ce que produit le skill

Trois modes opérationnels :

| Mode | Entrée | Sortie |
|------|--------|--------|
| **Mise à jour simple** | P(H) + observation + vraisemblances | P(H\|E) calculé + BF + interprétation |
| **Mise à jour multi-hypothèses** | Tableau H1/H2/H3 + observation | Tableau ACH-Bayes avec posteriors renormalisés |
| **Audit de révision** | Historique de révisions passées | Cohérence bayésienne des mises à jour antérieures |

---

## Cas d'usage typiques

- **Nouvelles informations sur un dossier en cours** : une démission, une fuite, un vote — de combien réviser ?
- **Mise à jour d'hypothèses concurrentes** (`superforecasting-protocol`, *Signaux du Futur*) : ce nouveau signal favorise-t-il H1, H2 ou H3 ?
- **Indicateur de bascule déclenché** (*Calibration Engine*) : un indicateur prévu vient d'apparaître — quel impact sur la proba ?
- **Entraînement bayésien** : s'exercer sur des cas pour internaliser le raisonnement.
- **Audit rétrospectif** : mes révisions passées étaient-elles cohérentes avec Bayes ?

---

## Carte du dépôt

```
bayesian-updater/
│
├── README.md                              ← Ce fichier (page du dépôt, non chargé par l'agent)
├── SKILL.md                               ← Agent principal (3 modes)
├── LICENSE                                ← GPL-3.0
├── scripts/
│   └── bayes.py                           ← Calculs déterministes (stdlib Python)
├── tests/
│   └── test_bayes.py                      ← Recalcul de chaque exemple du skill
│
└── references/
    ├── theorie-bayesienne.md              ← Formules, intuition, forme odds
    ├── elicitation-vraisemblances.md      ← Comment estimer P(E|H) pratiquement
    ├── mise-a-jour-multi-hypotheses.md    ← ACH-Bayes : tableau simultané
    ├── raisonnement-qualitatif.md         ← Bayes sans chiffres précis
    ├── interop-skills.md                  ← Connexion à Signaux, Miroir, Calibration
    └── ethique-limites.md                 ← Sensibilité au prior, limites pratiques
```

---

## Fondements scientifiques

| Référence | Apport |
|-----------|--------|
| Bayes & Price (1763) | Théorème fondateur, publié posthume |
| Laplace (1812) | Formalisation moderne de la probabilité inverse |
| Jeffreys (1961) ; Lee & Wagenmakers (2014) | Échelles conventionnelles d'interprétation du BF (hybride utilisé ici) |
| Kass & Raftery (1995) | Le BF comme rapport de vraisemblances entre deux modèles ; échelle alternative |
| Jaynes (2003) | *Probability Theory: The Logic of Science* |
| Heuer (1999) | ACH : matrice de mise à jour multi-hypothèses |
| Tetlock & Gardner (2015) | Mise à jour fréquente et graduelle comme compétence entraînable |
| Atanasov et al. (2020) | Les révisions par petits pas sont associées à une meilleure précision |
| Good (1950) | Formalisation du Bayes Factor comme unité d'évidence |

---

## Activation

Le déclenchement repose uniquement sur le champ `description` du `SKILL.md` (seul champ chargé à l'avance par les agents conformes à la spécification Agent Skills). Les formulations typiques : « mise à jour bayésienne », « que change cette information », « réviser cette hypothèse », « Bayes Factor », « poids de l'évidence ».

## Tests

```bash
python3 -m unittest discover -s tests -v
```

---

## Lien avec les autres skills

| Skill | Relation |
|-------|----------|
| `superforecasting-protocol` | Fournit les scénarios MECE probabilisés à mettre à jour |
| `calibration-engine` | Reçoit les posteriors comme révisions dans le log |
| `prediction-engine` | Orchestrateur qui route vers ce skill (Mode B) |
| `signaux-du-futur` *(externe, non livré ici)* | Fournit des hypothèses H1/H2/H3 |
| `miroir-trans-echelle` *(externe, non livré ici)* | Convergences P3 (plafond Δ ≤ +0.10) |

---

## Licence

GPL-3.0 — écosystème IRIS∞.

---

*« Le prior est votre état de connaissance avant l'observation. Le posterior est votre état après. Bayes est le pont entre les deux. »*
