#!/usr/bin/env python3
"""
bayes.py — Calculs bayésiens déterministes pour le skill bayesian-updater.

Le LLM ne calcule pas les posteriors « de tête » : il appelle ce script.
Aucune dépendance externe (bibliothèque standard uniquement).

Usage CLI (entrée et sortie JSON) :

  # Mode 1 — hypothèse unique
  python3 scripts/bayes.py simple --prior 0.60 --peh 0.85 --penh 0.25

  # Mode 2 — multi-hypothèses (priors et vraisemblances dans le même ordre)
  python3 scripts/bayes.py multi --priors 0.60 0.25 0.15 --likelihoods 0.85 0.70 0.15

  # Mises à jour séquentielles en odds (BF supposés conditionnellement indépendants)
  python3 scripts/bayes.py sequence --prior 0.60 --bfs 3.4 0.4 8

  # Analyse de sensibilité sur une grille de vraisemblances
  python3 scripts/bayes.py sensitivity --prior 0.60 --peh 0.55 0.85 0.95 --penh 0.10 0.25 0.35

  # Plafond « narrative attractor » : BF max garantissant Δ ≤ delta quel que soit le prior
  python3 scripts/bayes.py cap --delta 0.10
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Dict, List, Sequence

TOL = 1e-9

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def _check_prob(x: float, name: str, open_interval: bool = False) -> None:
    if not isinstance(x, (int, float)) or math.isnan(x):
        raise ValueError(f"{name} doit être un nombre, reçu {x!r}")
    if open_interval:
        if not 0.0 < x < 1.0:
            raise ValueError(f"{name} doit être dans ]0, 1[, reçu {x}")
    elif not 0.0 <= x <= 1.0:
        raise ValueError(f"{name} doit être dans [0, 1], reçu {x}")


# ---------------------------------------------------------------------------
# Conversions
# ---------------------------------------------------------------------------


def odds(p: float) -> float:
    """Probabilité → odds. p doit être dans ]0, 1[."""
    _check_prob(p, "p", open_interval=True)
    return p / (1.0 - p)


def prob(o: float) -> float:
    """Odds → probabilité."""
    if o < 0:
        raise ValueError("des odds ne peuvent pas être négatives")
    if math.isinf(o):
        return 1.0
    return o / (1.0 + o)


def log_bf(bf: float, base: str = "10") -> float:
    """Logarithme du Bayes Factor. base '10' → bans ; 'e' → nats ; '2' → bits."""
    if bf <= 0:
        raise ValueError("BF doit être > 0 pour prendre son logarithme")
    return {"10": math.log10, "e": math.log, "2": math.log2}[base](bf)


# ---------------------------------------------------------------------------
# Échelles d'interprétation (CONVENTIONS, pas des normes)
# ---------------------------------------------------------------------------

# Seuils 1-3-10-30-100 : Lee & Wagenmakers (2014) ; libellé « décisif » : Jeffreys (1961).
# C'est un hybride conventionnel. Jeffreys utilisait des demi-puissances de 10
# (≈3.2, 10, ≈31.6, 100) ; Kass & Raftery (1995) proposent 1-3-20-150.
_SCALE = [
    (1.0, "nul / neutre"),
    (3.0, "anecdotique"),
    (10.0, "modéré"),
    (30.0, "fort"),
    (100.0, "très fort"),
    (math.inf, "décisif"),
]


def label_bf(bf: float) -> Dict[str, str]:
    """Libellé conventionnel d'un BF (symétrique : BF<1 est lu comme 1/BF contre H)."""
    if bf <= 0:
        raise ValueError("BF doit être > 0")
    direction = "pour H" if bf > 1 else ("contre H" if bf < 1 else "neutre")
    strength = bf if bf >= 1 else 1.0 / bf
    if abs(strength - 1.0) < 1e-12:
        lab = "nul / neutre"
    else:
        lab = next(name for upper, name in _SCALE[1:] if strength <= upper)
    return {
        "libelle": lab,
        "direction": direction,
        "convention": "hybride Lee & Wagenmakers (2014) / Jeffreys (1961) — convention, pas une norme",
    }


# ---------------------------------------------------------------------------
# Mode 1 — hypothèse unique
# ---------------------------------------------------------------------------


def posterior(prior: float, peh: float, penh: float) -> Dict[str, float]:
    """P(H|E) à partir de P(H), P(E|H), P(E|¬H)."""
    _check_prob(prior, "prior", open_interval=True)
    _check_prob(peh, "P(E|H)")
    _check_prob(penh, "P(E|¬H)")
    pe = prior * peh + (1.0 - prior) * penh
    if pe <= 0:
        raise ValueError("P(E) = 0 : l'observation est impossible sous H et sous ¬H")
    post = prior * peh / pe
    bf = math.inf if penh == 0 else peh / penh
    return {
        "prior": prior,
        "p_e_given_h": peh,
        "p_e_given_not_h": penh,
        "p_e": pe,
        "posterior": post,
        "delta": post - prior,
        "bayes_factor": bf,
    }


# ---------------------------------------------------------------------------
# Mode 2 — multi-hypothèses
# ---------------------------------------------------------------------------


def multi_update(priors: Sequence[float], likelihoods: Sequence[float],
                 prior_tol: float = 0.01) -> Dict[str, object]:
    """Mise à jour simultanée de K hypothèses MECE.

    - priors : P(Hk), doivent sommer à 1 (± prior_tol), sinon erreur.
    - likelihoods : P(E|Hk).
    Les posteriors sont normalisés et leur somme est vérifiée à 1e-9 près.
    Retourne aussi, pour chaque k, le BF « contre le reste » :
        BF_k = P(E|Hk) / P(E|¬Hk),  avec  P(E|¬Hk) = Σ_{j≠k} P(Hj)P(E|Hj) / (1 − P(Hk)).
    """
    if len(priors) != len(likelihoods) or len(priors) < 2:
        raise ValueError("il faut au moins 2 hypothèses et autant de vraisemblances que de priors")
    for i, p in enumerate(priors):
        _check_prob(p, f"prior H{i + 1}")
    for i, l in enumerate(likelihoods):
        _check_prob(l, f"P(E|H{i + 1})")
    s = sum(priors)
    if abs(s - 1.0) > prior_tol:
        raise ValueError(f"les priors somment à {s:.4f} ≠ 1 : demander un ajustement avant de continuer")
    priors = [p / s for p in priors]  # absorbe l'arrondi toléré

    nums = [p * l for p, l in zip(priors, likelihoods)]
    pe = sum(nums)
    if pe <= 0:
        raise ValueError("P(E) = 0 : aucune hypothèse ne rend l'observation possible — ajouter une hypothèse")
    posts = [n / pe for n in nums]
    total = sum(posts)
    assert abs(total - 1.0) < TOL, f"normalisation violée : somme = {total}"

    bf_vs_rest = []
    for k in range(len(priors)):
        rest_mass = 1.0 - priors[k]
        if rest_mass <= 0:
            bf_vs_rest.append(None)
            continue
        pe_not_k = (pe - nums[k]) / rest_mass
        bf_vs_rest.append(math.inf if pe_not_k == 0 else likelihoods[k] / pe_not_k)

    return {
        "priors": priors,
        "likelihoods": list(likelihoods),
        "numerators": nums,
        "p_e": pe,
        "posteriors": posts,
        "deltas": [q - p for p, q in zip(priors, posts)],
        "sum_posteriors": total,
        "bf_vs_rest": bf_vs_rest,
    }


def pairwise_bf(likelihoods: Sequence[float]) -> List[List[float]]:
    """Matrice BF(Hi vs Hj) = P(E|Hi)/P(E|Hj)."""
    return [[(li / lj if lj > 0 else math.inf) for lj in likelihoods] for li in likelihoods]


# ---------------------------------------------------------------------------
# Séquences, sensibilité, plafonds
# ---------------------------------------------------------------------------


def sequence(prior: float, bfs: Sequence[float]) -> List[Dict[str, float]]:
    """Mises à jour successives en odds. Suppose l'indépendance conditionnelle des observations."""
    o = odds(prior)
    out = []
    for i, bf in enumerate(bfs, 1):
        if bf <= 0:
            raise ValueError("chaque BF doit être > 0")
        o *= bf
        out.append({"etape": i, "bf": bf, "odds": o, "probabilite": prob(o)})
    return out


def sensitivity(prior: float, pehs: Sequence[float], penhs: Sequence[float]) -> List[Dict[str, float]]:
    """Grille de posteriors pour toutes les combinaisons (P(E|H), P(E|¬H))."""
    return [posterior(prior, a, b) for a in pehs for b in penhs]


def max_delta_for_bf(bf: float) -> float:
    """Hausse maximale de probabilité qu'un BF ≥ 1 peut produire, sur tous les priors.

    Δ(p) = p·BF/(1 − p + p·BF) − p, maximal en p* = 1/(1+√BF) ; Δmax = (√BF − 1)/(√BF + 1).
    """
    if bf < 1:
        raise ValueError("défini pour BF ≥ 1")
    r = math.sqrt(bf)
    return (r - 1.0) / (r + 1.0)


def bf_cap_for_delta(delta: float) -> float:
    """BF maximal garantissant une hausse ≤ delta quel que soit le prior (inverse de max_delta_for_bf)."""
    if not 0 < delta < 1:
        raise ValueError("delta doit être dans ]0, 1[")
    r = (1.0 + delta) / (1.0 - delta)
    return r * r


def apply_delta_cap(prior: float, post: float, delta: float = 0.10) -> Dict[str, float]:
    """Plafonne la hausse d'une mise à jour (règle narrative attractor)."""
    capped = min(post, prior + delta) if post > prior else post
    return {"prior": prior, "posterior_brut": post, "posterior_plafonne": capped,
            "plafond_applique": capped < post}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _json_default(o):
    if isinstance(o, float) and math.isinf(o):
        return "inf"
    raise TypeError


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("simple")
    a.add_argument("--prior", type=float, required=True)
    a.add_argument("--peh", type=float, required=True)
    a.add_argument("--penh", type=float, required=True)

    b = sub.add_parser("multi")
    b.add_argument("--priors", type=float, nargs="+", required=True)
    b.add_argument("--likelihoods", type=float, nargs="+", required=True)

    c = sub.add_parser("sequence")
    c.add_argument("--prior", type=float, required=True)
    c.add_argument("--bfs", type=float, nargs="+", required=True)

    d = sub.add_parser("sensitivity")
    d.add_argument("--prior", type=float, required=True)
    d.add_argument("--peh", type=float, nargs="+", required=True)
    d.add_argument("--penh", type=float, nargs="+", required=True)

    e = sub.add_parser("cap")
    e.add_argument("--delta", type=float, default=0.10)

    args = ap.parse_args(argv)
    try:
        if args.cmd == "simple":
            res = posterior(args.prior, args.peh, args.penh)
            res["interpretation_bf"] = label_bf(res["bayes_factor"]) if res["bayes_factor"] != math.inf else None
        elif args.cmd == "multi":
            res = multi_update(args.priors, args.likelihoods)
            res["bf_paires"] = pairwise_bf(args.likelihoods)
        elif args.cmd == "sequence":
            res = sequence(args.prior, args.bfs)
        elif args.cmd == "sensitivity":
            res = sensitivity(args.prior, args.peh, args.penh)
        else:
            cap = bf_cap_for_delta(args.delta)
            res = {"delta": args.delta, "bf_max": cap, "verification_delta_max": max_delta_for_bf(cap)}
    except ValueError as exc:
        print(json.dumps({"erreur": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(res, ensure_ascii=False, indent=2, default=_json_default))
    return 0


if __name__ == "__main__":
    sys.exit(main())
