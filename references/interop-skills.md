# Interopérabilité avec les autres skills

Ce fichier décrit comment le Bayesian Updater s'interface avec les autres skills de l'écosystème IRIS∞ : les skills du cluster prédictif (`superforecasting-protocol`, `calibration-engine`, `prediction-engine`) et des skills **externes à ce dépôt** (*Signaux du Futur*, *Miroir Trans-échelle*, *Hacking Narratif*, *Fractales du Destin*). Ces derniers ne sont pas livrés ici : les interfaces décrites supposent qu'ils sont installés séparément.

---

## Architecture de flux

```
Superforecasting Protocol ─────────────┐
Signaux du Futur (externe) ────────────┤
  (hypothèses H1/H2/H3 + probas)       │
                                        ▼
Miroir Trans-échelle (externe) ►  BAYESIAN UPDATER
  (convergences P3 avec probas)         │
                                        │ posteriors
                                        ▼
                              Calibration Engine
                              (log des révisions)
```

Le Bayesian Updater est un **middleware** : il reçoit des analyses produites en amont, les met à jour, et transmet les résultats en aval.

---

## 1. Interface avec `signaux-du-futur`

### Ce qui est fourni par Signaux

*Signaux du Futur* produit systématiquement (en mode autonome ou étendu) :
- Trois hypothèses concurrentes H1, H2, H3 avec probabilités
- Des indicateurs de bascule attachés à chaque scénario
- Un ou plusieurs signaux faibles identifiés

Ce format est **directement compatible** avec le Mode 2 (multi-hypothèses) du Bayesian Updater.

### Déclenchement

Quand *Signaux* a été exécuté et qu'un signal nouveau arrive, le Bayesian Updater est invoqué avec :

```
[Hypothèses de Signaux]
H1 — [libellé]  P = 0.60
H2 — [libellé]  P = 0.25
H3 — [libellé]  P = 0.15

[Observation nouvelle]
E = [description précise du signal ou de l'événement]
```

### Sortie vers Signaux

Le Bayesian Updater produit les posteriors P(Hk|E) qui **remplacent** les priors dans la prochaine itération de Signaux. L'utilisateur copie les posteriors dans son log de dossier pour la prochaine session Signaux.

---

## 2. Interface avec `miroir-trans-echelle`

### Observations loggables issues de Miroir

La Passe 3 (carte de résonance) de Miroir Trans-échelle peut produire des **convergences fortes** entre lecture symbolique et analytique. Ces convergences constituent des observations mises à jour en bayésien, avec précautions.

**Règle du cap narrative attractor** (commune avec `references/interop-skills.md` de `calibration-engine`) :

> Une convergence forte P1+P2 dans Miroir Trans-échelle ne peut augmenter la probabilité OSINT de base de plus de **+0.10**, quel que soit le prior.

**Correction (v1.1).** La version 1.0 imposait P(E|H) ≤ 0.75 et P(E|¬H) ≥ 0.40, soit BF ≤ 1.875. Or la hausse maximale qu'un BF peut produire sur l'ensemble des priors vaut (√BF − 1)/(√BF + 1) : pour BF = 1.875, elle atteint **+0.156**, ce qui viole le plafond annoncé. Pour garantir Δ ≤ +0.10, il faut BF ≤ ((1 + 0.10)/(1 − 0.10))² ≈ **1.49**.

**Procédure** :

1. Identifier la convergence forte dans la carte de résonance.
2. Formuler E : *"La lecture symbolique et la lecture OSINT convergent sur [dynamique X]."*
3. Éliciter les vraisemblances auprès de l'utilisateur, dans les bornes :
   - P(E|H) ≤ 0.75 (limiter la vraisemblance symbolique) ;
   - P(E|¬H) ≥ 0.50 (une convergence narrative est fréquente même quand H est fausse).
   Ces bornes donnent BF ≤ 1.5, soit une hausse maximale ≈ +0.101.
4. Calculer avec `scripts/bayes.py simple`, puis tronquer le posterior à prior + 0.10 si nécessaire (`apply_delta_cap`). Consigner la troncature dans le motif de révision.
5. Vérification : `python3 scripts/bayes.py cap --delta 0.10` renvoie le BF maximal compatible.

**Une dissonance** (P3) produit une observation de type "signal mixte" : elle ne bascule pas fortement dans un sens, mais peut invalider une hypothèse trop certaine.

---

## 3. Interface avec `calibration-engine`

### Le flux de sortie principal

