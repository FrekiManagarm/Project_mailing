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
* **l'automatisation** : cette partie que j'ai plus détaillé ci-dessous nous permettra, rien qu'en ouvrant **Monit** de lancer le script. 

# 3. Dockerisation

Tout projet Docker s'articule tout d'abord autour d'un **DockerFile**. 

Je vous propose donc d'en créer un dans lequel nous allons travailler.

Nous allons maintenant, couche par couche décrire ce dont nous avons besoin. Commençons donc par l'image sur laquelle nous nous baserons :       

    FROM ubuntu : 18.04

Pour éviter toute prise de tête pour monitorer de nôtre script nous allons utiliser **Monit**. 

*Doté d'une interface simpliste mais tout de même efficace, il nous permetttra de suivre, stopper et relancer l'exécution du script depuis une page web.*

Nous allons donc rajouter dans le **DockerFile** la ligne suivante, qui inclut les outils dont nous aurons besoin pour installer **Monit** :

    RUN apt-get update && apt-get install -y wget tar 

Pour l'instant, rien d'inconnu. Nous allons également utiliser une autre commande Docker :

    ENV MONIT_VERSION 5.18

Comme on l'aura deviné, ENV va nous permettre de déclarer une constante dont nous nous servirons dans le **DockerFile** pour représenter la numéro de version de Monit. 

On va également rajouter deux commandes qui vont nous permettre de pouvoir télécharger Monit et l'installer : 

    RUN wget -O /tmp/monit-$MONIT_VERSION-linux-x64.tar.gz http://mmonit.com/monit/dist/binary/$MONIT_VERSION/monit-$MONIT_VERSION-linux-x64.tar.gz
    
    RUN cd /tmp && tar -xzf /tmp/monit-$MONIT_VERSION-linux-x64.tar.gz && cp /tmp/monit-$MONIT_VERSION/bin/monit /usr/bin/monit

Désolé, c'est un peu long, mais grâce à ces deux lignes, **Monit** sera installé dans le dossier "/usr/bin/monit" de notre future image. 

Passons maintenant à la configuration de Monit. 

## 1. Ossature d'une configuration Monit 

On a brièvement parlé sur le fonctionnement de **Monit**. On va donc pouvoir parler un peu plus en détails en survolant l'interface graphique : 

