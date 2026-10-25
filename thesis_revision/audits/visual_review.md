# Procès-verbal de revue visuelle

**Fichier :** `deliverables/These_revisee_BERKANE_Dhiyaddine.pdf`  
**Version :** 98 pages A4  
**SHA-256 :** `7801e035603b1adfcfbc62d74f1ec6afd272b1777ace8efa5e9f61f131afaae2`  
**Date :** 25 octobre 2026  
**Résultat :** aucun défaut bloquant connu après les corrections décrites ci-dessous.

## 1. Périmètre inspecté

- Planches de contact régénérées pour les pages **1–20, 21–40, 41–60, 61–80 et 81–98** du PDF final.
- Résumé arabe, page 4, en pleine page : ordre de lecture, forme des glyphes, titre, mots-clés et absence de citations.
- Pages de continuation, de bibliographie et de fin : séparation entre en-tête, corps et pied de page.
- Les **21 fichiers figures** inspectés individuellement à pleine résolution avant leur incorporation.
- Pages finales contenant les figures retouchées : 18, 21, 23, 35, 48, 51, 55, 57, 59, 62, 64, 67 et 71.
- Bibliographie, pages 89–93, après changement du mode de retour à la ligne : vérification que les mots français ne sont plus coupés ; seules les URL trop longues sont rompues selon la largeur disponible.

## 2. Défauts trouvés et corrections vérifiées

| Défaut détecté pendant la revue | Correction | Contrôle final |
|---|---|---|
| Corps de texte commençant dans l’en-tête après certains sauts automatiques | Réinitialisation explicite à 20 mm après `header()` et test de la bande 40–54 pt | Aucun texte de corps dans la bande ; en-têtes séparés |
| Libellé « évolution du morphodynamique » | « Abaissement de calcul = dégradation + contraction + affouillement local » | Figure IV.2, page 57 |
| « une exutoire » et définition trop elliptique de la suffusion | « un exutoire » ; migration sélective des fines sans conduit nécessaire | Figure IV.3, page 59 |
| « coupure de modèle » et note touchant un cadre | « coupe géotechnique » et note déplacée | Figure V.1, page 67 |
| Flèche « Actions » traversant le titre du tablier | Flèche et libellé déplacés à droite | Figure I.1, page 18 |
| Flèche et étiquettes traversant le schéma d’alternatives | Flèche supprimée ; étiquettes déplacées et repliées | Figure I.4, page 23 ; schéma source également inspecté |
| Texte trop large dans le choix de fondation | Retour à la ligne explicite et terminologie « Superficielle/Profonde » | Figure V.2, page 71 |
| Câble/pylônes dépassant dans les titres des panneaux | Géométrie qualitative des panneaux suspendu/haubané abaissée ; libellé d’arc recentré | Figure I.3, page 21 |
| Libellés trop larges dans essais, liquéfaction, risques et registre | Repli ou reformulation courte sans changer le fond | Pages 48, 62, 55 et 64 |
| Libellé d’affouillement sur la ligne du lit | Libellé abaissé dans la zone libre | Figure IV.2, page 57 |
| Étiquettes de vallée croisant les traits techniques | Fonds d’étiquettes et niveau de texte ajustés | Figure II.1, page 35 |
| Mots bibliographiques coupés au milieu | `wrapmode="WORD"` pour les références | Pages 89–93, pagination inchangée |
| Année `2008` coupée dans une source de figure | `wrapmode="WORD"` aussi pour les lignes « Source » | Figure IV.4, page 62 : `(2008)` reste entier |

## 3. Résultat par critère

- **Pages blanches ou presque vides injustifiées :** aucune ; la page 98 est une fin d’annexe courte, avec titre courant et numéro.
- **Texte ou figures hors page :** aucun observé ; le contrôle géométrique automatisé est également `pass`.
- **Chevauchements corps/en-tête :** aucun.
- **Figures :** lisibles à la taille incorporée ; aucune cote ou dimension normative n’est ajoutée à un schéma qualitatif.
- **Tableaux :** titres, en-têtes et unités visibles ; aucune ligne coupée horizontalement hors cadre.
- **Arabe :** glyphes joints et ordre RTL corrects ; 1 317 lettres arabes extractibles.
- **Références :** 65 notices réparties sur les pages 89–93 ; pas de mot français coupé par la justification ou le retour chariot.

## 4. Réserve DOCX

Le DOCX a été rouvert et son package/contenu ont été audités, mais aucun moteur Word ou LibreOffice n’est disponible pour produire un rendu visuel fidèle. Sa pagination peut varier avec les polices et le logiciel. Le PDF ci-dessus reste la référence de mise en page et de pagination.
