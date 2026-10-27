# Procès-verbal de revue visuelle

**Fichier :** `deliverables/These_revisee_BERKANE_Dhiyaddine.pdf`  
**Version :** 141 pages A4  
**SHA-256 :** `4c531e72fb0eef12a056b325eb25d5e61f6389e2e4105176a0244367c9e30c9f`  
**Date :** 27 octobre 2026  
**Résultat :** aucun défaut bloquant connu après les corrections décrites ci-dessous.

## 1. Périmètre inspecté

- Huit planches de contact régénérées à partir du PDF et inspectées pour les pages **1–20, 21–40, 41–60, 61–80, 81–100, 101–120, 121–140 et 141**.
- Contrôle ciblé en pleine page des cinq nouvelles planches du début du chapitre I (22, 23, 28, 29 et 30), du résumé arabe (4), de la bibliographie (129 et 135) et de la dernière page d’annexe (141). La page 29 a été rendue et inspectée une nouvelle fois après l’ajout de l’attribution complète Akashi/MLIT.
- Les nouvelles pages ont été examinées pour le cadrage, la lisibilité, la concordance (a)/(b), les légendes, les sources, la continuité du texte scientifique et l’absence de présentation comme travail de terrain de l’auteur.
- Résumé arabe : ordre de lecture, forme des glyphes, titre, mots-clés et absence de citations.
- Les **68 figures** ont été contrôlées dans le PDF : 21 schémas et 47 planches réunissant 63 photographies ; leurs pages finales sont 20, 21, 22, 23, 24, 26, 28, 29, 30, 36, 38, 38, 39, 39, 40, 41, 41, 44, 45, 47, 49, 51, 52, 53, 54, 55, 55, 60, 62, 66, 67, 68, 69, 70, 72, 73, 73, 75, 76, 77, 77, 78, 81, 83, 85, 89, 89, 92, 94, 95, 95, 96, 96, 99, 103, 105, 108, 109, 110, 111, 112, 112, 113, 121, 123, 123, 124, 124.
- Bibliographie, pages 129–135 : vérification que les mots français ne sont pas coupés arbitrairement ; seules les URL trop longues sont rompues selon la largeur disponible.
- Identité, crédits, licences ou statuts et transformations des photographies : `references/credits_photographies.md` et `references/photograph_assets_manifest.json`.

## 2. Défauts trouvés et corrections vérifiées

| Défaut détecté pendant la revue | Correction | Contrôle final |
|---|---|---|
| Corps de texte commençant dans l’en-tête après certains sauts automatiques | Réinitialisation explicite à 25 mm après `header()` et test de la bande 40–54 pt | Aucun texte de corps dans la bande ; en-têtes séparés |
| En-tête courant du chapitre VI trop proche de la marge latérale | Réduction conditionnelle de 9 pt vers 8 pt avant toute troncature | Pages 115–125 lisibles ; contrôles de marges latérales `pass` |
| Note de la liste des abréviations isolée sur une page supplémentaire | Compactage conditionnel de cette liste seulement | Tableau et note réunis page 10 ; sommaire pages 11–13 |
| Libellés ou sources trop larges dans les schémas et leurs notices | Repli ou reformulation courte sans changer le fond ; `wrapmode="WORD"` pour les sources | Figures I.1 p.20, I.6 p.26, II.3 p.47, III.3 p.66, IV.1–IV.4 p.81–89 et V.3 p.105 lisibles |
| Petites photographies d’archive pixelisées si elles étaient élargies à toute la largeur | Largeur limitée selon les pixels sources | Alcántara, Strömsund et Tacoma Narrows lisibles pages 38, 39 et 95 |
| Risque de confusion entre images proches mais ouvrages différents | Notices et sources primaires contrôlées ; résultats mal identifiés exclus | Légendes concordantes avec les ouvrages visibles ; crédits documentés |
| Seconde série photographique : archives proches, captures de logiciel et miniatures | Notices USDA vérifiées figure par figure ; captures et miniatures écartées | 16 photographies dans 11 planches conservées ; aucune présentée comme une campagne propre |
| Troisième série : risque d’intervertir méthodes, équipements ou localisations | Association une par une des 24 sources aux 18 actifs ; paires (a)/(b) et crédits revérifiés après composition | Réfraction/réflexion distinctes ; OJACK360 non légendé comme kentledge ; bloc de paroi moulée non légendé comme excavation ; Kerala, Majorque, Jordanie, Auckland, Nisqually et Brisbane correctement situés |
| Quatrième série : identification des ouvrages, cadrage du Golden Gate et attribution complète de la vue aérienne d’Akashi | Huit photographies placées dans cinq planches aux pages 22, 23 et 28–30 ; résultats Pont du Gard, Forth et Sydney mal identifiés écartés ; recadrage vertical du Golden Gate recentré ; mention MLIT complète rétablie | Ouvrages et parties (a)/(b) concordants ; pont du Gard, Forth, Sydney, Golden Gate, Akashi, Confederation et Øresund correctement identifiés ; aucune source ou légende tronquée |
| Regroupement figure–légende–source pouvant laisser un espace résiduel en bas de page | Blocs conservés ensemble plutôt que légendes orphelines ; géométrie et pages blanches testées automatiquement | Aucun dépassement ni page blanche ; l’espace résiduel de la page 108 est justifié par le report du bloc suivant |

## 3. Résultat par critère

- **Pages blanches ou presque vides injustifiées :** aucune ; la page 141 est une fin d’annexe courte, avec titre courant et numéro.
- **Texte ou figures hors page :** aucun observé ; le contrôle géométrique automatisé est également `pass`.
- **Chevauchements corps/en-tête :** aucun.
- **Figures et photographies :** lisibles à la taille incorporée ; les recadrages ne suppriment aucun élément nécessaire à l’identification ; aucune photographie n’est présentée comme une campagne de terrain nouvelle.
- **Tableaux :** titres, en-têtes et unités visibles ; aucune ligne coupée horizontalement hors cadre.
- **Arabe :** glyphes joints et ordre RTL corrects ; 1 317 lettres arabes extractibles.
- **Références :** 65 notices réparties sur les pages 129–135 ; pas de mot français coupé par la justification ou le retour chariot.
- **Profil typographique :** A4, marges de 25 mm, corps Times New Roman 12 pt justifié avec interligne 1,5, légendes et sources différenciées, en-têtes de chapitre et pagination arabe continue.

## 4. Réserve DOCX

Le DOCX a été rouvert et son package/contenu ont été audités, mais aucun moteur Word ou LibreOffice n’est disponible pour produire un rendu visuel fidèle. Sa pagination peut varier avec les polices et le logiciel. Le PDF ci-dessus reste la référence de mise en page et de pagination ; aucune pagination Word n’est donc affirmée dans ce procès-verbal.
