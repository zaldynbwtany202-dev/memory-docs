# CHAPITRE V — INTERPRÉTATION DES DONNÉES ET DÉCISIONS DE FONDATION

## V.1 Introduction

L’interprétation géotechnique transforme des observations en paramètres et des paramètres en décisions. Chaque transformation ajoute des hypothèses. Une valeur mesurée devient une valeur corrigée, puis une estimation de propriété, une valeur caractéristique et enfin une valeur de calcul. La traçabilité de cette chaîne est aussi importante que le résultat final.

Ce chapitre propose une méthode pour valider les données, construire le modèle, choisir les paramètres et comparer les fondations. Il distingue portance, déplacements, constructibilité et durabilité. Les approches de calcul sont présentées sans mélanger les coefficients de référentiels différents ni appliquer deux fois une réduction déjà incluse dans une résistance de calcul.

## V.2 Validation et organisation des données

### V.2.1 Quatre niveaux de valeurs

Le premier niveau est la donnée brute : nombre de coups, pression, profondeur, teneur en eau ou déplacement. Le deuxième est la donnée corrigée, par exemple une résistance SPT normalisée en énergie ou une résistance CPT corrigée de la pression interstitielle. Le troisième est le paramètre interprété : cohésion, angle de frottement, module ou perméabilité. Le quatrième est la valeur retenue pour un état limite.

Les formules, unités et références utilisées à chaque étape doivent être conservées. Une feuille de synthèse qui ne contient que le paramètre final empêche de vérifier si une correction a été appliquée deux fois ou si une corrélation sort de son domaine.

### V.2.2 Cohérence et valeurs atypiques

Les résultats sont comparés par couche, par méthode et par position. Une valeur atypique peut être une erreur, mais aussi le signe d’une lentille, d’une cavité ou d’une variation de faciès. Elle n’est ni supprimée ni moyennée automatiquement.

Les contrôles comprennent la répétition d’essais, la comparaison avec les logs, l’examen des enregistrements bruts et la vérification des calculs. Si une valeur est écartée, la raison technique est documentée. Si elle est conservée, son influence sur le modèle et les décisions est examinée.

### V.2.3 Du point au volume

Le passage à un volume de sol exige une interprétation spatiale. Les unités sont définies à partir de la géologie et de la réponse mécanique, pas seulement d’une classification par couleur ou par valeur de pénétration. Les transitions et les zones incertaines sont représentées.

La figure V.1 rappelle le rôle du modèle conceptuel dans cette transformation. Il relie les mesures aux décisions et reçoit en retour les questions soulevées par le projet.

[[FIGURE:data_to_ground_model|Des observations au modèle géotechnique puis aux décisions de fondation]]
[[SOURCE:schéma original de synthèse.]]

[[TABLE:Traçabilité des valeurs géotechniques|1,2,2]]
| Niveau | Exemple | Information à conserver |
|---|---|---|
| Mesure brute | N, qc, pression PMT, lecture œdométrique | Appareil, date, position, profondeur, unité et conditions |
| Valeur corrigée | N₆₀, qt ou courbe pression–volume corrigée | Formule, coefficient, référence et contrôle qualité |
| Paramètre interprété | c′, φ′, cu, module ou perméabilité | Modèle, corrélation, domaine et incertitude |
| Valeur représentative d’unité | Distribution ou estimation prudente pour une couche | Volume concerné, variabilité et nombre de données |
| Valeur caractéristique | Valeur affectant un état limite | État limite, scénario et justification du choix |
| Valeur de calcul | Valeur après application du référentiel | Facteur utilisé et preuve qu’il n’est pas appliqué deux fois |

## V.3 Choix des paramètres et incertitudes

### V.3.1 Paramètres mesurés et corrélations

Certaines propriétés sont mesurées directement dans les limites d’un essai ; d’autres sont estimées par corrélations. La résistance non drainée d’un scissomètre, le module d’un essai triaxial et la perméabilité d’un essai de pompage ne relèvent pas du même niveau d’interprétation qu’un angle de frottement estimé à partir de N.

Les corrélations doivent être choisies selon le type de sol, la plage de mesure, la procédure et le paramètre recherché. Leur dispersion est examinée. WROTH (1984) souligne l’importance des principes d’interprétation des essais in situ ; les travaux de PHOON et KULHAWY (1999a, 1999b) fournissent une base pour analyser la variabilité géotechnique.

