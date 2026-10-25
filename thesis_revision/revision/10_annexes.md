# ANNEXE A — AIDE-MÉMOIRE POUR UN PROJET DE PONT

## A.1 Objet et mode d’emploi

Cette annexe rassemble des grilles de contrôle. Elle ne fixe ni un nombre minimal d’essais, ni des valeurs de paramètres, ni des seuils réglementaires. Pour un projet réel, chaque ligne doit être reliée à un document, une donnée ou une décision identifiable. Les cases non applicables sont justifiées plutôt que laissées implicites.

## A.2 Fiche initiale du projet

[[TABLE:Fiche minimale avant définition du programme d’investigation|1,2,2]]
| Rubrique | Informations à rassembler | Point de validation |
|---|---|---|
| Ouvrage | Fonction, tracé, longueur, travées, profil en travers et phases | Version du plan et responsable des données |
| Appuis | Position des piles, culées, pylônes et ancrages | Type d’appui et exposition à l’eau ou aux remblais |
| Structure | Système porteur, réactions estimées et déplacements sensibles | Situations et critères transmis par le concepteur |
| Site | Topographie, géologie, géomorphologie et occupations | Cartes, date et zones non documentées |
| Hydrologie | Bassin, séries, débits et incertitudes | Méthode, scénarios et validation |
| Hydraulique | Niveaux, vitesses, contraction, afflux et embâcles | Géométrie, conditions aux limites et version du modèle |
| Morphodynamique | Historique du lit, transport solide et berges | Preuves d’évolution et besoins de suivi |
| Hydrogéologie | Nappes, gradients, exutoires et variations | Piézométrie, saison et représentativité |
| Réglementation | DTR, normes, guides et exigences du maître d’ouvrage | Édition, champ et date d’application |
| Construction | Accès, méthodes, eau, nuisances et contrôles | Faisabilité et investigations associées |
| Exploitation | Inspection, entretien et conséquences d’une défaillance | Accès, mesures initiales et responsabilités |

## A.3 Matrice question–méthode–preuve

[[TABLE:Exemples de questions et de preuves à rechercher|1,1,1]]
| Question de projet | Méthodes possibles selon le site | Preuve permettant de progresser |
|---|---|---|
| Quelles unités traversent les pieux ? | Carottages, logs, CPT et géophysique calibrée | Coupe corrélée et limites d’interpolation |
| Quelle compressibilité gouverne les tassements ? | Échantillons de qualité, œdomètre et essais in situ adaptés | Courbes contrainte–déformation et chemin de chargement |
| Quelle résistance non drainée mobiliser ? | Scissomètre, triaxial et corrélations validées | Valeurs par unité avec dispersion et conditions d’essai |
| Quelle perméabilité pour le drainage ou le pompage ? | Lefranc, essais de laboratoire ou pompage selon l’échelle | Domaine de validité et comparaison des échelles |
| Quelles discontinuités dans le rocher ? | Carottage orienté, description et téléviewer si adapté | Orientation, ouverture, remplissage et altération |
| Quelle profondeur de Vs pour la réponse du site ? | MASW, SASW, cross-hole ou down-hole | Modèle de propagation, résolution et calibrage |
| Quelle géométrie du lit et quelle évolution ? | Bathymétries répétées, profils et historique | Cotes datées, références communes et tendances |
| Une anomalie est-elle une cavité ? | Géophysique ciblée, sondage et modèle géologique | Recoupement direct ou scénario conservateur explicite |
| Les matériaux sont-ils compatibles avec l’exposition ? | Analyses sol–eau et identification des contacts | Méthodes, unités, saisons et classes d’exposition |
| La qualité d’exécution correspond-elle au modèle ? | Enregistrements, inspection, essais et contrôles | Critères d’acceptation et traitement des écarts |

## A.4 Structure d’un compte rendu d’investigation

Chaque opération est décrite avec un identifiant stable. La localisation comprend les coordonnées, l’altitude, le système de référence et la date. Le compte rendu précise l’équipement, la méthode, les conditions d’accès, les incidents et les personnes responsables. Les enregistrements bruts sont associés à l’identifiant et non seulement à une feuille de synthèse.

Pour un sondage, les logs indiquent les profondeurs, les lithologies, les échantillons, les refus, les venues d’eau et les pertes. Pour un essai in situ, les zéros, les étalonnages et les corrections sont conservés. Pour un échantillon, l’état à la réception, la conservation et les essais affectés sont documentés.

L’interprétation est séparée de l’observation. Une couche « supposée » n’est pas écrite comme une couche mesurée. Une corrélation indique sa source et son domaine. Les désaccords entre opérateurs ou méthodes sont conservés dans la revue.

## A.5 Revue avant remise du dossier géotechnique

- Le modèle de site montre-t-il les appuis, les accès, l’eau et les zones incertaines ?
- Chaque paramètre est-il relié à une unité, une méthode, une correction et un état limite ?
- Les hypothèses de drainage, de nappe et de géométrie future sont-elles explicites ?
- Les investigations insuffisantes sont-elles signalées avec leur conséquence sur la décision ?
- Les alternatives de fondation incluent-elles l’exécution, la protection et le suivi ?
- Les vérifications utilisent-elles un seul système cohérent de facteurs et de résistances ?
- Les critères de déplacement sont-ils validés avec le concepteur de la structure ?
- Les exigences de construction sont-elles mesurables et assorties de contrôles ?
- Les mesures d’alerte et les responsabilités sont-elles définies avant travaux ?
- Un tiers peut-il reproduire les calculs à partir des données et références fournies ?

# ANNEXE B — FORMULES, UNITÉS ET CONTRÔLES DE COHÉRENCE

## B.1 Règles d’écriture

