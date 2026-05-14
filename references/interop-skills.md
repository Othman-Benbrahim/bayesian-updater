# Interopérabilité avec les autres skills

Ce fichier décrit comment le Bayesian Updater s'interface avec les autres skills de l'écosystème IRIS∞, en particulier *Signaux du Futur*, *Miroir Trans-échelle* et *Calibration Engine*.

---

## Architecture de flux

```
Signaux du Futur ──────────────────────┐
  (hypothèses H1/H2/H3 + probas)       │
                                        ▼
Miroir Trans-échelle ──────────►  BAYESIAN UPDATER
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

**Règle du cap narrative attractor** (reprise de `interop-skills.md` de Calibration Engine) :

> Une convergence forte P1+P2 dans Miroir Trans-échelle ne peut augmenter la probabilité OSINT de base de plus de **+0.10** via une mise à jour bayésienne.

**Procédure** :

1. Identifier la convergence forte dans la carte de résonance.
2. Formuler E : *"La lecture symbolique et la lecture OSINT convergent sur [dynamique X]."*
3. Estimer les vraisemblances en appliquant la règle :
   - P(E|H) ≤ 0.75 (limiter la vraisemblance symbolique)
   - P(E|¬H) ≥ 0.40 (ne pas sous-estimer la vraisemblance hors hypothèse)
4. Le BF résultant est plafonné à ≈ 1.5–2.0 — "modeste mais réel".

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

Comme Claude n'a pas de mémoire persistante, l'état des hypothèses est maintenu dans le **log de dossier** de l'utilisateur. Format recommandé :

```markdown
# Dossier [Nom] — État des hypothèses

**Dernière mise à jour** : [date]

| Hypothèse | Probabilité actuelle | Dernière révision |
|-----------|---------------------|------------------|
| H1 — [libellé] | 0.696 | 2026-06-15 (BF=3.2) |
| H2 — [libellé] | 0.068 | 2026-06-15 (BF=0.6) |
| H3 — [libellé] | 0.236 | 2026-06-15 (BF=5.9) |

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
| `signaux-du-futur` | → vers Updater | Hypothèses + probas |
| `miroir-trans-echelle` | → vers Updater | Convergences P3 (avec cap BF) |
| `calibration-engine` | ← depuis Updater | Révisions YAML |
| `calibration-engine` | → vers Updater (Mode 3) | Log complet pour audit |
| `hacking-narratif` | → vers Updater (indirect) | Observations narratives |
| `fractales-du-destin` | Non directement | Prédictions dérivées seulement |
