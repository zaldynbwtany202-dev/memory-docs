# CHAPITRE IV — MÉCANISMES DE RISQUE ET VULNÉRABILITÉ DES PONTS

## IV.1 Introduction

Les risques géotechniques des ponts résultent de la rencontre entre un mécanisme physique, une vulnérabilité de l’ouvrage et des conséquences fonctionnelles ou structurelles. Il n’existe pas de classement universel qui placerait partout l’affouillement, la liquéfaction ou le karst au même niveau. La gravité dépend du site, de la configuration des fondations, des possibilités de détection et des mesures de protection.

Cette approche évite deux répétitions fréquentes : présenter chaque risque comme « la première cause » de rupture et additionner des pourcentages issus de populations différentes. Le présent chapitre analyse les mécanismes, les données nécessaires et les interactions. Les valeurs de calcul ne sont retenues que lorsqu’une méthode et son domaine peuvent être définis.

## IV.2 Cadre d’analyse du risque

L’analyse suit une chaîne : danger ou processus, scénario, exposition de l’ouvrage, vulnérabilité, conséquences, incertitudes et mesures de maîtrise. Une même cavité peut avoir des conséquences très différentes selon sa position par rapport aux appuis ; une même crue peut être sans gravité pour une fondation protégée et critique pour une autre déjà partiellement dénudée.

La connaissance disponible fait partie de l’évaluation. Un mécanisme possible mais mal documenté peut nécessiter une investigation avant de conclure. À l’inverse, une hypothèse conservatrice peut être adoptée temporairement si son coût et ses conséquences sont explicites.

[[FIGURE:risk_interactions|Interactions des principales familles de risques au niveau d’un appui]]
[[SOURCE:schéma original de synthèse.]]

[[TABLE:Structure d’un scénario de risque géotechnique|1,2,2]]
| Élément | Question posée | Exemple de preuve attendue |
|---|---|---|
| Mécanisme | Quel processus physique peut se produire ? | Modèle géologique, hydraulique ou hydromécanique |
| Scénario | Dans quelles conditions se produit-il ? | Crue, séisme, humidification, travaux ou évolution lente |
| Exposition | Quels appuis ou zones sont concernés ? | Localisation et géométrie du système |
| Vulnérabilité | Comment l’ouvrage réagit-il ? | Fondation, rigidité, appuis, état et redondance |
| Conséquences | Quelles fonctions ou marges sont affectées ? | Déplacements, perte d’appui, interruption ou réparation |
| Incertitudes | Que sait-on et que suppose-t-on ? | Qualité des données, sensibilité et hypothèses |
| Maîtrise | Comment prévenir, détecter ou agir ? | Conception, protection, suivi et plan d’intervention |

## IV.3 Tassements et déplacements du terrain

### IV.3.1 Mécanismes

Les tassements peuvent résulter d’une compression immédiate, d’une consolidation, d’un fluage, d’un tassement régional ou d’une variation de volume liée à l’eau. Leur décomposition dépend du matériau et du chargement. Dans les sables, les déplacements peuvent être rapides mais rester sensibles à la densité et aux cycles ; dans les argiles, la dissipation des pressions interstitielles contrôle souvent la chronologie.

Le tassement calculé sous une charge uniforme ne représente pas nécessairement le mouvement d’un appui. La géométrie de la fondation, la superposition des charges, les remblais voisins et les variations latérales modifient la réponse. Les méthodes de calcul doivent donc être cohérentes avec le modèle de couches et le chemin de contrainte.

### IV.3.2 Vulnérabilité structurale

Un tassement uniforme peut affecter le profil et le drainage sans introduire les mêmes efforts qu’un tassement différentiel. Une rotation peut être critique pour un arc ou un appareil d’appui. Un mouvement horizontal peut solliciter les pieux et la culée. La vulnérabilité doit être examinée avec le concepteur de la structure.

Les mouvements tolérables dépendent du type de pont, de la portée, de la continuité et des détails constructifs. Les données de MOULTON et al. (1985) sont utiles pour comprendre les catégories de mouvements et leurs effets, mais ne créent pas une limite universelle de quelques millimètres applicable à tous les ouvrages.

### IV.3.3 Frottement négatif et déplacements imposés