Un paramètre issu d’une corrélation n’acquiert pas une précision supérieure parce qu’il est écrit avec plusieurs décimales. Le nombre de chiffres significatifs doit rester compatible avec la connaissance.

### V.3.2 Valeur caractéristique et état limite

L’Eurocode 7 définit la valeur caractéristique comme une estimation prudente de la valeur qui affecte l’occurrence de l’état limite considéré (CEN, 2004). Cette définition ne se réduit pas à « moyenne moins 1,64 écart-type ». Lorsque des méthodes statistiques sont utilisées, le texte distingue notamment l’estimation d’une moyenne et celle d’une valeur locale, avec des niveaux de confiance et de fractiles adaptés.

Le choix dépend donc du mécanisme : une rupture mobilisant un grand volume peut être gouvernée par une propriété moyenne sur ce volume, tandis qu’un mécanisme local peut dépendre d’une valeur défavorable localisée. Le nombre de données, leur indépendance et la représentativité de l’échantillon sont examinés.

Une distribution normale et un coefficient 1,64 ne sont appliqués que si le modèle statistique est justifié et si la question posée correspond à ce fractile. Dans tous les cas, le jugement géologique et l’expérience établie complètent le calcul.

### V.3.3 Variabilité et scénarios

La variabilité comprend la dispersion spatiale, les erreurs de mesure, l’incertitude des corrélations et l’incertitude du modèle. Elle peut être explorée par des scénarios bas, central et haut, par des analyses de sensibilité ou par une approche probabiliste lorsque les données le justifient.

Un coefficient de variation unique n’est pas attribué à un paramètre pour tous les sites. Les valeurs bibliographiques décrivent des populations particulières. Le projet doit plutôt indiquer quelles variations changent réellement la décision : niveau d’ancrage, type de fondation, épaisseur de couche compressible ou cote d’affouillement.

[[TABLE:Types d’incertitude et réponses possibles|1,2,2]]
| Source d’incertitude | Exemple | Réponse méthodologique |
|---|---|---|
| Mesure | Énergie SPT inconnue ou capteur mal saturé | Contrôle, calibration et limitation de l’usage |
| Échantillonnage | Couche peu représentée ou appui non accessible | Investigation ciblée ou scénario explicite |
| Corrélation | Paramètre estimé hors de la base initiale | Autre essai, comparaison et prudence documentée |
| Modèle spatial | Limite de couche interpolée | Variante de géométrie et investigation complémentaire |
| Modèle de comportement | Drainage ou mécanisme mal choisi | Comparaison de modèles et revue par les disciplines |
| Scénario | Crue, nappe ou phasage futur incertain | Analyse de sensibilité et suivi |

## V.4 Vérifications des fondations superficielles

### V.4.1 Mécanismes à examiner

Une fondation superficielle est vérifiée pour la rupture de portance, le glissement, le renversement ou l’équilibre global selon la configuration, ainsi que pour les déplacements et la durabilité. La géométrie de calcul inclut l’encastrement disponible dans la situation considérée. Sous une pile exposée à l’affouillement, le terrain potentiellement perdu n’est pas compté comme un soutien permanent sans justification.

Les conditions drainées et non drainées sont distinguées. Les paramètres effectifs c′ et φ′ conviennent à une analyse en contraintes effectives ; une analyse non drainée utilise une résistance adaptée et un modèle correspondant. La même expression ne doit pas être utilisée en remplaçant simplement un paramètre sans revoir le mécanisme.

### V.4.2 Forme classique de portance drainée

Pour une semelle filante, une charge verticale centrée et un modèle classique de rupture générale en conditions drainées, une expression de référence est :

[[EQ:qᵤₗₜ = c′N꜀ + q′N_q + 0,5γ′B N_γ]]

c′ est la cohésion effective, q′ la contrainte effective de couverture au niveau de la base, γ′ le poids volumique pertinent, B la largeur et N꜀, N_q, N_γ les facteurs de portance de la méthode choisie. Les définitions et valeurs de ces facteurs varient selon les formulations ; ils doivent être repris d’une seule source cohérente.

