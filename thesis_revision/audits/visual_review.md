# Procès-verbal de revue visuelle

**Fichier :** `deliverables/These_revisee_BERKANE_Dhiyaddine.pdf`  
**Version :** 109 pages A4  
**SHA-256 :** `0fdca0f009e87d207d15e69c28c92346ccd5d5b25a08ec071bb36d2daeeb7258`  
**Date :** 25 octobre 2026  
**Résultat :** aucun défaut bloquant connu après les corrections décrites ci-dessous.

## 1. Périmètre inspecté

- Planches de contact régénérées à partir du PDF final et inspectées pour les pages **1–20, 21–40, 41–60, 61–80, 81–100 et 101–109**.
- Contrôle en pleine page du résumé arabe (4), de la liste des abréviations (8), de la bibliographie (97), de la dernière page (109) et des pages 36, 62, 64, 68, 71, 74, 79 et 85.
- Résumé arabe : ordre de lecture, forme des glyphes, titre, mots-clés et absence de citations.
- Pages de continuation, de bibliographie et de fin : séparation entre en-tête, corps et pied de page.
- Les **21 fichiers figures** ont été inspectés individuellement à pleine résolution avant leur incorporation ; leurs pages finales sont 18, 19, 21, 23, 31, 36, 39, 41, 47, 52, 56, 60, 62, 64, 68, 71, 74, 79, 82, 90 et 92.
- Bibliographie, pages 97–103 : vérification que les mots français ne sont pas coupés arbitrairement ; seules les URL trop longues sont rompues selon la largeur disponible.

## 2. Défauts trouvés et corrections vérifiées

| Défaut détecté pendant la revue | Correction | Contrôle final |
|---|---|---|
| Corps de texte commençant dans l’en-tête après certains sauts automatiques | Réinitialisation explicite à 25 mm après `header()` et test de la bande 40–54 pt | Aucun texte de corps dans la bande ; en-têtes séparés |
| En-tête courant du chapitre VI trop proche de la marge latérale | Réduction conditionnelle de 9 pt vers 8 pt avant toute troncature | Pages 85–93 lisibles ; tous les contrôles de marges latérales passent |
| Note de la liste des abréviations isolée sur une page supplémentaire | Compactage conditionnel de cette liste seulement, sans réduire le corps du mémoire | Tableau et note réunis page 8 ; sommaire page 9 ; pagination finale stable à 109 pages |
| Libellé « évolution du morphodynamique » | « Abaissement de calcul = dégradation + contraction + affouillement local » | Figure IV.2, page 62 |
| « une exutoire » et définition trop elliptique de la suffusion | « un exutoire » ; migration sélective des fines sans conduit nécessaire | Figure IV.3, page 64 |
| « coupure de modèle » et note touchant un cadre | « coupe géotechnique » et note déplacée | Figure V.1, page 74 |
| Flèche « Actions » traversant le titre du tablier | Flèche et libellé déplacés à droite | Figure I.1, page 18 |
| Flèche et étiquettes traversant le schéma d’alternatives | Flèche supprimée ; étiquettes déplacées et repliées | Figure I.4, page 23 ; schéma source également inspecté |
| Texte trop large dans le choix de fondation | Retour à la ligne explicite et terminologie « Superficielle/Profonde » | Figure V.2, page 79 |
| Câble/pylônes dépassant dans les titres des panneaux | Géométrie qualitative des panneaux suspendu/haubané abaissée ; libellé d’arc recentré | Figure I.3, page 21 |
| Libellés trop larges dans essais, liquéfaction, risques et registre | Repli ou reformulation courte sans changer le fond | Pages 52, 68, 60 et 71 |
| Libellé d’affouillement sur la ligne du lit | Libellé abaissé dans la zone libre | Figure IV.2, page 62 |
| Étiquettes de vallée croisant les traits techniques | Fonds d’étiquettes et niveau de texte ajustés | Figure II.1, page 36 |
| Mots bibliographiques coupés au milieu | `wrapmode="WORD"` pour les références | Pages 97–103 ; seules les URL longues sont rompues |
| Année `2008` coupée dans une source de figure | `wrapmode="WORD"` aussi pour les lignes « Source » | Figure IV.4, page 68 : `(2008)` reste entier |

## 3. Résultat par critère

- **Pages blanches ou presque vides injustifiées :** aucune ; la page 109 est une fin d’annexe courte, avec titre courant et numéro.
- **Texte ou figures hors page :** aucun observé ; le contrôle géométrique automatisé est également `pass`.
- **Chevauchements corps/en-tête :** aucun.
- **Figures :** lisibles à la taille incorporée ; aucune cote ou dimension normative n’est ajoutée à un schéma qualitatif.
- **Tableaux :** titres, en-têtes et unités visibles ; aucune ligne coupée horizontalement hors cadre.
- **Arabe :** glyphes joints et ordre RTL corrects ; 1 317 lettres arabes extractibles.
- **Références :** 65 notices réparties sur les pages 97–103 ; pas de mot français coupé par la justification ou le retour chariot.
- **Profil typographique :** A4, marges de 25 mm, corps Times New Roman 12 pt justifié avec interligne 1,5, légendes et sources différenciées, en-têtes de chapitre et pagination arabe continue.

## 4. Réserve DOCX

Le DOCX a été rouvert et son package/contenu ont été audités, mais aucun moteur Word ou LibreOffice n’est disponible pour produire un rendu visuel fidèle. Sa pagination peut varier avec les polices et le logiciel. Le PDF ci-dessus reste la référence de mise en page et de pagination ; aucune pagination Word n’est donc affirmée dans ce procès-verbal.