Une équation est accompagnée de son domaine, de ses variables et de ses unités. Les grandeurs effectives et totales ne sont pas mélangées. Les pourcentages et les rapports sont distingués : une énergie de 60 % correspond à un rapport de 0,60 dans une formule qui attend un rapport sans dimension.

Les indices et exposants sont vérifiés par analyse dimensionnelle. Les expressions empiriques peuvent toutefois dépendre d’un système d’unités imposé par leur source ; dans ce cas, le système est indiqué et aucune conversion implicite n’est effectuée.

[[TABLE:Contrôles rapides des relations utilisées dans le mémoire|1,1,2]]
| Relation | Contrôle dimensionnel ou de domaine | Vigilance |
|---|---|---|
| q = k i A | q en volume/temps, k en longueur/temps, i sans dimension et A en aire | Loi de Darcy et section traversée cohérentes |
| i = Δh/L | Charge et longueur dans la même unité | Direction et géométrie de l’écoulement |
| N₆₀ = N × ER/60 | ER et 60 exprimés dans la même convention de pourcentage | Ne remplace pas les autres corrections SPT |
| qt = qc + u₂(1 − a) | Pressions dans la même unité et a sans dimension | Position de u₂ et coefficient de surface du cône |
| Fr = V/√(g y) | Vitesse, gravité et profondeur en unités cohérentes | Définition de la profondeur et écoulement représenté |
| y_l/y₁ = 2,0 K₁K₂K₃(a/y₁)^0,65 Fr₁^0,43 | Rapports sans dimension ; expression HEC-18 pour son domaine | Facteurs K et limites conditionnelles du guide |
| ΔH = Σ[Hᵢ(e₀,ᵢ − e₁,ᵢ)/(1 + e₀,ᵢ)] | Hauteurs et indices cohérents par couche | Chemin de contrainte et courbe de compressibilité |
| CSR = 0,65(a_max/g)(σ_v0/σ′v0)r_d | Tous les rapports sans dimension | Méthode simplifiée, mouvement de surface et facteur r_d |
| qᵤₗₜ = c′N꜀ + q′N_q + 0,5γ′B N_γ | Chaque terme en contrainte | Semelle filante, drainage et formulation des facteurs |
| E_d ≤ R_d | Même nature d’effet et de résistance | Facteurs définis par le référentiel, sans double réduction |

## B.2 Distinctions à contrôler dans une revue orale ou écrite

**Affouillement et érosion interne.** L’affouillement retire ou déplace les matériaux du lit et des berges sous l’action de l’écoulement et du transport solide. L’érosion interne concerne le transport de particules dans un sol, à une interface ou le long d’une discontinuité sous l’effet d’un écoulement interne. Le renard est un mécanisme d’érosion interne, pas un synonyme de l’affouillement.

**TCR et RQD.** Le TCR mesure la longueur totale récupérée par rapport à la longueur carottée. Le RQD ne retient que les morceaux sains de roche dont la longueur dépasse le seuil défini par la méthode, avec des règles de mesure et de qualité de carottage. Une récupération élevée peut inclure des fragments qui ne comptent pas dans le RQD.

**Vp et Vs.** Une méthode fondée sur les ondes de compression estime Vp dans son modèle. Elle ne fournit pas directement la vitesse de cisaillement Vs. Cette dernière nécessite une mesure ou une interprétation adaptée, par exemple par ondes de surface ou par dispositifs en forage.

**Porosité et perméabilité.** La porosité décrit la proportion de vides ; la perméabilité décrit la capacité à laisser circuler un fluide selon une loi et des conditions données. Deux matériaux de porosité comparable peuvent avoir des perméabilités très différentes.

**Mesure et paramètre.** Le nombre N du SPT, la résistance qc du CPT et une pression pressiométrique sont des résultats d’essai. Les paramètres c′, φ′, cu ou E sont interprétés avec des modèles et des hypothèses. Les deux niveaux doivent rester identifiables.

**Valeur caractéristique et valeur de calcul.** La première est choisie pour l’état limite et le volume concernés ; la seconde résulte de l’application du référentiel. Une résistance déjà exprimée comme valeur de calcul n’est pas réduite une seconde fois.

**Source primaire et source secondaire.** Un arrêté officialise un document et ses dispositions d’application ; il ne remplace pas le texte technique annexé. Un article de presse signale un événement ; il ne remplace pas un rapport d’expertise pour établir un mécanisme.

## B.3 Contrôle des tableaux et figures

Chaque figure possède un numéro, un titre et une source. Les schémas originaux sont identifiés comme tels et ne doivent pas être interprétés comme des coupes mesurées. Les dimensions normatives ne sont pas ajoutées à un dessin qualitatif. Les cartes et profils d’un projet réel doivent comporter orientation, échelle ou indication de non-échelle, unités et références de cotes.

Chaque tableau possède un titre, des en-têtes et des unités lorsque des grandeurs sont présentées. Les cellules vides sont expliquées. Les valeurs copiées d’une source sont vérifiées dans leur contexte et non dans un tableau secondaire qui les aurait déjà simplifiées.

## B.4 Contrôle final de cohérence scientifique

Avant diffusion, le lecteur vérifie que les mêmes termes désignent les mêmes objets dans tout le document. Les sigles sont définis, les références appelées dans le texte figurent dans la bibliographie et les notices non utilisées sont retirées. Les exemples locaux ne sont pas présentés comme des règles universelles.

Le lecteur recherche enfin les formulations absolues : « toujours », « jamais », « systématiquement », « premier facteur » ou « valeur admissible unique ». Elles ne sont conservées que si une définition, une démonstration ou un texte applicable les justifie. Cette revue stylistique est aussi une revue scientifique, car elle empêche une hypothèse limitée de devenir une règle non fondée.