Lorsqu’un sol se tasse autour d’un pieu, le frottement peut s’exercer vers le bas et ajouter une charge. Le phénomène dépend du déplacement relatif entre le sol et le pieu, de la compressibilité des couches et de la chronologie. Il ne se réduit pas à une règle liée à tout remblai proche.

Les culées subissent également la poussée et le tassement des remblais. Les déplacements latéraux du terrain peuvent courber les fondations et modifier les réactions du tablier. La reconnaissance doit donc fournir les paramètres de compressibilité et de résistance sur toute la hauteur concernée.

## IV.4 Affouillement et évolution du lit

### IV.4.1 Décomposition du processus

L’abaissement du lit près d’un pont peut associer trois composantes : la dégradation à long terme du tronçon, l’affouillement de contraction dû à la modification de l’écoulement dans l’emprise et l’affouillement local autour des piles ou culées. Une écriture conceptuelle est :

[[EQ:yₜ = y_d + y_c + y_l]]

yₜ représente l’abaissement total retenu par le modèle, y_d la dégradation à long terme, y_c la composante de contraction et y_l l’affouillement local. Cette addition n’est légitime que si les composantes sont définies sans double comptage et si le référentiel de calcul les combine de cette manière. La figure IV.2 illustre ces processus sans attribuer une profondeur numérique générale.

[[FIGURE:scour_components|Dégradation à long terme, contraction et affouillement local]]
[[SOURCE:schéma original de synthèse d’après FHWA (2012a, 2012b).]]

La dégradation à long terme relève du bassin et du tronçon : apports sédimentaires, aménagements, incision ou élargissement. La contraction dépend de la géométrie de l’écoulement et de l’emprise de l’ouvrage. L’affouillement local résulte des structures tourbillonnaires et de l’accélération autour d’un obstacle. Les confondre conduit soit à sous-estimer la cote du lit, soit à additionner des effets déjà inclus dans un modèle.

### IV.4.2 Affouillement local en lit vivant et en eau claire

En lit vivant, le transport sédimentaire alimente la fosse tout en étant affecté par l’écoulement local. En eau claire, le transport en amont est limité et l’évolution temporelle peut être différente. Les matériaux cohésifs, les sols cimentés et les roches érodables nécessitent des approches spécifiques ; les équations développées pour les sables ne leur sont pas automatiquement transposables.

Les paramètres importants comprennent la profondeur et la vitesse d’approche, l’angle d’attaque, la forme et la largeur de la pile, la géométrie du radier ou des pieux exposés, la granulométrie et la configuration du lit. Leur effet n’est pas toujours monotone ou indépendant.

### IV.4.3 Équation HEC-18 pour les piles : portée et limites

Pour des configurations simples de piles et des conditions fluviales alluviales définies, HEC-18 présente une équation issue des travaux de Colorado State University :

[[EQ:y_l/y₁ = 2,0 · K₁K₂K₃ · (a/y₁)⁰·⁶⁵ · Fr₁⁰·⁴³]]

Dans cette expression, y_l est la profondeur d’affouillement local, y₁ la profondeur d’écoulement directement en amont, a la largeur de pile, Fr₁ le nombre de Froude d’approche et K₁, K₂, K₃ les facteurs de forme de nez, d’angle d’attaque et de condition du lit définis par le guide (FHWA, 2012a).

Cette équation ne constitue pas une loi universelle. HEC-18 précise son domaine de base, des adaptations pour les configurations complexes et d’autres approches possibles. Les limites de rapport y_l/a citées par le guide concernent des conditions précises de piles à nez arrondi alignées avec l’écoulement ; elles ne doivent pas être appliquées indistinctement à toute pile, culée ou forme de lit.

[[TABLE:Données et vérifications nécessaires à une analyse d’affouillement|1,2,2]]
| Composante | Données nécessaires | Vérification de cohérence |
|---|---|---|
| Dégradation à long terme | Historique du tronçon, apports, aménagements et levés | Tendance distinguée de la réponse à une seule crue |
| Contraction | Géométrie de l’emprise, débits, vitesses et transport solide | Contraction générale et locale non comptées deux fois |
| Local aux piles | Forme, angle, approche, lit et configuration des fondations | Méthode adaptée au matériau et à la complexité de la pile |
| Local aux culées | Géométrie de rive, écoulement, remblai et protection | Méthode spécifique à la culée, non simple transposition de la pile |
| Situation future | Scénarios de crue, embâcles et changements du chenal | Sensibilité et cote résiduelle de la fondation |