![Image de l'interface graphique de Monit](/Images/Image_Monit.png "Image de l'interface de Monit")

On peut voir sur cette belle image la liste des processus en cours qui sont monitorés par le programme, ainsi que leur état (en fonction ou non), leur durée d'exécution, etc. 

En cliquant sur un des processus, on pourra obtenir plus de détails dessus, et l’arrêter ou le relancer.

Comme tout bon logiciel, **Monit** utilise un fichier de configuration, appelé **"monitrc"**. Créons donc ce fichier dans la racine du dossier du projet et éditons-le avec les lignes ci-dessous. 

    set daemon 30                     
    // Fréquence de vérification l'état des processus monitorés, en secondes
 
    set logfile /var/log/monit.log    
    // Emplacement du fichier de logs
 
    set httpd port 2812              
    // Le port sur lequel on accèdera à l'interface de Monit

    allow admin:monit                
    // Les identifiants de connexion à l'interface
 
    include /etc/monit/conf.d/*       // Inclusion d'un dossier contenant les configurations de monitoring des différents scripts/services

On a maintenant une configuration basique au possible, mais qui ne se trouve pour le moment que dans le dossier projet : 

il ne reste donc plus qu’à la copier dans l’image.
Ajoutons donc les lignes suivantes à votre **Dockerfile** : 

    COPY ./monitrc /etc/monitrc

    RUN chmod 0700 /etc/monitrc

## 2. Le script, c'est chic !

Créons donc un repertoire « scripts » dans notre dossier de projet, et à l’intérieur, le fichier « main.py ».

Retournons maintenant sur notre Dockerfile, et ajoutons-y les lignes suivantes :

    RUN mkdir scripts

    COPY scripts /scripts

Pour éviter la confusion du Docker pour notre script il faudra donc installer les librairies par la commande suivante :

    pip install nom-du-module

Dans votre dossiers scripts, créons donc le fichier « requirements.txt », et dedans, écrivons simplement « paho-mailing », et sauvegardons.

Puis, dans notre Dockerfile :

    RUN pip install -r /scripts/requirements.txt

Au lancement du container Docker, Pip s’occupera donc d’installer tous les modules Pythons que vous aurez listé dans ce fichier.

## 3. Wrapper sur la ville 

Pour monitorer un processus, Monit se sert de fichiers nommés « PIDfiles ». Ce sont des fichiers dans lesquels sont inscrits les « numéros » de chaque processus en cours sur la machine.

Le problème avec les scripts est qu’il ne fonctionnent pas avec ces PIDfiles, et ne peuvent donc pas être monitorés par défaut.

On va donc ici se servir d’un « wrapper », ou « emballage », qui s’occupera pour nous de créer ce PIDfile. On transformera ainsi notre simple script en quelque chose qui s’apparente à un « daemon » ou service.

A la racine du projet, **créez le fichier "python_mailing"**, notre futur wrapper, et collons ces lignes à l'intérieur : 

    #!/bin/bash
 
    PIDFILE=/var/run/python_mailing.pid
 
    case $1 in
    start)
    # Launch your program as a detached process
    python /scripts/main.py &>/dev/null &
    # Get its PID and store it
    echo $! > ${PIDFILE}
    ;;
    stop)
    kill `cat ${PIDFILE}`
    # Now that it's killed, don't forget to remove the PID file
    rm ${PIDFILE}
    ;;
    *)
    echo "Usage: python_mailing {start|stop}" ;;
    esac
    exit 0

Dans le **DockerFile**, entrons ces deux lignes ci-dessous, pour placer le wrapper dans le dossier des services (init.d) et le rendre exécutable. 

    COPY python_mailing /etc/init.d/

    RUN chmod +x /etc/init.d/python_mailing

Grâce à ce wrapper, vous pourrez maintenant lancer votre script grâce à la commande « python_mailing start ». 

C’est d’ailleurs ce que Monit fera lui-même.
Si vous vous souvenez, lors de la création du fichier **monitrc** précédemment, nous avions ajouté la ligne suivante :

    include /etc/monit/conf.d/*

Cette ligne indique à Monit le répertoire dans lequel il trouvera quels scripts il doit monitorer, et leurs configurations.

Nous allons donc créer ce dossier et son contenu dans notre dossier de projet, et l’envoyer dans l’image Docker grâce au Dockerfile.

Créez donc le dossier « conf.d » à la racine de votre projet, et à l’intérieur, un fichier nommé « python_mailing », dans lequel vous entrez ces lignes :

    check process python_mailing with pidfile /var/run/python_mailing.pid
    start program = "/etc/init.d/python_mailing start"
    stop program = "/etc/init.d/python_mailing stop"

Vous vous en doutez, c’est ici qu’est faite la liaison avec le wrapper que nous avons écrit plus tôt : 

Monit se servira de ce fichier pour trouver le PIDfile de notre script, ainsi que les commandes pour le lancer et le stopper.

Encore une fois la même manipulation, on ajoute donc une ligne au Dockerfile pour copier le contenu de notre dossier conf.d au dossier /etc/monit/conf.d :

    COPY ./conf.d /etc/monit/conf.d

Et voilà ! Au lancement de Monit, notre script devrait être exécuté et monitoré.

## 4. Le Docker sur la main 

Pour finaliser notre projet, il ne nous reste plus que quelques lignes à ajouter à notre Dockerfile, mais pas des moindres.

Tout d’abord, nous avons utilisé plusieurs outils dans les différentes commandes du fichier, et pour ne pas avoir à revenir là-dessus à chaque fois, 

j’ai préféré attendre la fin de ce tutoriel pour écrire, en une seule fois, la ligne permettant de les installer ; la voici donc :

    RUN apt-get update && apt-get install -y wget \
    tar \
    build-essential \
    ca-certificates \
    gcc \
    git \
    libpq-dev \
    make \
    python-pip \
    python3.7 \
    python3.7-dev \
    && apt-get autoremove \
    && apt-get clean

Ces outils étant utilisés tout au long du Dockerfile, il faut bien penser à les installer au début du fichier, soit à la troisième ligne par exemple ; sinon, vous risquez d’obtenir quelques erreurs !

Enfin, il ne reste plus qu’à rendre disponible le port utilisé par Monit (2812, comme défini dans le monitrc), et bien entendu, lancer Monit au démarrage du container :

    EXPOSE 2812
    CMD monit -I

Ceci est naturellement à écrire à la toute fin du Dockerfile.

Il ne nous reste plus qu’à compiler l’image !

À la racine du projet, lancez donc la commande build, puis la commande run si le build s’est correctement passé :

    ~/docker/python_script_docker $ docker build -t ray/python_script .
    ~/docker/python_script_docker $ docker run -it -p 2812:2812 ray/python_script

Pour accéder à l’interface de Monit, il suffira donc, depuis votre navigateur, de vous rendre à l’adresse « localhost:2812 ».

Vous pourrez ainsi voir le statut de l’exécution de votre script Python.

Attention, il est possible que Monit vous affiche initialement une erreur sur l’exécution du script. 

Mais normalement, au bout de 30 secondes, Monit réactualise l’interface et le script apparaît correctement en « running ».








