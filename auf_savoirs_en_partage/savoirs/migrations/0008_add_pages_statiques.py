# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

A_PROPOS = '''
<h1>À propos de</h1> 
	
<p> 
« Savoirs en partage » est un portail qui propose à la communauté universitaire 
de nouveaux services et des outils destinés à faciliter le travail en commun. 
Ce portail permet également l'accès unifié vers un ensemble de ressources et documents produits en partenariat avec nos universités membres.  
</p> 
<p> 
Ainsi, vous pourrez accéder depuis ce portail à : 
</p> 
 
<h2><a href="/chercheurs/">... un répertoire des chercheurs</a></h2> 
 
<p> 
Le répertoire présente une base de données de plus de 7000 chercheurs, étudiants-chercheurs et enseignants-chercheurs identifiés par domaines de recherche prioritaires. 
</p> 
 
<h2><a href="/agenda/">... un agenda scientifique</a></h2> 
 
<p> 
La possibilité est offerte aux chercheurs d'annoncer sur ce portail un évènement scientifique en l'inscrivant dans un agenda consultable par tous. 
C'est aussi un outil de communication et de veille au service des universitaires et scientifiques francophones qui leur permet de se tenir informés des manifestations scientifiques et de répondre aux appels à communications et contributions ainsi qu'aux appels à projets. 
</p> 
 
<h2><a href="/ressources/">... des ressources scientifiques</a></h2> 
 
<p> 
Le portail « Savoirs en partage » s'inscrit dans la continuité des différents projets de l'Agence universitaire de la Francophonie  visant la mise en ligne de nombreux contenus scientifiques produits par ses implantations, ses directions, ses réseaux de chercheurs, en collaboration avec ses établissements membres : ouvrages, revues, articles, cours en ligne, sites web, etc.  Ces contenus, dispersés, sont maintenant accessibles par une porte d'entrée unique. 
</p> 
 
<h2><a href="/sites/">... une sitothèque</a></h2> 
 
<p> 
Les sites retenus ici ont été créés en partenariat par l'AUF et des universités membres : cours en ligne, revues électroniques, fonds patrimoniaux, etc. constituent une source importante de ressources pédagogiques et scientifiques, à la disposition de tous. 
</p> 
 
<h2><a href="/actualites/">... des actualités scientifiques</a></h2> 
 
<p> 
Les actualités scientifiques proposés sur différents sites de l'AUF sont reprises ici. 
</p> 
 
<p>Toutes ces rubriques sont accessibles <strong>par une double entrée</strong>, 
par région ou par discipline, en fonction de la situation géographique ou des
centres d'intérêt des utilisateurs. Le contenu peut ainsi être configuré avec
précision selon les besoins des chercheurs, des directions régionales ou des
interlocuteurs sur le terrain sans qu'aucune priorité géographique ou
thématique ne soit imposée.</p>
'''