### IV.4.4 Protection, inspection et entretien

Les mesures de maîtrise comprennent la modification de la géométrie, l’approfondissement ou l’adaptation de la fondation, la protection du lit et des berges, la gestion des embâcles et la surveillance. HEC-23 présente une gamme de contre-mesures et leurs conditions de sélection (FHWA, 2009a, 2009b).

Une protection en enrochements ne se choisit pas par habitude. Son dimensionnement dépend de l’hydraulique, de la granulométrie, du filtre, de la géométrie et de la possibilité d’entretien. Les systèmes articulés, les gabions, les protections géotextiles ou les modifications d’avant-bec possèdent leurs propres modes de défaillance.

L’inspection après crue et le suivi bathymétrique sont essentiels lorsque les incertitudes sont importantes. La conception doit prévoir l’accès et les mesures de référence nécessaires.

## IV.5 Érosion interne et transport de particules

### IV.5.1 Diversité des mécanismes

L’érosion interne regroupe des processus différents : renard régressif, suffusion, érosion de contact et fuite concentrée. Le renard implique la progression d’un conduit ; la suffusion correspond à la migration de fines dans un squelette ; l’érosion de contact se développe à l’interface de couches ; la fuite concentrée exploite une fissure ou un interface. La figure IV.3 résume ces distinctions.

[[FIGURE:internal_erosion_mechanisms|Quatre mécanismes d’érosion interne et leurs conditions de diagnostic]]
[[SOURCE:schéma original de synthèse.]]

Le diagnostic nécessite des preuves de géométrie, de granulométrie et d’écoulement. La présence d’un niveau d’eau élevé ne suffit pas à conclure à un renard. Les sorties de particules, les variations turbides, les affaissements et les anomalies de drainage doivent être examinés avec le modèle du massif.

### IV.5.2 Gradient hydraulique et résistance à l’érosion

Pour un écoulement vertical ascendant dans un sol saturé et un modèle simplifié, le gradient critique associé à l’égalité entre contrainte effective verticale et force d’écoulement peut s’écrire :

[[EQ:i꜀ᵣᵢₜ = γ′/γ_w = (Gₛ − 1)/(1 + e)]]

γ′ est le poids volumique déjaugé, γ_w celui de l’eau, Gₛ la densité relative des grains et e l’indice des vides. Cette relation ne décrit pas tous les mécanismes d’érosion interne. Elle suppose une configuration et un mécanisme particuliers ; elle ne tient pas compte à elle seule de la cohésion, des filtres, de la suffusion ou des hétérogénéités.

La stabilité vis-à-vis de l’érosion ne doit donc pas être résumée par un coefficient global unique. Elle exige une analyse des gradients locaux, des propriétés des matériaux, des contacts et des conditions de sortie.

### IV.5.3 Filtres, drainage et surveillance

Les filtres et transitions granulométriques visent à retenir les particules tout en permettant le drainage. Leur vérification dépend des courbes granulométriques des matériaux protégés et du filtre, ainsi que de la compatibilité entre couches successives. Les géotextiles demandent également une analyse de colmatage et de mise en œuvre.

Le drainage réduit les pressions mais peut créer des chemins d’écoulement concentré s’il est mal conçu. Les sorties doivent être protégées et accessibles à l’inspection. La surveillance recherche les évolutions de turbidité, de débit, de niveau et de géométrie du terrain.

[[TABLE:Diagnostic différencié des processus d’érosion interne|1,1,1,1]]
| Processus | Indice recherché | Données décisives | Mesures de maîtrise possibles |
|---|---|---|---|
| Renard régressif | Conduit ou progression depuis une exutoire | Gradients, sortie, continuité du matériau et transport | Réduction du gradient, protection de sortie et colmatage maîtrisé |
| Suffusion | Migration de fines sans conduit initial | Granulométrie interne, squelette et écoulement | Filtre adapté, réduction de l’écoulement et traitement justifié |
| Érosion de contact | Transport à l’interface de couches | Compatibilité des granulométries et orientation du flux | Transition ou filtre et contrôle du gradient |
| Fuite concentrée | Circulation le long d’une fissure ou d’un contact | Interfaces, défauts, structures enterrées et pressions | Étanchéité, drainage contrôlé et réparation du chemin |