Cette forme ne tient pas compte à elle seule de l’excentrement, de l’inclinaison, de la forme, de la pente ou de la proximité d’une rive. Les extensions de MEYERHOF, HANSEN ou VESIĆ introduisent des corrections spécifiques. La notice de VESIĆ (1975) est retenue pour la discussion générale des fondations superficielles, mais aucun tableau de facteurs n’est reproduit sans recalcul et sans vérifier la formulation.

### V.4.3 Tassements

Les tassements sont évalués à partir du chemin de contrainte et de la compressibilité des couches. La méthode œdométrique utilise la variation d’indice des vides et distingue recompression et compression vierge lorsque le sol est surconsolidé. Dans les sables, des approches fondées sur les essais de pénétration peuvent être employées avec leurs limites ; SCHMERTMANN (1970) constitue une référence historique pour le tassement à partir du CPT.

Le résultat comprend une estimation des déplacements entre appuis et de leur chronologie. La comparaison aux mouvements acceptables est effectuée avec le modèle structural. Une valeur forfaitaire de tassement admissible ne remplace pas cette interaction.

## V.5 Vérifications des fondations profondes

### V.5.1 Résistance axiale et mécanismes

La résistance d’un pieu peut être décomposée en contribution de pointe et contribution de frottement latéral :

[[EQ:R = R_b + R_s]]

R_b est la contribution de base et R_s la contribution du fût pour le mécanisme et le niveau de déformation considérés. Cette écriture ne signifie pas que les maxima des deux contributions sont nécessairement mobilisés au même déplacement. La compatibilité des déformations et le comportement du groupe doivent être examinés.

Le frottement négatif est traité comme une action ou un effet du tassement du sol selon le référentiel, et non ajouté arbitrairement à la résistance. Les situations de soulèvement, de chargement horizontal et de séisme exigent des modèles spécifiques. POULOS et DAVIS (1980) présentent les principes d’analyse des pieux et des groupes.

### V.5.2 Mode d’installation

Le mode d’installation modifie le sol et la résistance. Les pieux battus peuvent densifier certains matériaux et générer des pressions interstitielles ; les pieux forés peuvent entraîner une décompression et un remaniement. Les paramètres issus d’une base de données pour une méthode ne sont pas transférés à une autre sans justification.

Les guides FHWA sur les pieux battus (FHWA, 2016b, 2016c) et les ouvrages de TOMLINSON (2001) insistent sur le lien entre calcul et construction. Les refus, les reprises de battage, les enregistrements de forage et les contrôles de bétonnage apportent des informations sur la cohérence du modèle.

Le matériel de forage conditionne la stabilité du trou, les paramètres d’exécution et les contrôles possibles. Cette foreuse à tarière photographiée à Auckland illustre un équipement de pieux de fondation ; le chantier n’est pas un pont et n’est pas attribué à l’auteur.

[[FIGURE:photo_auger_pile_rig|Foreuse à tarière pour pieux de fondation sur un chantier à Auckland (Nouvelle-Zélande)]]
[[SOURCE:Ingolfson, Wikimedia Commons, domaine public.]]

### V.5.3 Déplacements et interaction

Les vérifications incluent le tassement du pieu et du groupe, les déplacements horizontaux, les rotations et la flexion induite par les mouvements du terrain. Les réactions du sol peuvent être représentées par des relations non linéaires ou des modèles de continuum selon le niveau d’analyse requis.

Le choix du modèle dépend de la question. Une analyse détaillée n’est utile que si les paramètres et les conditions aux limites sont suffisamment contraints. Un modèle complexe alimenté par des données arbitraires ne constitue pas une amélioration de preuve.

[[TABLE:Principales vérifications par famille de fondation|1,1,1]]
| Famille | États ultimes à examiner | États de service et autres vérifications |
|---|---|---|
| Semelle / radier | Portance, glissement, équilibre global et géométrie après érosion | Tassements, rotations, drainage, durabilité et exécution de fouille |
| Pieux / barrettes | Pointe, frottement, groupe, soulèvement, charges horizontales et stabilité globale | Déplacements, frottement négatif, interaction et intégrité |
| Puits / caissons | Portance, stabilité pendant et après descente, base et fût | Contrôle du fond, déformations, étanchéité et conditions de travail |
| Scellement dans le rocher | Rupture du massif et de l’interface | Discontinuités, altération, déformations et contrôle du scellement |
| Sol amélioré | Stabilité du massif traité et du système composite | Homogénéité, performance mesurée et durabilité du traitement |