AIDE = '''
<h1>Mode d'emploi</h1> 
 
<ul> 
    <li><a href="#principes-navigation">Principes de navigation</a></li> 
    <li><a href="#repertoire">Répertoire des chercheurs</a></li> 
    <ul> 
        <li><a href="#recherche-repertoire">Recherche dans le répertoire</a></li> 
    </ul> 
    </li> 
    <li><a href="#ressources">Ressources</a></li> 
    <li><a href="#actualites">Actualités</a></li> 
    <li><a href="#agenda">Agenda</a> 
    <ul> 
        <li><a href="#soumettre-evenement">Soumettre un évènement</a></li> 
    </ul> 
    </li> 
    <li><a href="#sitotheque">Sitothèque</a></li> 
</ul> 
 
<a name="principes-navigation"></a>
<h2>Principes de navigation sur Savoirs en partage</h2> 
 
<p>Vous retrouvez sur la <a href="/">page d'accueil</a> 
l'ensemble des rubriques du portail. Pour chaque rubrique sont présentées les
derniers enregistrements dans l'ordre antéchronologique.</p> 
 
<p>Vous pouvez accéder à la rubrique en cliquant sur son titre.</p> 
 
Le portail Savoirs en partage vous permet l'accès&nbsp;: 
<ul> 
    <li>au <a href="/chercheurs/">répertoire des chercheurs</a></li> 
    <li>à des <a href="/ressources/">ressources scientifiques</a></li> 
    <li>à des <a href="/actualites/">actualités</a></li> 
    <li>à des <a href="/appels/">appels d'offres scientifiques</a></li> 
    <li>à un <a href="/agenda/">agenda scientifique</a></li> 
    <li>à une <a href="/sites/">sitothèque</a></li> 
</ul> 
 
<p>Toutes ces rubriques sont accessibles <strong>par une double entrée</strong>, par région ou par discipline.</p> 
 
<h3>Barre de recherche</h3> 
 
<p>La barre de recherche permet une <strong>recherche dans toutes les rubriques
    du portail</strong>. Vous pouvez rechercher indifféremment un nom commun ou
un nom propre, ou tout autre terme. La recherche est lancée dans les
différentes rubriques et les résultats apparaissent sous forme d'une liste pour
chaque rubrique.</p> 
 
<p>Pour une recherche contenant plusieurs termes, les résultats contenant tous
ces termes vous sont proposés. Un calcul de pertinence fait remonter les
résultats dans lesquels ces termes ou un de ces termes apparaissent dans le
titre, et selon le nombre d'occurrence de vos termes de recherche dans la
notice.</p> 
 
<p>Vous pouvez également rechercher une expression complète en la mettant entre
guillemets.</p> 
 
<p>Les caractères accentués et les marques du pluriel sont ignorés lors de la
recherche.</p> 
 
<h3>Barre de menu principale</h3> 
 
<p>En haut du site, et sur toutes ses pages, vous retrouvez notre barre de menu
qui vous permet d'entrer directement, par un simple clic, dans une rubrique et
de passer d'une rubrique à une autre.</p> 
 
<p>Vous y retrouvez également les liens vers une page de présentation du portail 
<a href="/a-propos/">À propos</a>, une page <a href="/nous-contacter/">Contact</a> 
avec nos coordonnées, les <a href="/legal/">Mentions légales</a> 
du site, et le bouton <a href="/chercheurs/connexion/">Connexion</a> qui permet aux chercheurs inscrits dans le
répertoire des chercheurs d'accéder immédiatement à leur espace personnalisé.</p> 
 
 
<h3>Menu latéral à droite</h3> 
 
<p>Les deux menus latéraux (Région, Discipline), à droite des pages du
portail, vous permettent de sélectionner une région et/ou une discipline pour
trouver rapidement les informations pertinentes sur cette région et/ou une
discipline dans l'ensemble des rubriques du portail.</p> 
 
<p>Pour cela, il vous suffit de cliquer sur une région, et ou une discipline,
qui apparaissent alors sur un fond grisé&nbsp;; un nouveau clic vous permet de
sélectionner une autre région ou discipline ou de rechercher sur « toutes les
régions » ou « toutes les disciplines ».</p> 
 
<a name="repertoire"></a>
<h2><a href="/chercheurs/">Répertoire des chercheurs</a></h2> 
 
<p>Cet outil recense les universitaires (enseignants, chercheurs, doctorants)
impliqués, ou souhaitant s'impliquer, dans les projets scientifiques appuyés
par l'AUF. Il permet à la communauté scientifique de se mobiliser sur des
projets en fonction de repères thématiques et/ou régionaux.</p> 
 
<p>Dans le cadre de la programmation quadriennale, la politique scientifique de
l'AUF s'appuie sur la mise en œuvre de projets inter-universitaires régionaux
ou internationaux. Les réseaux de chercheurs ne sont plus le critère
d'organisation du répertoire (consulter la
<a href="/chercheurs/conversion">table de passage</a>). Les chercheurs précisent
leur <a href="/domaines-de-recherche/">domaine de recherche</a>,
discipline, thème(s) et groupe(s) de recherche, et ajoutent des mots-clés pour
affiner leur profil scientifique.</p> 
 
<p>Pour <strong>compléter</strong> une nouvelle fiche d'inscription, cliquez
sur le lien suivant:<br /> 
<a href="/chercheurs/inscription/">http://www.savoirsenpartage.auf.org/chercheurs/inscription/</a></p> 
 
<p>Tous les champs obligatoires sont indiqués par un astérisque (<span style="color: red">*</span>) rouge.</p> 
 
<p>Pour <strong>mettre à jour</strong> votre fiche (chercheur déjà inscrit),
cliquez sur le lien suivant:<br /> 
<a href="/chercheurs/connexion/">http://www.savoirsenpartage.auf.org/chercheurs/connexion/</a></p> 
 
<p>Pour se <strong>désinscrire du répertoire</strong> (supprimer sa fiche
chercheur),
<ul> 
    <li>cliquez sur le lien suivant: <a href="/chercheurs/connexion/">http://www.savoirsenpartage.auf.org/chercheurs/connexion/</a></li> 
    <li>saisissez votre adresse courriel et votre mot de passe (avec lesquels vous avez créé la fiche)</li> 
    <li>cliquez sur "Vous désinscrire du répertoire" (en rouge, dans le coin droit de la fiche).</li> 
</ul> 
 
<p>Si vous avez oublié votre mot de passe, vous pouvez le réinitialiser à l'adresse suivante:<br /> 
<a href="/chercheurs/oubli-mdp/">http://www.savoirsenpartage.auf.org/chercheurs/oubli-mdp/</a></p> 
 
<p><strong>Attention:</strong> Le système ne permet pas la création de deux
fiches associées à la même adresse de courrier électronique (doublon). Avant de
compléter une nouvelle fiche, veuillez vous assurer qu'une fiche correspondant
à votre nom et à votre profil ne figure pas déjà dans le répertoire des
chercheurs.</p> 
 
<p>Les données de l'ancien répertoire (autrefois accessible depuis le lien 
<a href="http://www.chercheurs.auf.org">http://www.chercheurs.auf.org</a>)
ont été importées sans modification dans ce nouveau Répertoire, qui prend
maintenant place sur le portail Savoirs en partage.</p> 
 
<p>Il est de votre responsabilité de vous assurer que les renseignements
contenus sur votre fiche sont exacts et à jour. Vous seul pouvez apporter des
modifications à votre fiche ou supprimer votre fiche du répertoire (voir
procédure décrite ci-dessus). Les données enregistrées sont immédiatement
publiées en ligne et visibles par tous les utilisateurs du site, que ces
derniers soient inscrits ou non au répertoire des chercheurs.</p> 
 
<h3>Durée de conservation des données</h3> 
 
<p>Nous attirons votre attention sur le fait que les informations communiquées
sont enregistrées dans la base pour une période initiale de <strong>12
    mois</strong> au-delà de laquelle une revalidation ou une mise à jour de
votre fiche est nécessaire pour qu'elle reste active. Un message de rappel vous
sera adressé à ce sujet par courriel. Sans réponse de votre part, l'Agence
procédera à la suppression de votre fiche.</p> 
 
<p>Voici des précisions concernant certains champs du 
<a href="/chercheurs/inscription/">formulaire d'inscription</a> au répertoire des chercheurs.</p> 
 
<p><strong>Domaines de recherche</strong>: Ce champ est proposé à titre
d'indication complémentaire, mais il n'est pas obligatoire. Cette liste de
domaines est inspirée des anciens réseaux où le passage selon la 
<a href="/chercheurs/conversion">table de passage</a> a été fait de manière automatique.
On peut décocher la sélection en faisant « Ctrl + clique » ou « Commande
(touche pomme) » sur un Mac + clique ». Pour en sélectionner plusieurs,
maintenez appuyé « Ctrl », ou « Commande (touche pomme) » sur un Mac.</p> 
 
<p><strong>Établissement de rattachement</strong>: Après avoir sélectionné un
pays, une liste d'établissement apparaît dès la saisie partielle du nom de
l'établissement. Par exemple, si on choisit « Sénégal » et qu'on écrit « ins »,
on voit apparaître, dans un menu déroulant limité au pays présélectionné, «
Institut africain de management », « Institut sénégalais de recherches
agricoles » et « Institut supérieur de management ». Ne reste plus qu'à
sélectionner l'établissement approprié dans la liste suggérée.</p> 
 
<p>Il est à noter que la liste est limitée aux établissements membres de l'AUF.
En revanche, tout chercheur peut s'inscrire au répertoire, que son
établissement de rattachement soit membre ou non de l'AUF.</p> 
 
<p>Le répertoire attribue automatiquement une <strong>région</strong>, qui est
liée au pays de l'établissement de rattachement du chercheur, indépendamment du
lieu où se trouve le chercheur ou de la région sur laquelle portent ses travaux
de recherche. Comme il est indiqué sur la page 
<a href="/chercheurs/">http://www.savoirsenpartage.auf.org/chercheurs/</a>,
la région est ici définie au sens, non strictement géographique, du Bureau
régional de l'AUF de référence.</p> 
 
<p><strong>Discipline:</strong> La liste des disciplines procède d'un choix
fait par le conseil scientifique de l'AUF. Le mélange entre disciplines
académiques classiques, phénomènes et objectifs relève d'une tentative de
rendre mieux compte de possibles liens interdisciplinaires,
plusridisciplinaires et transdisciplinaires sur la base des priorités de l'AUF.
Si la liste est limitative, les mots clés (qui sont indexés dans la base de
données) permettent d'apporter les précisions nécessaires.</p> 
 
<p><strong>Thèmes de recherche</strong>: La description des thèmes de recherche
est limitée à 1000 signes.</p> 
 
<p><strong>Groupe de recherche</strong>: Indiquer l'appartenance à un groupe de
recherche universitaire ou laboratoire ou groupement inter-universitaire.</p> 
 
<p><strong>Adresse site Internet</strong>: Si vous le souhaitez, vous pouvez y
indiquer le lien qui renvoie vers une page personnelle (sur le site de votre
établissement par exemple) plus complète.</p> 
 
<p><strong>Expertises:</strong> Le nombre d'expertises qu'il est possible
d'ajouter n'est pas limité.</p> 
 
<p><strong>Publications:</strong> Le nombre de publications qu'il est possible
d'ajouter n'est pas limité.</p> 
 
<p><strong>Enregistrement de l'inscription:</strong> Après avoir cliqué sur «
Enregistrer l'inscription », le message suivant s'affiche: <br />« Un courriel
contenant un lien d'activation vous a été envoyé. »</p> 
 
<p>Le courriel est envoyé par <a href="mailto:contact-savoirsenpartage@auf.org">contact-savoirsenpartage@auf.org</a> 
(pensez à vérifier vos courriers indésirables ou à ajouter cette adresse dans
votre carnet d'adresse). On vous demande de confirmer votre adresse
électronique en cliquant sur le lien indiqué dans le courriel.</p> 
 
<p>Si vous rencontrez des difficultés, vous pouvez écrire à 
<a class="email" href="mailto:contact-savoirsenpartage@auf.org">contact-savoirsenpartage@auf.org</a></p> 
 
<a name="recherche-repertoire"></a>
<h3>Recherche dans le répertoire</h3> 
 
<p>Le répertoire des chercheurs est librement consultable par tous. Les fiches
sont remplies par les chercheurs eux-mêmes qui, en plus d'informations
personnelles et académiques, signalent ici leurs sujets de thèses et leurs
publications et/ou expertises éventuelles. Ils indiquent également leurs
domaines et thématiques de recherche.</p> 
 
<ul> 
    <li><p>Une <strong>recherche simple</strong> vous est proposée en entrant vos
    termes de recherche dans la fenêtre « Rechercher dans tous les champs
    »&nbsp;: vous pourrez entrer ici soit le nom et/ou prénom d'un chercheur
    soit un mot susceptible d'apparaitre sur sa fiche, une discipline, une
    région, un pays ou encore une expression exacte (entre guillemets).</p></li> 
 
    <li><p>Une <strong>recherche plus complexe</strong> est également possible en
    précisant dans quel(s) champ(s) vous souhaitez rechercher&nbsp;; vous
    pouvez entrer vos critères dans un ou plusieurs de ces champs pour
    permettre des recoupement.</p></li> 
</ul> 
 
<p>Les deux derniers champs (Discipline / Région), sous forme de listes
déroulantes, correspondent à ce qui apparaît dans le menu latéral à droite. Ils
vous permettent d'identifier rapidement les chercheurs de votre région et/ou
intéressés par une discipline précise.</p> 
 
<p>La liste de résultats qui vous est proposée fait apparaître les chercheurs
par ordre d'inscription ou de fiches actualisées récemment, les dernières
inscriptions ou mises à jour apparaissant en tête de liste.</p> 
 
<p>Vous pouvez choisir de trier cette liste par ordre alphabétique de nom,
d'établissement, ou de pays (en cliquant sur le champ correspondant, en haut de
la colonne). Un premier clic vous présente cette liste par un ordre
croissant&nbsp;; un second clic la range en ordre décroissant.</p> 
 
<a name="ressources"></a>
<h2><a href="/ressources/">Ressources</a></h2> 
 
<p>La rubrique Ressources vous donne accès à des documents, articles, ouvrages,
cours en ligne, etc. déposés sur différents sites et qui ont reçu le soutien de
l'AUF. Un moissonneur OAI nous permet de regrouper ces contenus pour les
interroger simultanément.</p> 
 
<p>La recherche se fait sur <strong>tous les champs des notices des
    documents</strong> telles qu'elles ont été créées dans ces différents sites
(et non pas sur le texte intégral des documents). Pour chaque ressources, un
lien hypertexte (derrière la mention&nbsp;: Contenu original) vous renvoie vers
le document en ligne sur des sites extérieurs.</p> 
 
<ul> 
    <li><p>Une <strong>recherche simple</strong> vous est proposée en entrant vos
    termes de recherche dans la fenêtre « Rechercher dans tous les champs
    »&nbsp;: vous pouvez entrer ici un nom commun ou un nom propre, une
    discipline, une région, un pays ou encore une expression exacte (entre
    guillemets).</p></li> 
 
    <li><p>Une <strong>recherche plus complexe</strong> est également possible
    en précisant dans quel(s) champ(s) vous souhaitez rechercher&nbsp;; vous
    pouvez entrer vos critères dans un ou plusieurs de ces champs pour
    permettre des recoupement.</p></li> 
</ul> 
 
<p>Pour une recherche contenant plusieurs termes, les résultats contenant tous
ces termes vous seront proposés. Un <strong>calcul de pertinence</strong> fait
remonter les résultats dans lesquels ces termes ou un de ces termes apparaît
dans le titre, et selon le nombre d'occurrence de vos termes de recherche dans
la notice.</p> 
 
<p>Vous pouvez également rechercher une expression complète en la mettant entre
guillemets. Les caractères accentués et les marques du pluriel sont ignorés
lors de la recherche.</p> 
 
<a name="actualites"></a>
<h2> 
    <a href="/actualites/">Actualités</a> / 
    <a href="/appels/">Appels d'offres</a> 
</h2> 
 
<p>Les rubriques "actualités" et "appels d'offres" vous permettent de retrouver
les informations scientifiques sélectionnées sur nos sites institutionnels et
nos sites régionaux.</p> 
 
<p>La recherche dans ces deux rubriques peut se faire en mode simple (rechercher
dans tous les champs) ou plus complexe, en sélectionnant les actualités selon
leur dates de parution. On retrouve, comme sur toutes les rubriques du portail,
la possibilité d'un tri par région et/ou discipline. Il est bien entendu
possible de croiser ces différentes recherches.</p> 
 
<a name="agenda"></a>
<h2><a href="/agenda/">Agenda</a></h2> 
 
<p>La possibilité est offerte aux chercheurs d'annoncer sur ce portail un
évènement scientifique en l'inscrivant dans un agenda consultable par tous.</p> 
 
<p>La recherche dans les évènements de l'agenda peut se faire en mode simple
(rechercher dans tous les champs) ou plus complexe, en sélectionnant les
actualités selon leur dates ou en précisant avec le menu déroulant le type
d'évènement qui vous interesse.  On retrouve, comme sur toutes les rubriques du
portail, la possibilité d'un tri par région ou discipline. Il est bien entendu
possible de croiser ces différentes recherches.</p> 
 
<a name="soumettre-evenement"></a>
<h3>Soumettre un évènement</h3> 
 
<p>Un bouton <a href="/agenda/evenements/creer/">Soumettre un évènement</a> en
haut à droite dans la rubrique agenda ouvre le formulaire d'annonce d'évènement
que chacun peut remplir en ligne pour annoncer à la communauté universitaire
francophone un évènement scientifique.</p> 
 
<p>Le formulaire vous permet d'indiquer pour chaque événement deux disciplines
et de lui attacher des mots-clés. Vous devez sélectionner un pays et un fuseau
horaire ( la sélection du pays entraine la saisie automatique du fuseau horaire
) dans les listes déroulante, ainsi qu'un type d'évènement&nbsp;: l'agenda
permet d'annoncer les évènements de type colloque, conférence, journée d'étude,
séminaire, appels à contribution pour les publications ou à communication pour
les colloques, appels à projet. Les cours et formations ne peuvent pas faire
l'objet d'une annonce dans cet agenda.</p> 
 
<p>Dans le champs « Description », vous pouvez présenter les thématiques de
l'évènement et donner toutes les informations utiles aux futurs
participants.</p> 
 
<p>Toutes les annonces sont validées par l'administrateur du site avant leur
publication en ligne.</p> 
 
<p>L'AUF se réserve le droit de retenir ou non une annonce&nbsp;: ne seront
conservées que les annonces susceptibles d'intéresser la communauté
universitaire. L'auteur d'une annonce autorise l'AUF à publier en ligne les
informations données sur le formulaire d'annonce d'évènement. L'auteur d'une
annonce s'engage à détenir l'autorisation de publication en ligne des
informations attachées à l'annonce. Seules les annonces complètes seront
publiées après un contrôle de la validité des informations données.</p> 
 
<a name="sitotheque"></a>
<h2><a href="/sites/">Sitothèque</a></h2> 
 
<p>La sitothèque regroupe un ensemble de sites de contenus produits par ou avec
le soutien de l'AUF.</p> 
 
<p>La recherche dans la sitothèque peut se faire en mode simple (rechercher
dans tous les champs) ou plus complexe, en sélectionnant les actualités selon
leur dates de parution. On retrouve, comme sur toutes les rubriques du portail,
la possibilité d'un tri par région et/ou discipline.</p> 
 
<h3><a href="/sites-auf/" title="recherche Google">Sites AUF</a></h3> 
 
<p>Une recherche Google est proposée pour <em>rechercher sur l'ensemble des sites présentés dans la sitothèque</em>.</p>
'''