## IV.6 Instabilité des berges et des pentes

La stabilité des berges dépend de la géométrie, de la résistance du sol, des pressions interstitielles, des charges et de l’érosion du pied. Une berge peut être stable en étiage et se déstabiliser lors de la recession d’une crue, lorsque le soutien de l’eau diminue alors que les pressions internes restent élevées.

L’affouillement du pied retire du matériau et modifie la géométrie ; il ne doit pas être analysé indépendamment de la stabilité globale. Les remblais d’accès, les charges de chantier et les modifications de drainage peuvent également influencer le mécanisme.

Les méthodes d’analyse en contraintes effectives ou totales sont choisies selon le drainage et la durée de la situation. DUNCAN et WRIGHT (2005) détaillent les principes de résistance et de stabilité des pentes. Les facteurs partiels et les exigences de vérification relèvent du référentiel retenu ; aucun coefficient global n’est attribué ici à l’Eurocode 7.

[[TABLE:Situations de rive à examiner|1,2,2]]
| Situation | Mécanisme possible | Données et analyses nécessaires |
|---|---|---|
| Montée de crue | Variation des pressions et érosion localisée | Niveaux, perméabilité, géométrie et vitesse de montée |
| Recession rapide | Pressions internes résiduelles avec soutien externe réduit | Drainage, résistance et analyse transitoire |
| Affouillement du pied | Retrait du soutien et augmentation de la hauteur instable | Bathymétrie, scénario d’affouillement et stabilité globale |
| Remblai ou travaux | Surcharge et modification du drainage | Phasage, charges temporaires et instrumentation |
| Végétation ou aménagement | Modification de l’érosion, de l’eau et des charges | Diagnostic spécifique, sans supposer un effet toujours favorable |

## IV.7 Liquéfaction et conséquences sismiques

### IV.7.1 Chaîne de dépistage

La liquéfaction concerne la perte de résistance et de rigidité d’un sol sous l’effet des pressions interstitielles cycliques, principalement dans des sols pulvérulents saturés susceptibles de se contracter. Son évaluation associe la susceptibilité du dépôt, le niveau d’eau, la sollicitation sismique et les conséquences sur l’ouvrage.

La présence d’une couche sableuse saturée ne suffit pas à conclure. La densité, la granulométrie, les fines, l’histoire du sol et le confinement interviennent. Les classifications sismiques de site ne sont pas des critères binaires de liquéfaction ; elles répondent à une autre question.

### IV.7.2 Sollicitation cyclique

La méthode simplifiée historique de SEED et IDRISS (1971) compare une demande cyclique à une résistance. Une forme classique de la demande est :

[[EQ:CSR = 0,65 · (a_max/g) · (σ_v0/σ′v0) · r_d]]

a_max est l’accélération maximale à la surface du site, g l’accélération de la pesanteur, σ_v0 la contrainte verticale totale initiale, σ′v0 la contrainte verticale effective initiale et r_d un facteur de réduction avec la profondeur. Cette équation s’insère dans une méthode complète qui inclut notamment la magnitude et les corrections de résistance. Elle ne doit pas être utilisée avec l’accélération du rocher présentée comme celle de la surface.

### IV.7.3 Résistance à la liquéfaction

La résistance cyclique peut être estimée par des approches SPT, CPT ou Vs. Les travaux de YOUD et al. (2001), IDRISS et BOULANGER (2008) et ROBERTSON et WRIDE (1998) présentent des méthodes et leurs corrections. Chaque approche exige des paramètres cohérents : énergie et couverture pour le SPT, résistance corrigée et comportement pour le CPT, vitesse de cisaillement et domaine de la méthode pour Vs.

Les seuils proposés par les courbes ne sont pas des interrupteurs universels. Les sols graveleux, les matériaux à forte teneur en fines et les dépôts particuliers peuvent sortir du domaine des bases de données. Une analyse complémentaire est alors nécessaire.

### IV.7.4 Conséquences pour les fondations

Les conséquences possibles comprennent tassements, déplacements latéraux, perte de résistance, augmentation de pression interstitielle et interaction dynamique modifiée. Les pieux peuvent être sollicités par les déplacements du sol même lorsque leur capacité verticale reste suffisante. L’ancrer sous une couche potentiellement liquéfiable ne dispense pas d’analyser ces effets.

