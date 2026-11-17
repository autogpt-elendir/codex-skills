# Éclairage : estimation et implantation

## Ce que les grandeurs signifient

- Le flux lumineux du luminaire s’exprime en lumens (lm).
- L’éclairement reçu sur une surface s’exprime en lux (lx), soit des lm/m² reçus.
- Température de couleur, rendu des couleurs et flux sont des caractéristiques distinctes. Une source plus froide ne crée pas, à elle seule, plus de lux.
- Une puissance en watts renseigne sur la consommation ; elle ne remplace pas le flux et la distribution photométrique.

Pour une tâche, examiner la surface sur laquelle elle est réalisée, pas uniquement le sol. La [fiche INRS ED 161](https://www.inrs.fr/media.html?refINRS=ED+161) décrit l’association de lumière générale et localisée, les obstacles, l’éblouissement et le choix des sources. Son périmètre est celui des lieux de travail ; ses tableaux ne sont pas automatiquement une obligation pour un logement.

## Méthode des lumens

Pour une zone simple et un ensemble de luminaires identiques :

```text
E_moyen_estimé = N × flux_luminaire × UF × MF / A
flux_total_requis = E_cible × A / (UF × MF)
N_minimum_arithmétique = plafond(E_cible × A / (flux_luminaire × UF × MF))
```

`A` est la surface de la zone en m² ; `N` la quantité ; `flux_luminaire` le flux émis par le luminaire complet au réglage considéré. `UF` représente la part utilisée sur la surface utile ; `MF` la conservation du flux utile dans le temps selon l’entretien et le vieillissement. Ce calcul suppose une zone alimentée par les sources considérées.

**Les deux facteurs sont au dénominateur dans le calcul du flux requis.** Avec des facteurs inférieurs à 1, les besoins augmentent. Ne pas réappliquer le rendement du luminaire si la fiche fournit déjà son flux de sortie. Un facteur majorant de dimensionnement parfois donné sous une valeur supérieure à 1 n’est pas MF ; préciser la convention au lieu de les intervertir.

La [méthode décrite par DIALux](https://evo.support-en.dial.de/support/solutions/articles/9000078303-lumen-method-) estime une moyenne à partir de la géométrie, des réflectances et de la distribution des sources. Ses hypothèses se dégradent pour les obstacles ou les géométries complexes. Une moyenne ne permet pas d’affirmer l’uniformité, l’éclairement minimal ou l’absence d’éblouissement.

Exécuter le calculateur :

```bash
python3 scripts/lumen_method.py --area-m2 24 --lumens-per-fixture 2400 \
  --utilization-factor 0.60 --maintenance-factor 0.80 --target-lux 200
```

Cet exemple est fictif. Les facteurs et la cible ne sont ni mesurés ni proposés comme réglages par défaut. Le script exige qu’ils soient fournis explicitement. À la racine du dépôt, préfixer le chemin par `architecture-interieure-eclairage/`.

## Inconnues et variantes

Un coefficient choisi parce qu’il paraît plausible doit être nommé hypothèse. Montrer l’effet d’une plage de facteurs quand elle est justifiée ; ne pas produire une précision décimale qui masque l’incertitude. Si la hauteur, la distribution ou les réflectances manquent, une estimation conditionnelle reste possible, mais elle ne valide pas l’installation.

Ne pas affecter tous les lumens de la pièce à une petite zone pour annoncer un éclairement de tâche. Seuls les flux qui y contribuent peuvent être pris en compte, avec un facteur adapté. Pour des luminaires différents, calculer la somme des flux utiles avec des hypothèses propres à chaque contribution ; le script fourni traite seulement les luminaires identiques d’une zone.

Conserver l’état de chaque zone. Une proposition d’éclairage du plan de travail ne résout pas automatiquement les besoins du passage, du stockage, d’un escalier ou d’un étage.

## Ombres et confort

Vérifier la ligne source–surface utile. Une étagère opaque, une poutre ou le corps de l’utilisateur peut l’intercepter. Rechercher une position au-dessus de la tâche ou une combinaison de directions, sans source agressive dans le champ de vision. Examiner aussi les reflets sur le plan et les écrans.

Un diffuseur peut améliorer le confort, mais sa seule présence ne garantit pas une valeur UGR. Le diamètre du plafonnier ne suffit pas à calculer sa couverture. Ne pas annoncer d’IRC, de scintillement ou de performance à faible variation sans fiche correspondante.

Pour comparer blanc et couleurs, utiliser le flux documenté au blanc utile. Le flux maximal ne décrit pas nécessairement une scène colorée ou un blanc chaud. Le curseur d’une application n’est pas une mesure photométrique ; éviter les conversions linéaires supposées en lux.

## Validation et entretien

Pour dimensionner finement, employer les données du luminaire exact, sa hauteur, les surfaces, les obstacles et un moteur photométrique adapté. Distinguer le fait de citer un logiciel, de l’avoir exécuté et d’avoir vérifié son résultat. Si aucun fichier IES/LDT adapté n’est disponible, l’indiquer ; ne pas remplacer la référence par un modèle voisin sans le déclarer.

Après pose, relever des mesures au luxmètre sur la zone de tâche et ses alentours, en notant position, réglage, lumière naturelle et points faibles. Un téléphone non étalonné fournit au mieux une indication approximative. Réserver un accès à l’entretien ; adapter choix et position si les essais révèlent une gêne ou des ombres.