CONTACT = '''
<h1>Nous contacter</h1> 
 
<p> 
Pour toute information sur les services proposés par ce site,<br /> 
vous pouvez nous contacter en écrivant à  : 
<span style="color: #800000;">contact-savoirsenpartage@auf.org</span> 
</p> 
<p> 
Pour toute information sur l'Agence universitaire de la francophonie,<br /> 
vous pouvez visitez notre site : 
<a href="http://www.auf.org">http://www.auf.org</a>.<br /> 
Vous y trouverez également les adresses et contacts de nos différentes implantations. 
</p> 
 
<h2>AUF (Montréal)<br />Rectorat et Siège</h2> 
<p> 
<i>Adresse postale :</i><br /> 
Case postale du Musée<br /> 
C.P. 49714<br /> 
Montréal, (Québec) H3T 2A5<br /> 
Canada
</p> 
<p> 
<i>Adresse physique :</i><br /> 
3034, Boul. Edouard-Montpetit<br /> 
Montréal, (Québec) H3T 1J7<br /> 
Canada<br /> 
<br /> 
Téléphone :	+1 514 343 66 30<br /> 
Télécopie :	+1 514 343 21 07<br /> 
</p> 
 
<h2>AUF (Paris)<br />Rectorat et Services centraux</h2> 
<p> 
<i>Adresse postale :</i><br /> 
4, place de la Sorbonne<br /> 
75005 Paris<br /> 
France 
</p> 
<p> 
 
<i>Adresse physique :</i><br /> 
4, place de la Sorbonne<br /> 
75005 Paris<br /> 
France<br /> 
<br /> 
Téléphone :	+33 1 44 41 18 18<br /> 
Télécopie :	+33 1 44 41 18 19<br /> 
</p> 
'''