La reconnaissance doit donc fournir l’épaisseur et la continuité des couches, leur état, la nappe, les paramètres de dépistage et les éléments nécessaires à la réponse du site. Les solutions peuvent associer adaptation des fondations, amélioration du sol, drainage ou modification du système structural, avec vérification de leur performance.

[[FIGURE:liquefaction_chain|Chaîne d’évaluation de la liquéfaction, du dépistage aux conséquences]]
[[SOURCE:schéma original de synthèse d’après SEED et IDRISS (1971), YOUD et al. (2001) et IDRISS et BOULANGER (2008).]]

Les manifestations de surface aident à documenter les conséquences, mais leur présence ou leur absence ne suffit pas à conclure sur tout un site. Les exemples USGS montrent des volcans de sable et un étalement latéral ; ils ne démontrent pas une susceptibilité à la liquéfaction en Algérie.

[[FIGURE:photo_liquefaction_effects|Manifestations de liquéfaction : (a) volcans de sable le long d’une voie ferrée ; (b) escarpement d’étalement latéral et restes de volcan de sable à Nisqually (2001)]]
[[SOURCE:USGS, « What is liquefaction? » et Open-File Report 03-211, domaine public.]]

[[TABLE:Erreurs à éviter dans l’analyse de liquéfaction|1,2,2]]
| Simplification incorrecte | Pourquoi elle est trompeuse | Traitement retenu |
|---|---|---|
| « Sable + nappe = liquéfaction » | Ignore la densité, la sollicitation et l’histoire du dépôt | Évaluer susceptibilité, demande, résistance et conséquences |
| Employer N ou qc sans corrections | Mélange des procédures et des bases de données | Documenter les corrections propres à la méthode |
| Utiliser l’accélération du rocher comme accélération de surface | Ignore la réponse du site | Définir le mouvement de surface avec le spécialiste sismique |
| Ancrer les pieux puis conclure sans autre analyse | Ne traite pas les déplacements latéraux et la flexion | Vérifier l’interaction sol–fondation–structure |
| Déduire la liquéfaction d’une classe de site | La classification sismique répond à un autre objectif | Conduire un dépistage spécifique |

## IV.8 Karst, dissolution et affaissement

Le risque karstique est traité selon le modèle du chapitre II : géométrie, remplissage, eau, discontinuités et évolution. Les conséquences pour un pont peuvent être une perte d’appui, un tassement différentiel, une rupture de toit ou des difficultés d’exécution. Leur probabilité et leur gravité ne peuvent être déduites d’une seule anomalie géophysique ou d’un seul indice RMR.

Les résultats publiés pour un site particulier apportent des méthodes d’investigation et des ordres de grandeur locaux. Ils ne définissent pas un rapport toit/largeur universel pour toute fondation de pont. La recommandation générale est de recouper les preuves et d’évaluer les scénarios de rupture avec les charges et la géométrie réelles.

## IV.9 Agressivité chimique et durabilité

### IV.9.1 De l’analyse à l’exposition

L’agressivité dépend du sol, de l’eau, de l’élément exposé et du temps. Sulfates, chlorures, acidité et autres agents agissent selon des mécanismes différents. Leur concentration mesurée à une date ne suffit pas à définir l’exposition pendant toute la vie de l’ouvrage : renouvellement de l’eau, alternance humide–sec et contact avec les matériaux doivent être considérés.

Les prélèvements sont représentatifs des zones et des saisons pertinentes. Les résultats sont reliés à une norme d’analyse et à un système de classes d’exposition. Le choix du ciment, des additions, de la formulation, de l’enrobage ou d’une protection appartient ensuite à une conception de durabilité cohérente avec le référentiel applicable.

### IV.9.2 Éditions normatives et responsabilité de vérification

La famille EN 206 connaît une transition documentaire au moment de la révision. EN 206:2013+A2:2021 existe avec ses dispositions nationales, tandis que les parties EN 206-1:2026 et EN 206-2:2026 sont publiées (CEN, 2021, 2026a, 2026b). La notice AFNOR précise que l’utilisation des nouvelles parties en France est liée à la publication de l’ensemble de la série et que la version antérieure demeure applicable pendant cette transition (AFNOR, 2026).

