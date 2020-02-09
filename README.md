# Projet Mailing en Python
-------------------------------------------------------

# 1. Les Prérequis 
Pour mettre en place le projet il nous faut deux ou trois choses :

1. Un **IDE** (pour produire du code bien évidemment) ou **éditeur de code**(comme sublime text ou notepad++) avec un terminal (si vous n'avez pas d'IDE).
2. Et votre adresse mail et de votre mot de passe (si vous vous en souvenez).
3. Pour l'étape supplémentaire de mise en conteneurisation du script il nous faut donc **Docker**.

# 2. La logique

La logique du programme est très simple, il est procédé par quelques étapes : 

* **La connection et la surveillance** : cette première partie va permettre         "d'écouter" la boîte mail en question, dont le mail et la mot de passe sera établie de base dans le fichier de configuration. 
* **La création du fichier** : la deuxième étape permettra de créer le fichier json et d'y insérer les données de l'email comme le sujet ou encore ce qu'il contient. 
* **Le stockage** : la dernière partie de ce script permettra de stocker le fichier json créé dans un répetoire prédéfini dans le fichier de configuration. 

# 3. Dockerisation

Tout projet Docker s'articule tout d'abord autour d'un **DockerFile**. Je vous propose donc d'en créer un dans lequel nous allons travailler.

Nous allons maintenant, couche par couche décrire ce dont nous avons besoin. Commençons donc par l'mage sur laquelle nous nous baserons :       

    FROM ubuntu : 18.04

Pour éviter toute prise de tête pour monitorer de nôtre script nous allons utiliser **Monit**. Doté d'une interface simpliste mais tout de même efficace, il nous permetttra de suivre, stopper et relancer l'exécution du script depuis une page web. 

Nous allons donc rajouter dans le **DockerFile** la ligne suivante, qui inclut les outils dont nous aurons besoin pour installer **Monit** :

    RUN apt-get update && apt-get install -y wget tar 

Pour l'instant, rien d'inconnu. Je vous propose donc également d'utiliser une autre commande Docker :

    ENV MONIT_VERSION 5.18

Comme vous l'aurez deviné, ENV va nous permettre de déclarer une constante dont nous nous servirons dans le **DockerFile** pour représenter la numéro de version de Monit. On va également rajouter deux commandes qui vont nous permettre de pouvoir télécharger Monit et l'installer : 

    RUN wget -O /tmp/monit-$MONIT_VERSION-linux-x64.tar.gz http://mmonit.com/monit/dist/binary/$MONIT_VERSION/monit-$MONIT_VERSION-linux-x64.tar.gz
    
    RUN cd /tmp && tar -xzf /tmp/monit-$MONIT_VERSION-linux-x64.tar.gz && cp /tmp/monit-$MONIT_VERSION/bin/monit /usr/bin/monit

Désolé, c'est un peu long, mais grâce à ces deux lignes, **Monit** sera installé dans le dossier "/usr/bin/monit" de notre future image. 
Passons maintenant à la configuration de Monit. 

## Ossature d'une configuration Monit 

On a brièvement parlé sur le fonctionnement de **Monit**. On va donc pouvoir parler un peu plus en détails en survolant l'interface graphique : 

![Image de l'interface graphique de Monit](/Images/Image_Monit.png "Image de l'interface de Monit")

On peut voir sur cette belle image la liste des processus en cours qui sont monitorés par le programme, ainsi que leur état (en fonction ou non), 