LEGAL = '''
<h1>Mentions légales</h1> 
	
<p> 
© AUF - Tous droits réservés 
 
<p> 
Le contenu du site Web « Savoirs en partage » de l'AUF est proposé à titre d'information générale uniquement. 
</p> 
<p> 
Sur ce site Web, le masculin est utilisé comme représentant des deux sexes, sans discrimination à l'égard des hommes et des femmes et dans le seul but d'alléger le texte. 
</p> 
<p> 
La classification des diplômes utilisée tient compte, dans la mesure des informations disponibles, de la réforme Licence, Master, Doctorat (LMD) actuellement en cours dans une partie des pays concernés. 
</p> 
<p> 
Ce portail présente des travaux de recherche qui rendent compte de l'état de la science au moment de leur publication : l'AUF et/ou ses représentants ne peuvent en aucun cas être tenus responsables relativement à quelque préjudice, inconvénient et/ou dommage lié directement ou indirectement à la lecture, à la consultation et/ou à l'utilisation du présent site Web et/ou de son contenu. 
</p> 
<p> 
L'AUF et/ou ses représentants ne peuvent en aucun cas être tenus responsables relativement au contenu des sites Web externes pour lesquels et vers lesquels elle offre des liens. 
</p> 
<p> 
Nonobstant ce qui précède, toute commercialisation, directe ou indirecte, de quelque texte contenu dans le présent site Web est strictement interdite. 
</p> 
<p> 
En utilisant le présent site Web, vous acceptez et reconnaissez que tous et chacun de ses aspects, dont telle utilisation, sont sujets aux lois du Québec et du Canada. 
</p> 
'''

