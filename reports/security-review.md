# Revue de sécurité du skill

Contrôle effectué le 17 novembre 2026 avec **NVIDIA SkillSpector 2.12.0**, source officielle épinglée au commit `a09091e0ebf6c96ff327457529d7b0d372125884`. Mode statique `--no-llm` ; aucun appel LLM, aucune baseline et aucune exclusion de fichiers dans les périmètres annoncés.

| Périmètre | Fichiers analysés | Couverture statique | Score | Recommandation du scanner | Constats |
|---|---:|---:|---:|---|---|
| [Skill installable](skillspector-static.json) | 8/8 | 100 % | 0/100 | SAFE | Aucun |
| [Tests de développement](skillspector-tests.json) | 1/1 | 100 % | 23/100 | CAUTION | Trois alertes modérées : AST3 × 2, AST4 × 1 |

## Changements depuis la première revue

La [première version publique](https://github.com/autogpt-elendir/codex-skills/tree/afd501a0d070d26d96e06fecdd5a6c96b4e7b3eb/architecture-interieure-eclairage) regroupait le skill et ses tests. Son scan statique donnait 38/100, cinq alertes modérées : LP3 pour la portée non déclarée, AE4 pour une notation mathématique grecque, deux AST3 pour l’import du calculateur par les tests et AST4 pour les tests de l’interface CLI.

Le dossier installable contient maintenant les instructions, les références et le calculateur autonome. Son périmètre d’exécution est décrit dans [SKILL.md](../architecture-interieure-eclairage/SKILL.md). Les métadonnées n’accordent aucune préautorisation d’outil. Les tests sont conservés à la racine du dépôt dans `tests/`, exécutés en CI et analysés séparément. Les formules utilisent des noms explicites `flux_luminaire` et `flux_total_requis` ; les calculs restent identiques.

## Revue des tests

Les deux AST3 correspondent au chargement du calculateur local, situé par un chemin fixe dérivé du fichier de tests. AST4 correspond au lancement de l’interpréteur Python et de ce même calculateur avec une liste d’arguments de test. Le lancement indique `shell=False` et un délai maximal. Aucune commande, URL ou nom de module n’est choisi depuis une entrée utilisateur. Ces trois constats du scanner sont conservés avec le verdict CAUTION pour les outils de développement.

## Reproduire

Après installation d’une version de SkillSpector compatible, depuis la racine du dépôt :

```bash
skillspector scan architecture-interieure-eclairage --no-llm --format json \
  --output skill-report.json --fail-on-incomplete --fail-on-findings
skillspector scan tests/test_lumen_method.py --no-llm --format json \
  --output tests-report.json --fail-on-incomplete --fail-on-findings
```

Le scan du skill se termine avec le code 0. Celui des tests se termine avec le code 1, lié aux trois constats et à `--fail-on-findings` ; les deux analyses sont complètes et réussies. Les JSON de ce dossier sont des synthèses structurées des rapports, avec les empreintes des fichiers analysés. Les rapports bruts peuvent contenir des chemins de machine ; ils ne sont pas redistribués ici.

Empreinte du manifeste trié des huit fichiers du skill : `fa6bcc38bfc66917e1eed1566745bb2318da2b71d59913a7fa30e1c38aaed4cb` (SHA256 du JSON compact de `files_sha256`, clés triées et séparateurs `,`/`:`).

Ce résultat couvre les fichiers et révisions indiqués. Le scanner n’atteste pas la qualité photométrique d’un projet et ce rapport ne constitue pas une certification NVIDIA-Verified. Les fichiers de documentation du dépôt et le workflow CI sont hors du périmètre installable ; les actions CI sont épinglées à leurs commits et le calculateur ne dépend que de Python standard.
