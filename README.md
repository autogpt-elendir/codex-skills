# Skills d’aménagement intérieur et d’éclairage

Des skills en français pour préparer un aménagement à partir de mesures, comparer des luminaires et expliquer les limites des estimations.

## Skill disponible

[architecture-interieure-eclairage](architecture-interieure-eclairage/SKILL.md) accompagne les projets de pièces de vie, espaces polyvalents et ateliers domestiques : relevé de l’existant, circulation, implantation, choix des sources, budget et visuels.

- Conserve les équipements réutilisables et distingue mesures, observations et hypothèses.
- Calcule un éclairement moyen estimé avec des facteurs d’utilisation et de maintenance explicites.
- Traite séparément l’éclairage général, le travail et l’ambiance, sans affecter tout le flux d’une pièce à un petit établi.
- Préserve la géométrie et les matériaux lors des montages photo.
- Ne suppose aucune marque, API payante, automatisation ou installation électrique.

Le calculateur fonctionne hors ligne avec Python 3.11 ou plus récent, sans dépendance externe. L’agent peut consulter des sources publiques pour vérifier des produits ; le calculateur ne transmet aucune donnée.

## Utilisation avec un agent

Installer le dossier `architecture-interieure-eclairage` avec l’installateur de skills de l’agent. Pour Codex, on peut demander :

> Utilise $skill-installer pour installer https://github.com/autogpt-elendir/codex-skills/tree/main/architecture-interieure-eclairage

Puis invoquer :

> Utilise $architecture-interieure-eclairage pour proposer l’éclairage de cette pièce en conservant les équipements existants. Commence par les mesures disponibles et les informations manquantes.

Les références sont chargées selon la tâche. Aucun service d’images n’est obligatoire : si l’agent dispose d’un outil de génération, la référence sur les visuels explique comment l’utiliser sans confondre illustration et simulation.

## Exemple fictif de calcul

Une zone rectangulaire fictive de 24 m², des luminaires fictifs de 2 400 lm, une cible choisie pour l’exercice de 200 lx, un facteur d’utilisation supposé de 0,60 et un facteur de maintenance supposé de 0,80 :

```bash
python3 architecture-interieure-eclairage/scripts/lumen_method.py \
  --area-m2 24 --lumens-per-fixture 2400 \
  --utilization-factor 0.60 --maintenance-factor 0.80 \
  --target-lux 200
```

Le résultat est **5 luminaires au minimum arithmétique** et **240 lx de moyenne estimée** avec cette quantité. Ce résultat ne valide ni leur position, ni les zones d’ombre, ni l’uniformité, ni l’éblouissement. Les facteurs et la cible sont des hypothèses d’exercice, pas des valeurs par défaut pour une pièce réelle.

Pour évaluer une quantité existante, utiliser `--fixtures 4`. Les deux options peuvent être combinées pour comparer l’existant à une cible.

## Vérification

Depuis la racine du dépôt :

```bash
python3 -m unittest discover -s architecture-interieure-eclairage/tests -v
python3 architecture-interieure-eclairage/scripts/lumen_method.py --help
```

Une intégration GitHub Actions exécute les tests sur plusieurs versions de Python. Les tests vérifient les calculs et les entrées, pas une certification du projet d’éclairage.

## Sources et confidentialité

Les [sources primaires](architecture-interieure-eclairage/references/sources.md) sont liées et datées. La rédaction et le calculateur de ce dépôt sont originaux. Les skills communautaires examinés ont servi à identifier le besoin, sans reprise de leur texte ou de leur code.

Les exemples publiés sont fictifs. Garder plans habités, photos, mesures, devis nominatifs et identifiants domotiques dans un dossier privé séparé ; les fournir à un service externe seulement si cela entre dans la demande et les choix de l’utilisateur.

Licence : [MIT](LICENSE).