REPERTOIRE = '''
<h1>Répertoire des chercheurs</h1> 
 
<p> 
Bienvenue sur le répertoire des chercheurs francophones de l'Agence
universitaire de la Francophonie (AUF).
</p> 
<p> 
Cet outil recense les universitaires (enseignants, chercheurs, doctorants)
impliqués, ou souhaitant s'impliquer, dans les projets scientifiques appuyés
par l'AUF. Il permet à la communauté scientifique de se mobiliser sur des
projets en fonction de repères thématiques et/ou régionaux. 
</p> 
<p> 
Dans le cadre de la programmation quadriennale, la politique scientifique de
l'AUF s'appuie sur la mise en œuvre de projets inter-universitaires
régionaux ou internationaux. Les <i>réseaux de chercheurs</i> ne sont plus
le critère d'organisation du répertoire (consulter la 
<a href="/chercheurs/conversion">table de passage</a>). Les
chercheurs précisent leur <a href="/domaines-de-recherche/">domaine de recherche</a>,
discipline, thème(s) et groupe(s) de recherche, et ajoutent des mots-clés
pour affiner leur profil scientifique.
</p>
'''

RESSOURCES = '''
<h1>Ressources</h1> 
 
<p> 
Le portail « Savoirs en partage » s'inscrit dans la continuité des
différents projets de l'Agence universitaire de la Francophonie visant la
mise en ligne de nombreux contenus scientifiques produits par ses
implantations, ses directions, ses réseaux de chercheurs, en collaboration
avec ses établissements membres : ouvrages, revues, articles, cours en
ligne, etc. Un moissonneur OAI permet de regrouper ces contenus pour les
interroger simultanément.
</p> 
'''

ACTUALITES = '''
<h1>Actualités</h1>
'''

APPELS = '''
<h1>Appels d'offres scientifiques</h1> 
'''

AGENDA = '''
<h1>Agenda</h1>
 
<p>La possibilité est offerte aux chercheurs d'annoncer sur ce
portail un évènement scientifique en l'inscrivant dans un agenda
consultable par tous.  C'est aussi un outil de communication et de
veille au service des universitaires et scientifiques francophones qui
leur permet de se tenir informés des manifestations scientifiques et
de répondre aux appels à communications et contributions ainsi qu'aux
appels à projets.</p>
 
<p> 
Consulter les <a href="/agenda/evenements/utilisation/">conditions d'utilisation</a>.
</p> 
'''