## V.6 Démarche comparative de choix

Le choix compare des solutions complètes : fondation, méthode d’exécution, protection, contrôle et suivi. Une semelle avec protection contre l’affouillement et une fondation profonde sans entretien ne sont pas des alternatives équivalentes si leurs risques résiduels diffèrent.

Les critères incluent la sécurité, les déplacements, la durabilité, la constructibilité, le délai, l’impact environnemental, le coût global et la capacité d’inspection. Les options écartées sont documentées avec la raison technique. Si les données sont insuffisantes pour décider, une investigation complémentaire est elle-même un résultat du processus.

[[FIGURE:foundation_selection|Comparaison des solutions de fondation et d’adaptation du site]]
[[SOURCE:schéma original de synthèse.]]

[[TABLE:Exemple de matrice de décision sans poids universels|1,1,1,1]]
| Critère | Question de comparaison | Preuve attendue | Conséquence d’une lacune |
|---|---|---|---|
| Sécurité géotechnique | Les mécanismes ultimes sont-ils vérifiés ? | Modèles, paramètres et scénarios | Option non validée |
| Déplacements | La structure accepte-t-elle les mouvements prévus ? | Analyse sol–structure et critères du projet | Risque de désordre ou de redimensionnement |
| Constructibilité | La qualité supposée est-elle réalisable ? | Méthode, accès, contrôles et retour d’expérience | Modification de méthode ou investigation |
| Hydraulique et érosion | La solution reste-t-elle stable dans la géométrie future ? | Cote de calcul et protection | Adaptation ou suivi obligatoire |
| Durabilité | Les matériaux et détails résistent-ils à l’exposition ? | Classes d’exposition et dispositions | Protection ou révision des matériaux |
| Coût global et entretien | Quels coûts et risques sur le cycle de vie ? | Hypothèses économiques séparées des faits techniques | Comparaison à documenter, sans ratio inventé |

## V.7 États limites et approches de calcul

### V.7.1 Principe général

Une vérification aux états limites compare les effets des actions à une résistance ou à un critère de performance dans une situation définie. Pour la stabilité géotechnique, une forme conceptuelle est :

[[EQ:E_d ≤ R_d]]

E_d est la valeur de calcul de l’effet et R_d la valeur de calcul de la résistance. Lorsque le référentiel applique un facteur de résistance à une valeur caractéristique, on peut écrire R_d = R_k/γ_R. Si R_d est déjà obtenue par une méthode qui inclut les réductions, il ne faut pas la diviser une seconde fois.

Les états de service comparent les déplacements ou autres indicateurs aux critères du projet. Ils ne sont pas déduits automatiquement des coefficients ultimes.

### V.7.2 Approches de l’Eurocode 7

L’Eurocode 7 définit des ensembles de facteurs pour les actions, les paramètres de sol et les résistances. Leur emploi dépend de l’approche de calcul et de l’annexe nationale. Le tableau V.4 rappelle la structure générale des ensembles A, M et R pour les vérifications géotechniques, sans attribuer de valeurs numériques universelles.

[[TABLE:Structure générale des approches de calcul de l’Eurocode 7 pour GEO|1,1,1,2]]
| Approche | Actions | Paramètres de sol | Résistances et remarques |
|---|---|---|---|
| DA1 — combinaison 1 | A1 | M1 | R1 ; vérifier cette combinaison avec l’autre lorsque requis |
| DA1 — combinaison 2 | A2 | M2 | R1 ; ne pas substituer R3 à cette combinaison |
| DA2 | A1 | M1 | R2 ; facteurs de résistance selon le référentiel national |
| DA3 | A2 | M2 | R3 ; domaine et application à vérifier pour l’ouvrage |

Le tableau ne constitue pas une liste complète des règles. Les ensembles applicables aux actions structurales et géotechniques, aux situations accidentelles et aux éléments de structure doivent être examinés dans le texte et l’annexe nationale retenus (CEN, 2004). Aucune approche n’est déclarée systématiquement la plus défavorable : les combinaisons requises sont vérifiées et le cas gouvernant est identifié par le calcul.

### V.7.3 Documents nationaux et versions

Le choix du référentiel est une décision contractuelle et réglementaire. Pour un projet algérien, les DTR et règlements applicables doivent être identifiés, notamment le DTR-BC 2.33 approuvé en 2024 pour les fondations et soutènements. Les coefficients ne doivent pas être reconstruits à partir d’un résumé ou d’un autre pays.

