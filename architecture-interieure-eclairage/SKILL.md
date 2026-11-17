---
name: architecture-interieure-eclairage
description: Préparer un aménagement intérieur et un éclairage à partir de plans, photos et mesures ; comparer des luminaires, estimer les lux et produire une implantation ou un visuel. Pour des pièces réelles, pas pour les interfaces web, les scènes de jeu vidéo ou le calcul de structure.
---

# Architecture intérieure et éclairage

Proposer une implantation réalisable qui répond aux usages et au budget, en réutilisant l’existant. Adapter la profondeur du travail à la demande : un avis sur un plafonnier ne nécessite pas de refaire tout le projet.

## Partir des informations disponibles

- Consulter les plans et relevés déjà fournis avant de redemander des dimensions. Une photo renseigne sur les obstacles et la disposition ; elle ne fournit pas une hauteur mesurée.
- Distinguer les mesures confirmées, les observations, les valeurs de fabricant et les hypothèses. Ne pas remplacer une cote confirmée par une dimension commode pour dessiner.
- Relever les usages simultanés, les zones réellement éclairées, les hauteurs de pose et de travail, fenêtres, poutres, étagères, matériaux, équipements réutilisables, alimentation et budget.
- Progresser sur les parties indépendantes des données manquantes. Demander seulement ce qui change le choix ou le dimensionnement ; conserver une implantation provisoire si les hauteurs restent inconnues.

Pour l’aménagement ou les circulations, lire [amenagement.md](references/amenagement.md). Pour structurer un dossier, utiliser les champs de [dossier-projet.md](references/dossier-projet.md), sans imposer un long formulaire à une demande simple.

## Concevoir l’éclairage par usage

Lire [eclairage.md](references/eclairage.md) avant un calcul ou une comparaison technique.

- Séparer éclairage général, éclairage des tâches et mise en valeur, avec des commandes adaptées aux usages. Une zone de travail mérite son propre examen même si la moyenne de la pièce semble suffisante.
- Examiner les ombres de l’utilisateur, des poutres et des meubles, ainsi que l’éblouissement et les reflets aux positions assises et debout. Éviter de placer la source au-dessus d’un obstacle qui masque la tâche.
- Conserver les marques et protocoles demandés. Comparer diamètre, encombrement, flux au réglage utile, diffusion, rendu des couleurs documenté, variation, entretien et coût complet. Ne pas déduire une meilleure répartition du seul diamètre.
- Vérifier les caractéristiques sur la fiche fabricant de la référence exacte. Les tarifs d’une capture sont les tarifs de cette capture ; dater les prix recherchés. Compter rails, alimentations et raccords quand ils sont nécessaires.
- Déduire de la liste d’achats les équipements déjà présents. Sans photométrie ou mesure, ne pas compter tout le flux d’un ruban décoratif caché comme éclairage utile du plan de travail.

## Chiffrer avec des limites explicites

Utiliser `scripts/lumen_method.py --help` puis le calculateur pour une estimation moyenne. Exiger surface éclairée, flux par luminaire, facteur d’utilisation UF et facteur de maintenance MF. L’un des paramètres quantité ou cible en lux est nécessaire.

Les facteurs ne sont pas des constantes universelles. S’ils sont inconnus, présenter des scénarios explicitement supposés ou attendre les données utiles. Le script ne mesure pas UF et ne déduit pas MF de photos. Employer le flux du luminaire complet à la température de couleur et au régime retenus, sans inventer un flux à partir d’un pourcentage dans une application.

Présenter le résultat comme une moyenne estimée. Le minimum arithmétique ne valide ni le nombre final de points, ni leur implantation. Pour un volume haut, une mezzanine, des obstacles importants ou une exigence d’uniformité, passer à une étude point par point avec géométrie et fichiers photométriques appropriés si disponibles. Sinon, expliquer ce qui reste incertain et proposer un essai mesuré.

Les valeurs de confort choisies pour un logement ne constituent pas une conformité réglementaire. Pour un besoin réglementaire, vérifier juridiction, usage, édition applicable et référence exacte avec les [sources](references/sources.md).

## Montrer et livrer

Pour un montage ou un rendu, lire [visuels.md](references/visuels.md). Conserver la pièce, les équipements et le nombre de luminaires proposés ; signaler les positions approximatives. Une image générée illustre une ambiance, elle ne démontre pas un niveau de lux.

Livrer, selon la demande : implantation légendée, raison du choix, hypothèses chiffrées, liste d’achats et coût complet, points à confirmer et une prochaine action utile. Les fonctions d’automatisation, achats, travaux ou publications nécessitent le périmètre autorisé par l’utilisateur ; un conseil ne déclenche pas ces actions.

Garder les dossiers réels privés. Tout exemple destiné à un dépôt public doit être fictif et indépendant de plans, photos, mesures et identifiants de clients. Les références ci-dessous guident l’analyse ; elles ne remplacent pas une inspection des supports et du raccordement avant travaux.