TABLE_DE_PASSAGE = '''
<h1>Répertoire des chercheurs - conversion</h1> 
 
<p> 
Les anciens <b>réseaux de chercheurs</b> ont été associés aux 
<a href="/domaines-de-recherche/">domaines de recherche</a> suivants.
Les chercheurs de ces anciens réseaux ont été
associés automatiquement aux nouveaux domaines de recherche.
</p> 
 
<h2>Thématique prioritaire 1 : Langue française, diversité culturelle et linguistique</h2> 
 
<h3>Domaine de recherche "Langues pour le développement"</h3> 
<ul> 
    <li>réseau de chercheurs "Dynamique des langues et francophonie"</li> 
    <li>réseau de chercheurs "Étude du français en francophonie"</li> 
    <li>réseau de chercheurs "Lexicologie, Terminologie, Traduction"</li> 
</ul> 
 
<h3>Domaine de recherche "Littératures au Sud"</h3> 
<ul> 
    <li>réseau de chercheurs "Littérature francophone d'Afrique subsaharienne et de l'océan Indien (CRITAOI)"</li> 
    <li>réseau de chercheurs "Littératures d'enfance"</li> 
</ul> 
 
<h3>Domaine de recherche "Cultures"</h3> 
<ul> 
    <li>réseau de chercheurs "Diversité des expressions culturelles et artistiques, et mondialisations"</li> 
</ul> 
 
<h2>Thématique prioritaire 2 : État de droit, démocratie et société</h2> 
 
<h3>Domaine de recherche "Cultures juridiques et gouvernance"</h3> 
<ul> 
    <li>réseau de chercheurs "Droits fondamentaux"</li> 
    <li>réseau de chercheurs "Droit de la santé"</li> 
    <li>réseau de chercheurs "Genre, droits et citoyenneté"</li> 
</ul> 
 
<h3>Domaine de recherche "Nouvelles figures de l'État"</h3> 
<ul> 
    <li>réseau de chercheurs "Droits fondamentaux"</li> 
    <li>réseau de chercheurs "Droit de la santé"</li> 
</ul> 
 
<h3>Domaine de recherche "Francophonie institutionnelle, État(s) francophone(s) et francophonie"</h3> 
<ul> 
    <li>réseau de chercheurs "Droits fondamentaux"</li> 
    <li>réseau de chercheurs "Droit de la santé"</li> 
    <li>réseau de chercheurs "L'état de droit saisi par la philosophie"</li> 
</ul> 
 
<h2>Thématique prioritaire 3 : Environnement, eau, énergie et climat</h2> 
 
<h3>Domaine de recherche "Agronomie"</h3> 
<ul> 
    <li>réseau de chercheurs "Biotechnologies végétales"</li> 
    <li>réseau de chercheurs "Génie des procédés appliqué à l'agro-alimentaire"</li> 
    <li>réseau de chercheurs "Érosion et gestion conservatoire des eaux et des sols"</li> 
    <li>réseau de chercheurs "Environnement et développement durable"</li> 
</ul> 
 
<h3>Domaine de recherche "Biodiversité"</h3> 
<ul> 
    <li>réseau de chercheurs "Environnement et développement durable"</li> 
</ul> 
 
<h3>Domaine de recherche "Changements climatiques"</h3> 
<ul> 
    <li>réseau de chercheurs "Télédétection"</li> 
</ul> 
 
<h3>Domaine de recherche "Énergie"</h3> 
<ul> 
    <li>réseau de chercheurs "Environnement et développement durable"</li> 
</ul> 
 
<h3>Domaine de recherche "Ville durable"</h3> 
<ul> 
    <li>réseau de chercheurs "Environnement et développement durable</li> 
</ul> 
 
<h2>Thématique prioritaire 4 : Développement durable et bien-être des populations</h2> 
 
<h3>Domaine de recherche "Économie du développement"</h3> 
<ul> 
    <li>réseau de chercheurs "Entrepreneuriat"</li> 
    <li>réseau de chercheurs "Analyse économique et développement"</li> 
</ul> 
 
<h3>Domaine de recherche "Santé et bien-être des populations"</h3> 
<ul> 
    <li>réseau de chercheurs "Maladies parasitaires et vectorielles"</li> 
    <li>réseau de chercheurs "Dynamiques démographiques et sociétés"</li> 
</ul> 
 
<h2>Thématique prioritaire 5 : Économie de la connaissance</h2> 
 
<h3>Domaine de recherche "Res@TICE"</h3> 
<ul> 
    <li>réseau de chercheurs "Réseau de chercheurs en technologies de l'information et de la communication pour l'enseignement"</li> 
</ul> 
'''

DOMAINES_DE_RECHERCHE = '''
<h1>Domaines de recherche</h1> 
<dl> 
    <dt>Littératures au Sud</dt> 
    <dd>Ce domaine de recherche réaffirme la nécessité de la littérature comme
    un des enjeux de la formation de l’individu, de l’éducation et du
    développement. Non seulement elle a « un rôle aigu et précieux » à jouer
    dans la mondialisation en cours, celui d’une « mise en relation » qui nous
    permet de dire qu’elle est « un réel apprentissage du monde » (E. Glissant)
    mais elle débouche aussi sur des formations utiles dans les nouveaux
    métiers de la culture, de l’édition et des médias.</dd> 
 
    <dt>Didactique</dt> 
    <dd>L’enseignement / apprentissage du français dans ses variations
    situationnelles (culturelle, sociolinguistique, pragmatique), dans la
    variété des contextes (plurilingues, politiques, structurels), et dans ses
    relations avec les pratiques d’autres langues, tant du point de vue de ses
    référents sociaux et scientifiques que de ses objectifs, ses moyens, ses
    modalités, ses approches, ses dispositifs, ses supports et des politiques
    éducatives et linguistiques qui les organisent.</dd> 
 
    <dt>Cultures</dt> 
    <dd>La mondialisation ouvre un espace dynamique propice à la pluralisation
    des expressions culturelles et à la résistance à la standardisation des
    esprits et des modes de vie.<br />La francophonie a retenu parmi ses
    missions essentielles celle de favoriser la diversité culturelle et
    linguistique. Cette diversité s’offre au sein de notre présent sous forme
    d’un champ multiforme d’initiatives et de recherches, dont les enjeux
    concernent l’édification commune du monde contemporain. Elle appelle un
    partage des contributions savantes, des réflexions, des expériences et des
    pratiques créatives.</dd> 
 
    <dt>Langues pour le développement</dt> 
    <dd>Le domaine de recherche « Langues pour le développement » a pour buts
    d'appuyer la recherche et la formation dans la perspective d'aménager le
    lexique du français et des langues au service du développement, de décrire
    et préserver la diversité linguistique, de valoriser la langue maternelle,
    l’intercompréhension et la traduction. Il s'agit également de développer
    les méthodologies en rapport avec ces objectifs : corpus, bases de données,
    bibliographies, thésaurus…</dd> 
 
    <dt>Cultures juridiques et gouvernance</dt> 
    <dd>Question centrale: Comment peut s’instaurer dans la pratique le
    dialogue des cultures juridiques en vue de la rénovation de l’État de
    droit, de la gouvernance démocratique et des droits de l’Homme dans
    l’espace francophone ? <br />Mots-clefs: cultures juridiques, diversité
    juridique, pluralisme, État de droit, gouvernance démocratique, droits de
    l’Homme, juges et juridictions.</dd> 
 
    <dt>Nouvelles figures de l'État</dt> 
    <dd>Question centrale: Comment, et dans quelle mesure, les dynamiques
    d’institutionnalisation du pouvoir dans le monde contemporain font-elles
    émerger une pluralité de figures de l’État, notamment en contexte de crise
    ou de sortie de crise ? <br />Mots-clefs: autorité, citoyenneté, crise,
    conflit, État, institutionnalisation du pouvoir, légalité, légitimité,
    pratiques sociales, représentations sociales, sphère publique.</dd> 
 
    <dt>Francophonie institutionnelle, État(s) francophone(s) et francophonie</dt> 
    <dd>Question centrale: Dans quelle mesure et à quelles conditions la
    Francophonie peut-elle, ou doit-elle, devenir un enjeu géopolitique pour
    les États francophones, et non plus simplement un ensemble géoculturel
    original rattaché à une langue en partage, compte tenu des dynamiques
    actuelles des relations internationales ? <br />Mots-clefs: gouvernance
    mondiale, migrations internationales, sécurité internationale, communautés
    francophones, individualisation, mondialisation.</dd> 
 
    <dt>Res@TICE</dt> 
    <dd>L’arrivée massive des TICE, souvent mal contrôlée, dans les systèmes
    éducatifs, notamment ceux des pays du Sud, nécessite de revisiter certains
    concepts, de s’interroger sur les usages, les conditions d’appropriation,
    de pérennisation des dispositifs et des nouvelles ressources. Ce domaine de
    recherche vise à favoriser les partenariats entre les chercheurs de la
    francophonie du Sud, de l’Est et du Nord, à soutenir la diffusion de la
    recherche et d’assurer une animation scientifique dans le domaine des TICE,
    en lien avec des pratiques existantes ou émergentes et dans l’attention
    portée à la diversité des contextes et des cultures.</dd> 
 
    <dt>Agronomie</dt> 
    <dt>Biodiversité</dt> 
    <dt>Changements climatiques</dt> 
    <dt>Énergie</dt> 
    <dt>Ville durable</dt> 
    <dt>Économie du développement</dt> 
    <dt>Santé et bien-être des populations</dt>
</dl>
'''