Toute mise à jour bayésienne formelle (Mode 1 ou Mode 2) génère une **entrée de révision** à verser dans le `calibration-log.md`. Format :

```yaml
# Révision à ajouter dans l'entrée de la prédiction concernée
revisions:
  - date: [date ISO]
    probabilite_avant: [prior]
    probabilite_apres: [posterior]
    motif: >
      Mise à jour bayésienne — BF=[valeur] — observation: [E courte]
    source: "[source de l'observation]"
    methode: bayesienne_formelle
    bf: [valeur numérique]
    p_e_sachant_h: [valeur]
    p_e_sachant_non_h: [valeur]
```

Le champ `methode: bayesienne_formelle` permet au Calibration Engine de distinguer les révisions bayésiennes formelles des révisions intuitives, pour l'audit de Mode 3.

### Flux d'information inverse

Le Calibration Engine peut alimenter le Bayesian Updater dans le Mode 3 (audit de cohérence). L'utilisateur fournit le `calibration-log.md` et le Bayesian Updater extrait les révisions passées pour les auditer.

---

## 4. Interface avec `hacking-narratif`

*Hacking Narratif* Mode B produit parfois des analyses de récits collectifs qui peuvent constituer des observations bayésiennes indirectes.

**Exemple** : une analyse HN révèle que le récit dominant sur X est en train de changer. C'est une observation potentiellement pertinente pour une hypothèse de type "changement de perception" ou "rupture narrative".

**Procédure** : traiter comme une observation de type C (dissonance narrative) du mode qualitatif. Vraisemblances à estimer prudemment — le changement de récit peut précéder ou suivre le changement réel.

---

## 5. Protocole de session multi-skills

Quand plusieurs skills sont utilisés dans la même session et qu'une chaîne d'analyse se déroule :

**Ordre recommandé** :

```
1. Signaux du Futur ou Miroir Trans-échelle
   → Production des hypothèses initiales + probas

2. Bayesian Updater (au fil des nouvelles informations qui arrivent)
   → Mise à jour des probas

3. Calibration Engine (en fin de session)
   → Enregistrement des prédictions finales + toutes les révisions
```

**Instruction en début de session** pour activer ce workflow :

> *"Active Bayesian Updater en mode veille : chaque fois qu'un signal nouveau est mentionné dans la session, propose automatiquement une mise à jour bayésienne des hypothèses en cours."*

---

## 6. Format de passation entre sessions

L'état des hypothèses est maintenu dans un **log de dossier** tenu par l'utilisateur : selon l'environnement, l'agent peut ne pas disposer de mémoire entre sessions, et le log reste dans tous les cas la référence auditable. Format recommandé :

```markdown
# Dossier [Nom] — État des hypothèses

**Dernière mise à jour** : [date]

| Hypothèse | Probabilité actuelle | Dernière révision |
|-----------|---------------------|------------------|
| H1 — [libellé] | 0.697 | 2026-06-15 (BF contre le reste = 1.53) |
| H2 — [libellé] | 0.067 | 2026-06-15 (BF contre le reste = 0.22) |
| H3 — [libellé] | 0.236 | 2026-06-15 (BF contre le reste = 1.75) |

*(Valeurs reprises de l'exemple de `mise-a-jour-multi-hypotheses.md` §4. Les BF « contre le reste » dépendent des priors des autres hypothèses ; les noter avec les vraisemblances qui les produisent.)*

**Indicateurs de bascule actifs** :
- [Indicateur A] — non déclenché
- [Indicateur B] — déclenché le [date] → intégré dans révision du [date]

**Prochaines observations à surveiller** :
- [...]
```

Ce fichier est fourni en contexte à chaque session pour reprendre là où on s'est arrêté.

---

## 7. Tableau de compatibilité

| Skill | Direction | Format |
|-------|-----------|--------|
| `superforecasting-protocol` | → vers Updater | Scénarios MECE + probas (fiche de prédiction) |
| `signaux-du-futur` *(externe)* | → vers Updater | Hypothèses + probas |
| `miroir-trans-echelle` *(externe)* | → vers Updater | Convergences P3 (BF ≤ 1.49, Δ ≤ +0.10) |
| `calibration-engine` | ← depuis Updater | Révisions YAML |
| `calibration-engine` | → vers Updater (Mode 3) | Log complet pour audit |
| `hacking-narratif` *(externe)* | → vers Updater (indirect) | Observations narratives |
| `fractales-du-destin` *(externe)* | Non directement | Prédictions dérivées seulement |
