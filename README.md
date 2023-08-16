# DaGuinci - SoftDesk

## Installation

* Cloner le depot git

``` bash
git clone git@github.com:DaGuinci/softDesk.git
```

* Créer environnement virtuel :

``` bash
python -m venv env
```

* Activer environnement virtuel :

``` bash
source env/bin/activate
```

* Installer dépendances

``` bash
pip install -r requirements.txt
```

## Exécution

* Lancer le serveur

``` bash
python manage.py runserver
```

## Commandes utiles

* Desactiver environnement virtuel :

``` bash
deactivate
```

* Sauvegarder dépendances

``` bash
pip freeze > requirements.txt
```

* Mettre à jour la base de données

``` bash
python manage.py makemigrations
python manage.py migrate
```

## Todo list

- [x] Initialize project
  - [x] Create Github repository
  - [x] Create local folder with Django
  - [x] Git init in local folder
  - [x] Manage gitignore
  - [x] Manage dependencies
  - [x] Set settings timezone
  - [x] Adapt readme.md
  - [x] Create authentication app
  - [x] Make migrations
  - [x] Git push
  - [x] Create superuser

- [ ] Design project
  - [x] Need analysis
  - [x] Class diagramm
  - [x] Paginate

- [ ] Code project
  - [ ] Create users endpoint
  - [ ] Create first endpoint
  - [ ] Install drf-spectacular
  - [ ] Reecrire contributor en action 'patch' de project

- [ ] Optimize project
  - [ ] Check optimization project document
  - [ ] Check OWASP

- [ ] Test project
  - [ ] Test readme local new install

- [ ] Clean project
  - [ ] Generate flake8 report
  - [ ] Check token duration

## Initialisation des données

### Utilisateurs

* admin-oc
password: password-oc

* string
password: string

* John
password: string

* Ringo
password: string

### Projets

* Premier projet
Propriétaire: string
Contributeurs: John

* Second projet
Propriétaire: Ringo


## Diagrammes classes uml

![Alt text](README.svg)

```plantuml
@startuml
skinparam backgroundColor #123749
skinparam roundcorner 20
skinparam classfontcolor lemon chiffon
skinparam titlefontcolor linen
skinparam arrowfontcolor linen
skinparam attributefontcolor linen

skinparam class {
BackgroundColor #123749
ArrowColor #EEB258
BorderColor #EEB258
AttributeFontColor linen
}

title SoftDesk\nClass diagram

class User {
  + userName: str
  + password: str
  + age: int
  + can_be_contacted: bool
  + can_data_be_shared: bool
  + login()
  + logout()
  + update_profile()
  + is_old_enough(): bool
  + created_time: datetime
  + create_project(Project)
}

class Contributor extends User {
' Cette classe est-elle utile ?
  + contributings: list of Contributing
  + create_issue(Project, Issue)
  + create_comment(Issue, Comment)
}

class Contributing {
  + contributor: User
  + project: Project
  + created_time: datetime
}

class Project {
  + author: User
  + description: str
  + type: choices
  back-end, front-end, IOS, Android
  + contributors: list of Contributings
  + issues: list of Issues
  + created_time: datetime
}

class Issue {
  + author: User
  + name: str
  + description: str
  + status: choices
  to do, in progress, finished
  + priority: choices
  low, medium, high
  + assigned: Contributor
  + tag: choices
  bug, task, feature
  + comments: list of Comments
  + created_time: datetime
}

class Comment {
  + author: User
  + description: str
  + issue: Issue
  + uudi: str uuidfield
  + created_time: datetime
}

Project "Possède" --> Issue
Issue "Possède" --> Comment
Contributor "Peut créer" --> Issue
Contributor "\nPeut créer" --> Comment
Contributing "gère" --> Project
Contributor "est géré par" --> Contributing
@enduml
```