CONDITIONS_AGENDA = '''
<h1>Conditions d'utilisation de l'agenda</h1> 
 
<p> 
    <b>Autorisations :</b><br /> 
    <ul> 
    <li>L'agenda est librement consultable par tous les visiteurs du site Savoirs en partage.</li> 
    <li>Les chercheurs sont invités à annoncer à la communauté universitaire
    francophone un évènement scientifique en remplissant en ligne une
    «&nbsp;fiche évènement&nbsp;»</li> 
    </ul> 
</p> 
<p> 
    <b>Critères de validation :</b><br /> 
    Votre annonce sera publiée après un contrôle de la validité des informations données.
    
</p> 
<p> 
    <b>Type d'évènement : </b><br /> 
    L'agenda scientifique permet d'annoncer les évènements de type : 
    <ul> 
    <li>Colloque, conférence</li> 
    <li>Journée d'étude, séminaire</li> 
    <li>Appels à contribution ou à communication pour colloque ou publication</li> 
    <li>Appels à projet</li> 
    <li style="color:red">NB : les cours et formations ne peuvent pas faire l'objet d'une annonce dans cet agenda.</li> 
    </ul>    
</p> 
<p> 
    <b>Droits : </b><br /> 
    <br /> 
    L'AUF se réserve le droit de retenir ou non une annonce.
    L'auteur d'une annonce  autorise l'AUF à publier en ligne les informations données sur le formulaire d'annonce d'évènement. 
    L'auteur d'une annonce s'engage à détenir l'autorisation de publication en ligne des  informations attachés à leur annonce.
</p>
'''
 
