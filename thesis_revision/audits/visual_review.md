# Procès-verbal de revue visuelle

**Fichier :** `deliverables/These_revisee_BERKANE_Dhiyaddine.pdf`  
**Version :** 116 pages A4  
**SHA-256 :** `7da0db13e99a7da40520fcfc35b94c0bfa9bf937d01a6685071a6ae76a52cc08`  
**Date :** 25 octobre 2026  
**Résultat :** aucun défaut bloquant connu après les corrections décrites ci-dessous.

## 1. Périmètre inspecté

- Planches de contact régénérées à partir du PDF et inspectées pour les pages **1–20, 21–40, 41–60, 61–80, 81–100 et 101–116**, puis contrôle ciblé des pages modifiées après stabilisation à 116 pages.
- Contrôle en pleine page du résumé arabe (4), de la liste des abréviations (8), des pages 33, 34, 63, 78, 99, 100 et 101, du début de bibliographie (104) et de la dernière page (116).
- Planche rapprochée des pages photographiques 33–36, 46, 63, 78, 89 et 99 : identité visible, cadrage, lisibilité, légendes et sources.
- Résumé arabe : ordre de lecture, forme des glyphes, titre, mots-clés et absence de citations.
- Les **34 figures** ont été inspectées dans le PDF ; les 21 schémas sources avaient également été contrôlés individuellement et les 13 nouvelles planches réunissant 15 photographies ont été vérifiées avant incorporation ; leurs pages finales sont 18, 19, 21, 23, 31, 33, 33, 34, 34, 35, 36, 36, 40, 43, 45, 46, 52, 57, 61, 63, 63, 66, 68, 70, 74, 77, 78, 80, 85, 88, 89, 97, 99, 99.
- Bibliographie, pages 104–110 : vérification que les mots français ne sont pas coupés arbitrairement ; seules les URL trop longues sont rompues selon la largeur disponible.
- Identité, crédits, licences ou statuts et transformations des photographies : `references/credits_photographies.md` et `references/photograph_assets_manifest.json`.

## 2. Défauts trouvés et corrections vérifiées

| Défaut détecté pendant la revue | Correction | Contrôle final |
|---|---|---|
| Corps de texte commençant dans l’en-tête après certains sauts automatiques | Réinitialisation explicite à 25 mm après `header()` et test de la bande 40–54 pt | Aucun texte de corps dans la bande ; en-têtes séparés |
| En-tête courant du chapitre VI trop proche de la marge latérale | Réduction conditionnelle de 9 pt vers 8 pt avant toute troncature | Pages 91–100 lisibles ; contrôles de marges latérales `pass` |
| Note de la liste des abréviations isolée sur une page supplémentaire | Compactage conditionnel de cette liste seulement | Tableau et note réunis page 8 ; sommaire page 9 |
| Libellé « évolution du morphodynamique » | « Abaissement de calcul = dégradation + contraction + affouillement local » | Figure IV.2, page 68 |
| « une exutoire » et définition trop elliptique de la suffusion | « un exutoire » ; migration sélective des fines sans conduit nécessaire | Figure IV.3, page 70 |
| « coupure de modèle » et note touchant un cadre | « coupe géotechnique » et note déplacée | Figure V.1, page 80 |
| Flèche « Actions » traversant le titre du tablier | Flèche et libellé déplacés à droite | Figure I.1, page 18 |
| Flèche et étiquettes traversant le schéma d’alternatives | Flèche supprimée ; étiquettes déplacées et repliées | Figure I.4, page 23 |
| Texte trop large dans le choix de fondation | Retour à la ligne explicite et terminologie « Superficielle/Profonde » | Figure V.2, page 85 |
| Câble/pylônes dépassant dans les titres des panneaux | Géométrie qualitative des panneaux abaissée ; libellé d’arc recentré | Figure I.3, page 21 |
| Libellés trop larges dans essais, liquéfaction, risques et registre | Repli ou reformulation courte sans changer le fond | Pages 57, 74, 66 et 77 |
| Libellé d’affouillement sur la ligne du lit | Libellé abaissé dans la zone libre | Figure IV.2, page 68 |
| Étiquettes de vallée croisant les traits techniques | Fonds d’étiquettes et niveau de texte ajustés | Figure II.1, page 40 |
| Année `2008` coupée dans une source de figure | `wrapmode="WORD"` pour les lignes « Source » | Figure IV.4, page 74 : `(2008)` reste entier |
| Dernier fragment de l’introduction des photographies SPT/CPT isolé en haut de page | Introduction raccourcie sans perdre la réserve sur l’absence de campagne nouvelle | Page 63 commence par les deux figures, sans ligne orpheline |
| Une seule ligne de conclusion du chapitre VI repoussée sur une page presque vide | Paragraphe contextuel resserré et nouvelle stabilisation en deux passes | Chapitre VI se termine page 100 ; conclusion générale page 101 ; total 116 pages |
| Petites photographies d’archive pixelisées si elles étaient élargies à toute la largeur | Largeur limitée selon les pixels sources, avec cible d’au moins environ 110 dpi | Alcántara, Strömsund et Tacoma Narrows lisibles pages 33, 34 et 78 |
| Risque de confusion entre images proches mais ouvrages différents | Notices Commons et sources primaires contrôlées ; résultats mal identifiés exclus | Légendes concordantes avec les ouvrages visibles ; crédits documentés |

## 3. Résultat par critère

- **Pages blanches ou presque vides injustifiées :** aucune ; la page 116 est une fin d’annexe courte, avec titre courant et numéro.
- **Texte ou figures hors page :** aucun observé ; le contrôle géométrique automatisé est également `pass`.
- **Chevauchements corps/en-tête :** aucun.
- **Figures et photographies :** lisibles à la taille incorporée ; les recadrages ne suppriment aucun élément nécessaire à l’identification ; aucune photographie n’est présentée comme une campagne de terrain nouvelle.
- **Tableaux :** titres, en-têtes et unités visibles ; aucune ligne coupée horizontalement hors cadre.
- **Arabe :** glyphes joints et ordre RTL corrects ; 1 317 lettres arabes extractibles.
- **Références :** 65 notices réparties sur les pages 104–110 ; pas de mot français coupé par la justification ou le retour chariot.
- **Profil typographique :** A4, marges de 25 mm, corps Times New Roman 12 pt justifié avec interligne 1,5, légendes et sources différenciées, en-têtes de chapitre et pagination arabe continue.

## 4. Réserve DOCX

Le DOCX a été rouvert et son package/contenu ont été audités, mais aucun moteur Word ou LibreOffice n’est disponible pour produire un rendu visuel fidèle. Sa pagination peut varier avec les polices et le logiciel. Le PDF ci-dessus reste la référence de mise en page et de pagination ; aucune pagination Word n’est donc affirmée dans ce procès-verbal.