Cette situation illustre pourquoi le mémoire ne fige ni une classe de ciment ni une valeur d’enrobage comme règle universelle. Le projet doit identifier l’édition applicable, les compléments nationaux et les classes d’exposition retenues. La même exigence s’applique aux aciers et aux systèmes de protection contre la corrosion.

[[TABLE:Chaîne de décision pour l’agressivité chimique|1,2,2]]
| Étape | Contenu | Erreur à éviter |
|---|---|---|
| Prélèvement | Sol, eau, zones exposées et conditions saisonnières | Généraliser une analyse isolée à tout le site |
| Analyse | Méthodes, unités, incertitudes et agents recherchés | Comparer des résultats obtenus par des méthodes incompatibles |
| Classement d’exposition | Référentiel, contact et renouvellement de l’eau | Transformer une concentration en prescription sans contexte |
| Conception des matériaux | Liants, formulation, enrobage, détails et protections | Choisir un seul ciment comme réponse à toute agressivité |
| Contrôle et suivi | Conformité, inspection et maintenance | Supposer que la durabilité est acquise sans contrôle |

## IV.10 Risques liés à l’exécution

Les travaux peuvent modifier le terrain et créer des risques qui n’existaient pas dans l’état initial. Le battage produit des vibrations et du refoulement ; le forage peut décomprimer ou éroder ; le pompage abaisse la nappe et provoque des tassements ; le bétonnage sous boue ou sous eau exige une continuité et des contrôles stricts.

La reconnaissance doit anticiper ces mécanismes. Un paramètre de portance élevé ne garantit pas la qualité d’un pieu si le fond est mal nettoyé ou si la paroi s’effondre. Les incidents de forage sont des données géotechniques : pertes de boue, chutes d’outil et venues d’eau peuvent révéler des cavités ou des circulations.

[[TABLE:Risques d’exécution et données préventives|1,2,2]]
| Opération | Risque géotechnique ou de qualité | Données et contrôles à prévoir |
|---|---|---|
| Battage | Vibrations, refoulement, refus et endommagement | Profil de pénétration, essais, critères d’arrêt et suivi des environs |
| Forage de pieux | Instabilité, boue, remaniement et obstructions | Lithologie, eau, paramètres de forage et inspection |
| Bétonnage | Inclusion, discontinuité ou contamination | Contrôles du béton, volumes, continuité et essais d’intégrité adaptés |
| Pompage | Tassements, érosion et rabattement non contrôlé | Perméabilité, rayon d’influence, suivi piézométrique et filtration |
| Batardeau ou caisson | Soulevènement, fuite et difficulté de descente | Gradient, stabilité du fond, obstacles et niveau d’eau |
| Remblaiement | Tassement et pressions sur culées ou pieux | Compressibilité, phasage, compactage et instrumentation |

## IV.11 Synthèse des risques et priorisation

La synthèse ne consiste pas à attribuer un score arbitraire puis à en déduire une catégorie réglementaire. Elle organise les scénarios par mécanisme, appui, conséquence et niveau de preuve. Une matrice peut aider à prioriser les revues, mais sa graduation doit être définie pour le projet et ne remplace pas l’analyse physique.

Les interactions sont explicitées : affouillement du pied et instabilité de rive, remblai compressible et frottement négatif, karst et circulation d’eau, séisme et liquéfaction, exécution et érosion interne. Cette lecture évite de traiter chaque ligne du registre indépendamment.

[[FIGURE:risk_register_flow|Organisation d’un registre de risques fondé sur les scénarios et les preuves]]
[[SOURCE:schéma original ; les catégories de priorité sont à définir pour chaque projet.]]

[[TABLE:Synthèse des mécanismes et des données gouvernantes|1,1,1,1]]
| Mécanisme | Données gouvernantes | Vulnérabilité à examiner | Réponse de conception ou de suivi |
|---|---|---|---|
| Tassements | Compressibilité, couches, charges et drainage | Système de tablier, appuis et transitions | Adaptation, phasage, traitement ou instrumentation |
| Affouillement | Hydrologie, hydraulique, sédiments et géométrie future | Encastrement et stabilité de la fondation | Fondation, protection, inspection et entretien |
| Érosion interne | Granulométrie, gradients, interfaces et exutoires | Perte de matériau et affaissement | Filtres, drainage et surveillance |
| Instabilité de rive | Géométrie, résistance, eau et érosion du pied | Culées, piles et accès | Protection, modification de géométrie et suivi |
| Liquéfaction | Sol, nappe, mouvement et résistance cyclique | Déplacements et interaction avec les fondations | Dépistage, analyse SSI, amélioration ou adaptation |
| Karst | Cavités, remplissage, eau et discontinuités | Perte d’appui et exécution | Vérification, déplacement, traitement ou fondation adaptée |
| Agressivité | Chimie, exposition et matériaux | Durabilité des éléments enterrés ou exposés | Classes d’exposition, conception et maintenance |
| Exécution | Méthode, eau, obstacles et qualité | Défauts et modification du terrain | Contrôles, adaptation de méthode et traçabilité |