class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        orm.PageStatique.objects.create(id='a-propos', titre='À propos de Savoirs en partage',
                                    contenu=A_PROPOS)
        orm.PageStatique.objects.create(id='aide', titre='Aide', contenu=AIDE)
        orm.PageStatique.objects.create(id='contact', titre='Nous contacter', contenu=CONTACT)
        orm.PageStatique.objects.create(id='legal', titre='Mentions légales', contenu=LEGAL)
        orm.PageStatique.objects.create(id='repertoire', titre='Répertoire des chercheurs', contenu=REPERTOIRE)
        orm.PageStatique.objects.create(id='ressources', titre='Ressources', contenu=RESSOURCES)
        orm.PageStatique.objects.create(id='actualites', titre='Actualités', contenu=ACTUALITES)
        orm.PageStatique.objects.create(id='appels', titre="Appels d'offres scientifiques", contenu=APPELS)
        orm.PageStatique.objects.create(id='agenda', titre='Agenda', contenu=AGENDA)
        orm.PageStatique.objects.create(id='table-de-passage', titre='Table de passage', contenu=TABLE_DE_PASSAGE)
        orm.PageStatique.objects.create(id='domaines-de-recherche', titre='Domaines de recherche', contenu=DOMAINES_DE_RECHERCHE)
        orm.PageStatique.objects.create(id='conditions-agenda', titre="Conditions d'utilisation de l'agenda", contenu=CONDITIONS_AGENDA)

    def backwards(self, orm):
        "Write your backwards methods here."
        orm.PageStatique.objects.filter(id__in=['a-propos', 'aide', 'contact', 'legal', 'repertoire', 'ressources', 'actualites',
                                                'appels', 'agenda', 'table-de-passage', 'domaines-de-recherche',
                                                'conditions-agenda']).delete()

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datamaster_modeles.bureau': {
            'Meta': {'object_name': 'Bureau', 'db_table': "u'ref_bureau'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'implantation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Implantation']", 'db_column': "'implantation'"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_court': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nom_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Region']", 'db_column': "'region'"})
        },
        'datamaster_modeles.implantation': {
            'Meta': {'ordering': "('nom',)", 'object_name': 'Implantation', 'db_table': "u'ref_implantation'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'adresse_physique_bureau': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'adresse_physique_code_postal_avant_ville': ('django.db.models.fields.NullBooleanField', [], {'null': 'True'}),
            'adresse_physique_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'adresse_physique_pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'impl_adresse_physique'", 'db_column': "'adresse_physique_pays'", 'to': "orm['datamaster_modeles.Pays']"}),
            'adresse_physique_precision': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_precision_avant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_rue': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_physique_ville': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'adresse_postale_boite_postale': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_postale_bureau': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_postale_code_postal': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'adresse_postale_code_postal_avant_ville': ('django.db.models.fields.NullBooleanField', [], {'null': 'True'}),
            'adresse_postale_no': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'adresse_postale_pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'impl_adresse_postale'", 'db_column': "'adresse_postale_pays'", 'to': "orm['datamaster_modeles.Pays']"}),
            'adresse_postale_precision': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_postale_precision_avant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_postale_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_postale_rue': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'adresse_postale_ville': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bureau_rattachement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Implantation']", 'db_column': "'bureau_rattachement'"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'code_meteo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'commentaire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'courriel': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'courriel_interne': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'date_extension': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_fermeture': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_inauguration': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_ouverture': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fax_interne': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'fuseau_horaire': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'hebergement_convention': ('django.db.models.fields.NullBooleanField', [], {'null': 'True'}),
            'hebergement_convention_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hebergement_etablissement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'modif_date': ('django.db.models.fields.DateField', [], {}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nom_court': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nom_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Region']", 'db_column': "'region'"}),
            'remarque': ('django.db.models.fields.TextField', [], {}),
            'responsable_implantation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'statut': ('django.db.models.fields.IntegerField', [], {}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'telephone_interne': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'})
        },
        'datamaster_modeles.pays': {
            'Meta': {'ordering': "('nom',)", 'object_name': 'Pays', 'db_table': "u'ref_pays'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'code_bureau': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Bureau']", 'to_field': "'code'", 'db_column': "'code_bureau'"}),
            'code_iso3': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3', 'blank': 'True'}),
            'developpement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {}),
            'monnaie': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nord_sud': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datamaster_modeles.Region']", 'db_column': "'region'"})
        },
        'datamaster_modeles.region': {
            'Meta': {'object_name': 'Region', 'db_table': "u'ref_region'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'implantation_bureau': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gere_region'", 'db_column': "'implantation_bureau'", 'to': "orm['datamaster_modeles.Implantation']"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'datamaster_modeles.thematique': {
            'Meta': {'object_name': 'Thematique', 'db_table': "u'ref_thematique'"},
            'actif': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'savoirs.actualite': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Actualite', 'db_table': "u'actualite'"},
            'ancienid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'ancienId_actualite'", 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'db_column': "'date_actualite'"}),
            'disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'actualites'", 'blank': 'True', 'to': "orm['savoirs.Discipline']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True', 'db_column': "'id_actualite'"}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'actualites'", 'blank': 'True', 'to': "orm['datamaster_modeles.Region']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actualites'", 'to': "orm['savoirs.SourceActualite']"}),
            'texte': ('django.db.models.fields.TextField', [], {'db_column': "'texte_actualite'"}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'titre_actualite'"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'url_actualite'"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'visible_actualite'"})
        },
        'savoirs.discipline': {
            'Meta': {'ordering': "['nom']", 'object_name': 'Discipline', 'db_table': "u'discipline'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True', 'db_column': "'id_discipline'"}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '765', 'db_column': "'nom_discipline'"})
        },
        'savoirs.evenement': {
            'Meta': {'ordering': "['-debut']", 'object_name': 'Evenement'},
            'adresse': ('django.db.models.fields.TextField', [], {}),
            'approuve': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'contact': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'courriel': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'debut': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'discipline': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'discipline'", 'null': 'True', 'to': "orm['savoirs.Discipline']"}),
            'discipline_secondaire': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'discipline_secondaire'", 'null': 'True', 'to': "orm['savoirs.Discipline']"}),
            'fin': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'fuseau': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mots_cles': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pays': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'evenements'", 'null': 'True', 'to': "orm['datamaster_modeles.Pays']"}),
            'piece_jointe': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'prenom': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'evenements'", 'blank': 'True', 'to': "orm['datamaster_modeles.Region']"}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uid': ('django.db.models.fields.CharField', [], {'default': "'7bbcba58-33d6-11e0-b407-f0def13a5ffb'", 'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ville': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'savoirs.harvestlog': {
            'Meta': {'object_name': 'HarvestLog'},
            'added': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'context': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'processed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['savoirs.Record']", 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'savoirs.listset': {
            'Meta': {'object_name': 'ListSet'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'spec': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'savoirs.pagestatique': {
            'Meta': {'object_name': 'PageStatique'},
            'contenu': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'titre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'savoirs.profile': {
            'Meta': {'object_name': 'Profile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'serveurs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['savoirs.Serveur']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'savoirs.record': {
            'Meta': {'object_name': 'Record'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'alt_title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contributor': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'creation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'disciplines': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['savoirs.Discipline']", 'symmetrical': 'False', 'blank': 'True'}),
            'format': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'isbn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'issued': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'last_checksum': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'last_update': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'listsets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['savoirs.ListSet']", 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'orig_lang': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pays': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['datamaster_modeles.Pays']", 'symmetrical': 'False', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['datamaster_modeles.Region']", 'symmetrical': 'False', 'blank': 'True'}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'source': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'thematiques': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['datamaster_modeles.Thematique']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'savoirs.serveur': {
            'Meta': {'object_name': 'Serveur'},
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255', 'primary_key': 'True'})
        },
        'savoirs.sourceactualite': {
            'Meta': {'object_name': 'SourceActualite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nom': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'actu'", 'max_length': '10'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['savoirs']