La date du document, ses amendements et son domaine sont consignés. Les comparaisons entre Eurocode, FHWA et règlements algériens portent sur leurs objets et leurs méthodes, sans créer de tableau d’équivalence artificiel.

## V.8 Sensibilité et revue des hypothèses

Une analyse de sensibilité fait varier les paramètres et scénarios qui ont une influence possible sur la décision. Elle peut porter sur l’épaisseur d’une couche, la nappe, la résistance, le module, la cote d’affouillement ou l’angle d’attaque. Les résultats sont examinés en termes de changement de solution, pas seulement de pourcentage de variation d’un calcul.

Les hypothèses critiques sont celles dont une modification plausible inverse le choix ou franchit un critère. Elles deviennent des priorités pour les investigations complémentaires ou pour le suivi. Les hypothèses sans influence peuvent être conservées avec une justification plus simple.

[[TABLE:Exemple de lecture d’une analyse de sensibilité|1,2,2]]
| Hypothèse testée | Résultat à examiner | Décision possible |
|---|---|---|
| Épaisseur de couche compressible | Tassement différentiel et chronologie | Investissement dans une investigation ou adaptation de la structure |
| Niveau de nappe | Portance, stabilité et exécution | Piézométrie prolongée et scénarios de drainage |
| Cote d’affouillement | Encastrement et stabilité | Protection, approfondissement ou inspection renforcée |
| Paramètre de frottement | Capacité et déplacement des pieux | Essai complémentaire ou modification de fondation |
| Géométrie d’une cavité | Mécanisme de rupture et risque résiduel | Sondage ciblé, déplacement d’appui ou traitement |

## V.9 Essais et contrôles pendant l’exécution

Les contrôles sont choisis pour vérifier les hypothèses et la qualité des éléments réalisés. Ils peuvent inclure essais de chargement, enregistrements de battage, carottages, contrôles d’intégrité, mesures de béton, inspection de fond de fouille et essais sur le terrain amélioré.

Il n’existe pas de pourcentage universel de pieux à tester pour tout projet. Le plan de contrôle dépend de la méthode, de la variabilité, des conséquences d’un défaut, des exigences du référentiel et du retour des premiers éléments. Les résultats sont comparés aux critères définis avant travaux.

Un essai bidirectionnel utilise une cellule de chargement incorporée au pieu et ne se confond pas avec un chargement statique appliqué en tête. L’exemple OJACK360 ci-dessous est photographié pendant l’installation sur un chantier de bâtiment ; il illustre le matériel et non un essai de pieu de pont exécuté pour cette étude.

[[FIGURE:photo_ojack_load_test|Cellule OJACK360 pour essai bidirectionnel de pieu pendant son installation sur un chantier de bâtiment]]
[[SOURCE:Amiruddin1995, Wikimedia Commons, CC BY-SA 4.0.]]

Les détails de cage et d’enrobage font également partie du contrôle préparatoire. La photographie montre un bloc d’enrobage sur une armature de paroi moulée ; elle ne démontre pas à elle seule la conformité de l’ensemble de la cage ou de l’élément bétonné.

[[FIGURE:photo_diaphragm_wall_spacer|Bloc d’enrobage fixé sur une armature de paroi moulée]]
[[SOURCE:CMMNA, « Diaphragm wall block », Wikimedia Commons, CC BY-SA 3.0.]]

Les non-conformités déclenchent une revue : vérification du matériel, investigation complémentaire, modification du procédé ou réévaluation du modèle. Elles ne doivent pas être seulement archivées.

## V.10 Méthode observationnelle et suivi

La méthode observationnelle, discutée notamment par PECK (1969), repose sur des hypothèses explicites, des prévisions, un plan de mesure et des actions prévues en cas d’écart. Elle n’est pas une invitation à improviser après le début des travaux.

Avant l’instrumentation, le projet définit ce qui sera mesuré, la fréquence, la précision, les critères d’alerte et les responsabilités. Les mesures sont reliées aux hypothèses : niveau de nappe pour le pompage, déplacement pour un remblai, bathymétrie pour l’affouillement ou intégrité pour une fondation.