Le suivi bathymétrique relie une mesure à une position et à une date. L’inspection hydrographique du Barnhart Island Bridge illustre cette acquisition au droit d’un appui ; elle ne constitue pas une campagne réalisée pour ce mémoire et ne remplace pas l’analyse des tendances entre levés.

[[FIGURE:photo_fathometer_inspection|Inspection hydrographique par fathometer au Barnhart Island Bridge, Massena (New York)]]
[[SOURCE:McLaren Engineering Group, Wikimedia Commons, CC BY-SA 4.0.]]

La vulnérabilité peut également provenir d’une interaction qui dépasse le seul modèle géotechnique. Le cas de Tacoma Narrows, analysé à la section I.3.5, est rappelé ici pour ne pas réduire tous les désordres à un problème de fondation : la photographie documente la rupture du tablier par un phénomène aérodynamique, non un affouillement.

[[FIGURE:photo_tacoma_collapse|Rupture du tablier de Tacoma Narrows le 7 novembre 1940 : interaction vent–structure]]
[[SOURCE:photographie d’archive, « Tacoma-narrows-bridge-collapse.jpg », Wikimedia Commons, domaine public.]]

Les archives de l’USDA permettent de distinguer des mécanismes qui ne doivent pas être réunis sous le terme générique d’« érosion » : affouillement d’appuis d’un pont, puis perte d’un remblai de ponceau associée à un piping et à l’affouillement. Le second exemple reste explicitement un ponceau, et non un pont.

[[FIGURE:photo_scour_piping_usfs|Conséquences hydrauliques documentées : (a) rupture du Little Salmon River Bridge après affouillement ; (b) rupture du remblai d’un ponceau à Moss Creek après piping et affouillement]]
[[SOURCE:USDA Forest Service, « Bridge Scour Evaluation » (1998), figures 1 et 8 ; crue de janvier 1997 pour le panneau (a).]]

L’affouillement du remblai de culée peut compromettre l’accès sans détruire immédiatement la structure porteuse. La photographie suivante illustre ce scénario et justifie d’inspecter les remblais, les murs en aile et les appuis ensemble.

[[FIGURE:photo_monture_fill_failure|Rupture du remblai de culée au Monture Bridge, avec dommages limités à l’ouvrage]]
[[SOURCE:USDA Forest Service, « Bridge Scour Evaluation » (1998), figure 15.]]

En matière de durabilité, l’écaillage est un indice visuel à localiser et à suivre. La photographie ne démontre pas à elle seule son origine chimique ou l’état des armatures ; l’enquête doit associer matériaux, exposition et mesures complémentaires.

[[FIGURE:photo_bridge_spalling|Écaillage du béton au Lewis River Bridge : exemple d’indice visuel à documenter]]
[[SOURCE:NPS / Doug Madsen, Yellowstone National Park, domaine public, via Wikimedia Commons.]]

## IV.12 Conclusion du chapitre

Les risques propres aux ponts sont liés par l’eau, les déplacements du terrain et le fonctionnement de l’ouvrage. Leur analyse exige des scénarios et des preuves plutôt qu’une liste de pourcentages ou de seuils généraux. L’affouillement est décomposé sans confusion, l’érosion interne est distinguée du renard seul, la liquéfaction est reliée à la sollicitation et aux conséquences, et l’agressivité est rattachée à l’exposition et aux matériaux.

La priorisation conserve les incertitudes et les interactions. Elle prépare le passage à l’interprétation des données et au dimensionnement : le chapitre V examine comment choisir les paramètres, comparer les fondations et organiser la revue pendant l’exécution.
