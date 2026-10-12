"""Tests de non-régression : chaque exemple chiffré du skill est recalculé ici.

Lancer :  python3 -m unittest discover -s tests -v   (depuis la racine du skill)
"""
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import bayes  # noqa: E402


class TestMode1(unittest.TestCase):
    def test_exemple_skill_mode1(self):
        r = bayes.posterior(0.60, 0.85, 0.25)
        self.assertAlmostEqual(r["p_e"], 0.610, places=6)
        self.assertAlmostEqual(r["posterior"], 0.836, places=3)
        self.assertAlmostEqual(r["bayes_factor"], 3.40, places=6)
        self.assertEqual(bayes.label_bf(3.40)["libelle"], "modéré")

    def test_prior_extreme(self):
        # theorie-bayesienne.md §4.1 : prior 0.01, BF 100 → 100/199 ≈ 0.503 (le texte original arrondissait à 0.502)
        o = bayes.odds(0.01) * 100
        self.assertAlmostEqual(bayes.prob(o), 100 / 199, places=12)

    def test_sensibilite_ethique(self):
        # ethique-limites.md §1 : 0.30/BF5 → 0.68 ; 0.70/BF5 → 0.92
        self.assertAlmostEqual(bayes.prob(bayes.odds(0.30) * 5), 0.68, places=2)
        self.assertAlmostEqual(bayes.prob(bayes.odds(0.70) * 5), 0.92, places=2)

    def test_sensibilite_elicitation(self):
        # elicitation-vraisemblances.md §8 (nominal : 0.85 / 0.25)
        self.assertAlmostEqual(bayes.posterior(0.60, 0.85, 0.25)["posterior"], 0.84, places=2)
        self.assertAlmostEqual(bayes.posterior(0.60, 0.55, 0.35)["posterior"], 0.70, places=2)
        self.assertAlmostEqual(bayes.posterior(0.60, 0.95, 0.10)["posterior"], 0.93, places=2)
        self.assertEqual(bayes.label_bf(9.5)["libelle"], "modéré")


class TestSequence(unittest.TestCase):
    def test_chaine_odds(self):
        s = bayes.sequence(0.60, [3.40, 0.40, 8.00])
        self.assertAlmostEqual(s[0]["probabilite"], 0.836, places=3)
        self.assertAlmostEqual(s[1]["probabilite"], 0.671, places=3)
        self.assertAlmostEqual(s[2]["probabilite"], 0.942, places=3)


class TestMode2(unittest.TestCase):
    def test_exemple_skill_mode2(self):
        r = bayes.multi_update([0.60, 0.25, 0.15], [0.85, 0.70, 0.15])
        self.assertAlmostEqual(r["p_e"], 0.7075, places=6)
        p = [round(x, 3) for x in r["posteriors"]]
        self.assertEqual(p, [0.721, 0.247, 0.032])
        d = [round(x, 3) for x in r["deltas"]]
        self.assertEqual(d, [0.121, -0.003, -0.118])
        self.assertAlmostEqual(sum(r["posteriors"]), 1.0, places=12)

    def test_exemple_reference_multi(self):
        # mise-a-jour-multi-hypotheses.md §4
        r = bayes.multi_update([0.60, 0.25, 0.15], [0.65, 0.15, 0.88])
        self.assertAlmostEqual(r["p_e"], 0.5595, places=6)
        self.assertEqual([round(x, 3) for x in r["posteriors"]], [0.697, 0.067, 0.236])
        self.assertEqual([round(x, 2) for x in r["bf_vs_rest"]], [1.53, 0.22, 1.75])

    def test_somme_toujours_un(self):
        r = bayes.multi_update([0.5, 0.3, 0.2], [0.33, 0.91, 0.07])
        self.assertAlmostEqual(r["sum_posteriors"], 1.0, places=12)

    def test_priors_non_normalises_refuses(self):
        with self.assertRaises(ValueError):
            bayes.multi_update([0.6, 0.3, 0.3], [0.5, 0.5, 0.5])

    def test_vraisemblances_nulles_refusees(self):
        with self.assertRaises(ValueError):
            bayes.multi_update([0.5, 0.5], [0.0, 0.0])


class TestMode3(unittest.TestCase):
    def test_audit_exemple_skill(self):
        # SKILL.md MODE 3 — PRED-2026-05-14-001, vraisemblances rétro-estimées
        r1 = bayes.posterior(0.65, 0.60, 0.25)
        self.assertAlmostEqual(r1["posterior"], 0.817, places=3)
        self.assertGreater(r1["posterior"] - 0.75, 0.05)       # → sous-révisée
        r2 = bayes.posterior(0.75, 0.50, 0.40)
        self.assertAlmostEqual(r2["posterior"], 0.789, places=3)
        self.assertLess(abs(0.80 - r2["posterior"]), 0.05)     # → cohérente


class TestCapNarrativeAttractor(unittest.TestCase):
    def test_ancien_plafond_incoherent(self):
        # 0.75/0.40 = 1.875 autorise une hausse > 0.10 : l'ancienne règle était incohérente
        self.assertGreater(bayes.max_delta_for_bf(0.75 / 0.40), 0.15)

    def test_plafond_coherent(self):
        cap = bayes.bf_cap_for_delta(0.10)
        self.assertAlmostEqual(cap, 1.4938, places=3)
        self.assertAlmostEqual(bayes.max_delta_for_bf(cap), 0.10, places=9)
        # BF 0.75/0.50 = 1.5 ≈ plafond (Δmax ≈ 0.101)
        self.assertLess(bayes.max_delta_for_bf(1.5), 0.102)

    def test_apply_cap(self):
        r = bayes.apply_delta_cap(0.55, 0.70, 0.10)
        self.assertAlmostEqual(r["posterior_plafonne"], 0.65, places=9)
        self.assertTrue(r["plafond_applique"])


class TestLabels(unittest.TestCase):
    def test_symetrie(self):
        self.assertEqual(bayes.label_bf(0.0625)["libelle"], "fort")
        self.assertEqual(bayes.label_bf(0.0625)["direction"], "contre H")
        self.assertEqual(bayes.label_bf(16)["libelle"], "fort")
        self.assertEqual(bayes.label_bf(150)["libelle"], "décisif")
        self.assertEqual(bayes.label_bf(1.45)["libelle"], "anecdotique")

    def test_log_bf(self):
        self.assertAlmostEqual(bayes.log_bf(100), 2.0)
        self.assertAlmostEqual(bayes.log_bf(math.sqrt(10)), 0.5)


if __name__ == "__main__":
    unittest.main()
