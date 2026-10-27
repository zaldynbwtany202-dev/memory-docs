# Profil de présentation harmonisé — mémoire BERKANE Dhiyaddine

**Date d’application :** 27 octobre 2026  
**Périmètre :** PDF fixe et DOCX éditable reconstruits depuis les sources contrôlées.  
**Statut :** profil explicite fondé sur des documents universitaires algériens identifiables et sur les instructions des encadrants. Ce n’est **ni une norme nationale unique ni une certification de conformité administrative à l’Université Larbi Tébessi**, dont aucun guide typographique complet n’a été obtenu.

## 1. Sources consultées et règles effectivement retenues

| Clé | Document identifiable | Règles retenues dans le présent profil | Règles non transposées automatiquement |
|---|---|---|---|
| **C3** | Université Constantine 3, Vice-rectorat de la formation supérieure, *Guide de présentation d’un mémoire de Master*, année universitaire 2014/2015. [PDF officiel](https://igtu.univ-constantine3.dz/wp-content/uploads/2021/11/Guide-master-fran%C3%A7ais.pdf), règles citées vérifiées le 25/10/2026 dans l’extraction partielle disponible (lots 0–1) ; consultation intégrale non revendiquée. | Times New Roman ; corps 12 ; interligne 1,5 ; marges de 2,5 cm ; paragraphes justifiés ; titres de chapitre 14 gras et de sections/sous-sections 12 gras ; résumé arabe ; listes des figures/tableaux/abréviations ; figures légendées sous la figure, tableaux titrés au-dessus ; sources en corps 10 ; bibliographie et annexes structurées. | La fourchette de 50–80 pages et la numérotation romaine des pages liminaires ne sont pas importées : elles appartiennent à ce guide, tandis que le manuscrit fourni compte 198 pages et que les corrections demandées nécessitent un corpus plus développé. Aucun texte n’est supprimé pour satisfaire une limite étrangère à l’établissement de soutenance. |
| **USTHB-IA** | Université des Sciences et de la Technologie Houari Boumediene, Faculté d’Électronique et d’Informatique, Département Instrumentation Automatique, *Présentation d’un mémoire de PFE Master*, rubrique « Normes à respecter lors de la rédaction ». [Page officielle](https://fei.usthb.dz/Dept_Inst_Auto/?q=node/31), règles relevées le 25/10/2026 dans l’extrait indexé de cette page ; accès direct indisponible lors de la vérification. | Confirmation, dans un contexte algérien de PFE technique, de Times New Roman 12 et de l’interligne 1,5 ; intitulé du chapitre dans l’en-tête ; numéro de page centré dans le pied ; formules sur ligne séparée ; schémas, graphiques et tableaux clairs, numérotés et légendés. | Les marges de 2 cm, les références entre crochets et la numérotation des formules propres à cette fiche départementale ne sont pas combinées avec le profil C3. Les citations auteur–année et les références scientifiques déjà vérifiées ne sont pas converties artificiellement. |
| **ULT-FST** | Université Echahid Cheikh Larbi Tébessi, Faculté des Sciences et de la Technologie, avis de dépôt des mémoires de Master 2023/2024. [Avis officiel](https://www.univ-tebessa.dz/fst/4213/), consulté le 25/10/2026. | Priorité à l’exécution effective des modifications demandées par le jury avant le dépôt. | Cet avis ne fixe aucune police, marge ou interligne ; il ne peut donc pas servir à inventer une règle typographique locale. |
| **SRC** | Mémoire fourni, `source/Étude_bibliographique_sur_les_fondations_de_ponts.pdf`, 198 pages, SHA-256 `a2d1ab3b3d8ebfc4a4f9bd954cd3435a8722f09f042cc52ad5a342c7147f5900`. | Éléments locaux vérifiables : A4, Times New Roman 12 dans le corps, pas de ligne d’environ 20,7 pt, identité de la couverture, jury, session et pagination arabe continue. Ces éléments servent à conserver la cohérence avec le document de l’établissement. | Le fichier fourni est un manuscrit, pas un règlement officiel. Il ne justifie à lui seul aucune affirmation de norme institutionnelle. |

## 2. Profil appliqué

| Élément | Règle appliquée au PDF et au DOCX | Origine |
|---|---|---|
| Page | A4 portrait, 210 × 297 mm | SRC ; présentation universitaire courante |
| Marges | **25 mm en haut, à droite, en bas et à gauche** | C3 |
| Corps du texte | **Times New Roman 12 pt** | C3, USTHB-IA, SRC |
| Interligne | **1,5** ; DOCX `line_spacing=1.5`, PDF avance de ligne **7,3 mm**, cohérente avec le pas mesuré dans SRC | C3, USTHB-IA, SRC |
| Paragraphes | Justifiés ; bibliographie alignée à gauche pour éviter les espaces excessifs dans les URL | C3 ; précaution technique documentée |
| Chapitres et titres principaux | Times New Roman **14 pt gras** | C3 |
| Sections et sous-sections | Times New Roman **12 pt gras** | C3 |
| En-tête | Intitulé du chapitre ou de la partie, corps 9, réduit conditionnellement jusqu’à 8 pt pour rester dans les marges sans troncature ; aucun en-tête sur la couverture | USTHB-IA ; adaptation technique mesurée |
| Pied de page | Numéro arabe continu, centré, corps 10 ; couverture non numérotée visuellement | USTHB-IA et SRC |
| Figures | Numérotation par chapitre ; titre centré **sous** la figure, corps 10 | C3, USTHB-IA |
| Tableaux | Numérotation par chapitre ; titre centré **au-dessus**, corps 10 | C3, USTHB-IA |
| Sources de figures/tableaux | Mention « Source : … », alignée à droite, corps 10 | C3 |
| Équations | Ligne séparée et définition des symboles/unités dans le texte ou l’annexe B | USTHB-IA ; contenu scientifique contrôlé |
| Tableaux et index | Corps intérieur compact 8,1–8,5 pt pour préserver la lisibilité des colonnes ; aucune règle C3/USTHB-IA n’impose un corps intérieur différent | Choix de composition explicité, sans changement du contenu |
| Résumé arabe | Texte réel, RTL, corps 12 et interligne 1,5 ; glyphes DejaVu Sans dans le PDF | Obligation d’un résumé arabe en C3 ; nécessité technique de rendu Unicode |

## 3. Polices et rendu du PDF

Le PDF n’est pas simplement étiqueté « Times New Roman ». Le constructeur extrait temporairement les fontes Times New Roman régulière, grasse et italique **déjà incorporées au mémoire source** (xrefs 245, 267 et 280). Leur champ `OS/2 fsType=8` permet l’incorporation éditable. Elles ne sont pas déposées comme fichiers de polices autonomes dans Git.

Ces incorporations PDF sont des sous-ensembles de caractères. DejaVu Serif/Sans sert uniquement de **repli pour les glyphes absents** ; le résumé arabe utilise explicitement DejaVu Sans avec HarfBuzz afin de préserver la liaison et la direction RTL. Le DOCX déclare Times New Roman dans les propriétés de police, y compris `w:cs`, afin que Word utilise la version complète installée sur le poste de lecture.

## 4. Limites de portée qui ne sont pas dissimulées

- Le profil est une **harmonisation documentée**, pas une prétendue norme algérienne uniforme : les sources C3 et USTHB-IA divergent notamment sur les marges et le style de citation.
- Aucune conformité administrative officielle à Larbi Tébessi n’est affirmée sans guide local complet. L’avis ULT-FST confirme seulement l’obligation d’appliquer les corrections du jury avant dépôt.
- La longueur n’est pas réduite pour importer la limite C3 de 50–80 pages. La version révisée compte **141 pages**, contre 198 pour le source, avec le contenu scientifique et les développements demandés conservés.
- La pagination arabe continue du manuscrit fourni est conservée pour des renvois stables ; la convention romaine des liminaires de C3 n’est pas revendiquée.
- La pagination du DOCX reste dépendante du moteur Word/LibreOffice ; le PDF constitue la référence fixe.

## 5. Preuves de vérification

- `build_report.json` : profil appliqué, provenance et empreintes des fontes, stabilité des deux passes.
- `final_pdf_qa.json` : A4, marges, corps 12, interligne mesuré, sources 10, pagination, sommaire, légendes, arabe et absence de défauts géométriques.
- `docx_build_report.json` et `docx_content_audit.json` : marges 25 mm, Times New Roman 12, interligne 1,5, styles de titres, champs, médias et structure du package.
- `visual_review.md` : inspection des planches de contact de toutes les pages et des pages critiques en pleine taille.