[[FIGURE:observational_loop|Boucle de la méthode observationnelle pendant l’exécution et l’exploitation]]
[[SOURCE:schéma original de synthèse d’après les principes de PECK (1969).]]

[[TABLE:Exemples de suivi relié à des décisions|1,1,1,1]]
| Mesure | Hypothèse vérifiée | Critère à définir avant travaux | Action préparée |
|---|---|---|---|
| Piézométrie | Rabattement et drainage conformes au modèle | Niveau, gradient ou vitesse de variation | Modifier pompage, filtre ou phasage |
| Déplacement d’appui | Tassement et rotation dans les limites du projet | Seuil lié au modèle structural | Revue du modèle, adaptation ou confortement |
| Bathymétrie | Évolution du lit compatible avec le scénario | Cote d’alerte et tendance | Inspection, protection ou restriction selon le projet |
| Enregistrement de battage | Profil et énergie cohérents avec la fondation | Critères d’arrêt et anomalies | Vérification, essai complémentaire ou adaptation |
| Intégrité des pieux | Continuité et qualité de l’exécution | Critères d’acceptation du référentiel | Investigation et traitement de la non-conformité |

Les photographies de chantier peuvent compléter les enregistrements d’exécution lorsqu’elles sont datées, localisées et reliées à un élément précis. La vue suivante, extraite du mémoire original, illustre la cage de renforcement, les foreuses et les opérations de réalisation ; elle ne constitue pas une campagne de terrain nouvelle menée pour cette révision.

[[FIGURE:photo_bored_piles_original|Réalisation de pieux forés : cage de renforcement et matériel de forage sur chantier]]
[[SOURCE:mémoire original, page 38, panneau (b) ; photographie extraite et recadrée.]]

La réparation documentée au Monture Bridge associe reconstitution du remblai et enrochements de protection. Elle illustre une action corrective, mais ne dispense pas de vérifier la granulométrie, le filtre, la mise en place et l’ouverture hydraulique propres au projet.

[[FIGURE:photo_monture_riprap|Réparation du remblai de culée et protection par enrochements au Monture Bridge]]
[[SOURCE:USDA Forest Service, « Bridge Scour Evaluation » (1998), figure 16.]]

Les photographies anciennes sont également utiles pour comprendre les phases de construction. Ici, les cintres, les arcs et les appuis sont visibles simultanément ; l’image sert à la lecture du phasage et non à la détermination de paramètres géotechniques.

[[FIGURE:photo_monroe_construction|Monroe Street Bridge en construction à Spokane en 1911 : cintres, arcs et appuis]]
[[SOURCE:William O. Reed, University of Washington, 1er juin 1911, domaine public, via Wikimedia Commons.]]

Une autre archive permet d’isoler l’opération de bétonnage d’une fondation de pile. Elle est utilisée ici pour la lecture du phasage et du contrôle d’exécution, sans extrapolation de ses matériaux ou de sa géométrie à un projet actuel.

[[FIGURE:photo_story_bridge_foundation|Bétonnage de la fondation de la pile principale nord du Story Bridge à Brisbane (30 janvier 1936)]]
[[SOURCE:Lands Department, Queensland State Archives, image 3147, domaine public, via Wikimedia Commons.]]

## V.11 Contenu du dossier géotechnique

Le dossier final doit permettre à un tiers de reconstruire le raisonnement. Il comprend les données sources, les logs, les résultats bruts et corrigés, le modèle de site, les paramètres, les hypothèses, les vérifications, les exigences de construction et le plan de suivi. Les figures et les tableaux indiquent leur origine et leurs unités.

Les limites sont explicites : zones non investiguées, méthodes non applicables, résultats discordants et scénarios non tranchés. Les recommandations identifient celles qui sont impératives pour la sécurité, celles qui optimisent le projet et celles qui restent conditionnées à une décision ultérieure.

## V.12 Conclusion du chapitre

L’interprétation des données est une chaîne de décisions contrôlées. La valeur caractéristique n’est pas une formule statistique automatique, la résistance de calcul n’est pas réduite deux fois et les approches de calcul ne sont pas mélangées. Les fondations sont comparées sur la sécurité, les déplacements, la construction, la durabilité et le cycle de vie.

La méthode observationnelle prolonge cette démarche pendant l’exécution. Le chapitre VI applique ces principes au contexte algérien, en distinguant les documents réglementaires, les études scientifiques et les événements rapportés par la presse.
