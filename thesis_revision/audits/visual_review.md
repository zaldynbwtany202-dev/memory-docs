# Procès-verbal de revue visuelle

**Fichier :** `deliverables/These_revisee_BERKANE_Dhiyaddine.pdf`  
**Version :** 124 pages A4  
**SHA-256 :** `3c358289ec44c82a7b5363fe96559b046912f92f957c143f31874280af7cfc2e`  
**Date :** 25 octobre 2026  
**Résultat :** aucun défaut bloquant connu après les corrections décrites ci-dessous.

## 1. Périmètre inspecté

- Planches de contact régénérées à partir du PDF et inspectées pour les pages **1–20, 21–40, 41–60, 61–80, 81–100, 101–120 et 121–124**.
- Contrôle ciblé en pleine page du résumé arabe (4), de la liste des abréviations (9) et des nouvelles pages photographiques 48, 49, 66, 67, 82, 83, 96 et 107 ; contrôle rapproché des pages 112 et 124.
- Planche rapprochée des huit pages contenant les onze nouvelles figures : cadrage, lisibilité, concordance (a)/(b), légendes, sources et enchaînement avec le texte scientifique.
- Résumé arabe : ordre de lecture, forme des glyphes, titre, mots-clés et absence de citations.
- Les **45 figures** ont été contrôlées dans le PDF : 21 schémas et 24 planches réunissant 31 photographies ; leurs pages finales sont 19, 20, 22, 24, 32, 34, 34, 35, 35, 36, 37, 37, 41, 44, 46, 47, 48, 49, 54, 59, 63, 65, 65, 66, 66, 67, 70, 72, 74, 78, 81, 82, 82, 83, 83, 86, 91, 94, 95, 96, 96, 104, 106, 106, 107.
- Bibliographie, pages 112–118 : vérification que les mots français ne sont pas coupés arbitrairement ; seules les URL trop longues sont rompues selon la largeur disponible.
- Identité, crédits, licences ou statuts et transformations des photographies : `references/credits_photographies.md` et `references/photograph_assets_manifest.json`.

## 2. Défauts trouvés et corrections vérifiées

| Défaut détecté pendant la revue | Correction | Contrôle final |
|---|---|---|
| Corps de texte commençant dans l’en-tête après certains sauts automatiques | Réinitialisation explicite à 25 mm après `header()` et test de la bande 40–54 pt | Aucun texte de corps dans la bande ; en-têtes séparés |
| En-tête courant du chapitre VI trop proche de la marge latérale | Réduction conditionnelle de 9 pt vers 8 pt avant toute troncature | Pages 98–108 lisibles ; contrôles de marges latérales `pass` |
| Note de la liste des abréviations isolée sur une page supplémentaire | Compactage conditionnel de cette liste seulement | Tableau et note réunis page 9 ; sommaire page 10 |
| Libellé « évolution du morphodynamique » | « Abaissement de calcul = dégradation + contraction + affouillement local » | Figure IV.2, page 72 |
| « une exutoire » et définition trop elliptique de la suffusion | « un exutoire » ; migration sélective des fines sans conduit nécessaire | Figure IV.3, page 74 |
| « coupure de modèle » et note touchant un cadre | « coupe géotechnique » et note déplacée | Figure V.1, page 86 |
| Flèche « Actions » traversant le titre du tablier | Flèche et libellé déplacés à droite | Figure I.1, page 19 |
| Flèche et étiquettes traversant le schéma d’alternatives | Flèche supprimée ; étiquettes déplacées et repliées | Figure I.4, page 24 |
| Texte trop large dans le choix de fondation | Retour à la ligne explicite et terminologie « Superficielle/Profonde » | Figure V.2, page 91 |
| Câble/pylônes dépassant dans les titres des panneaux | Géométrie qualitative des panneaux abaissée ; libellé d’arc recentré | Figure I.3, page 22 |
| Libellés trop larges dans essais, liquéfaction, risques et registre | Repli ou reformulation courte sans changer le fond | Pages 59, 78, 70 et 81 |
| Libellé d’affouillement sur la ligne du lit | Libellé abaissé dans la zone libre | Figure IV.2, page 72 |
| Étiquettes de vallée croisant les traits techniques | Fonds d’étiquettes et niveau de texte ajustés | Figure II.1, page 41 |
| Année `2008` coupée dans une source de figure | `wrapmode="WORD"` pour les lignes « Source » | Figure IV.4, page 78 : `(2008)` reste entier |
| Dernier fragment de l’introduction des photographies SPT/CPT isolé en haut de page | Introduction raccourcie sans perdre la réserve sur l’absence de campagne nouvelle | Page 65 commence par les deux figures, sans ligne orpheline |
| Une seule ligne de conclusion du chapitre VI repoussée sur une page presque vide | Paragraphe contextuel resserré et nouvelle stabilisation en deux passes | Chapitre VI se termine page 108 ; conclusion générale page 109 ; total 124 pages |
| Petites photographies d’archive pixelisées si elles étaient élargies à toute la largeur | Largeur limitée selon les pixels sources, avec cible d’au moins environ 110 dpi | Alcántara, Strömsund et Tacoma Narrows lisibles pages 34, 35 et 82 |
| Risque de confusion entre images proches mais ouvrages différents | Notices Commons et sources primaires contrôlées ; résultats mal identifiés exclus | Légendes concordantes avec les ouvrages visibles ; crédits documentés |
| Seconde série photographique : archives proches, captures de logiciel et miniatures | Notices USDA vérifiées figure par figure ; capture de consolidation et miniatures écartées ; cellule CSIRO et vrais montages triaxiaux retenus | 16 photographies supplémentaires dans 11 planches ; aucune présentée comme une campagne propre |

## 3. Résultat par critère

- **Pages blanches ou presque vides injustifiées :** aucune ; la page 124 est une fin d’annexe courte, avec titre courant et numéro.
- **Texte ou figures hors page :** aucun observé ; le contrôle géométrique automatisé est également `pass`.
- **Chevauchements corps/en-tête :** aucun.
- **Figures et photographies :** lisibles à la taille incorporée ; les recadrages ne suppriment aucun élément nécessaire à l’identification ; aucune photographie n’est présentée comme une campagne de terrain nouvelle.
- **Tableaux :** titres, en-têtes et unités visibles ; aucune ligne coupée horizontalement hors cadre.
- **Arabe :** glyphes joints et ordre RTL corrects ; 1 317 lettres arabes extractibles.
- **Références :** 65 notices réparties sur les pages 112–118 ; pas de mot français coupé par la justification ou le retour chariot.
- **Profil typographique :** A4, marges de 25 mm, corps Times New Roman 12 pt justifié avec interligne 1,5, légendes et sources différenciées, en-têtes de chapitre et pagination arabe continue.

## 4. Réserve DOCX

Le DOCX a été rouvert et son package/contenu ont été audités, mais aucun moteur Word ou LibreOffice n’est disponible pour produire un rendu visuel fidèle. Sa pagination peut varier avec les polices et le logiciel. Le PDF ci-dessus reste la référence de mise en page et de pagination ; aucune pagination Word n’est donc affirmée dans ce procès-verbal.
