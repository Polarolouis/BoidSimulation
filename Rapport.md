<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="flo cimage">
    <img src="https://images.unsplash.com/photo-1516434233442-0c69c369b66d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80"
  alt="Logo" width="734" height="489">
  </a>

  <h3 style="color:white;font-size:40px;">Crowd Simulation Project</h3>

</div>

<!-- TABLE OF CONTENTS -->

# Sommaire
- [Sommaire](#sommaire)
- [A propos du projet](#a-propos-du-projet)
- [Fenêtre graphique en temps réel](#fenêtre-graphique-en-temps-réel)
- [Première implémentation : Modèle vectoriel](#première-implémentation--modèle-vectoriel)
  - [Calcul des distances](#calcul-des-distances)
  - [Actions des forces : Principe fondamental de la dynamique](#actions-des-forces--principe-fondamental-de-la-dynamique)
  - [Comportement boidien](#comportement-boidien)
    - [Attraction](#attraction)
    - [Orientation](#orientation)
    - [Répulsion](#répulsion)
  - [Ajouts par rapport au comportement boidien](#ajouts-par-rapport-au-comportement-boidien)
    - [Collisions](#collisions)
    - [Force du vent](#force-du-vent)
    - [Force `goal` ou objectif](#force-goal-ou-objectif)
    - [Obstacles](#obstacles)
    - [Impact de la distance sur les effets des forces](#impact-de-la-distance-sur-les-effets-des-forces)
      - [Densité : calcul](#densité--calcul)
      - [Densité application](#densité-application)
  - [Optimisations](#optimisations)
    - [Construction de listes des distances](#construction-de-listes-des-distances)
      - [Filtrage des *boids*](#filtrage-des-boids)
  - [Complexité](#complexité)
  - [La simulation précalculée pour pallier à la complexité](#la-simulation-précalculée-pour-pallier-à-la-complexité)
    - [Simulateur](#simulateur)
    - [Affichage des simulations précalculées](#affichage-des-simulations-précalculées)
  - [Usage du programme](#usage-du-programme)
- [Deuxième implémentation : Modèle particulaire](#deuxième-implémentation--modèle-particulaire)
  - [Génération des chemins optimaux pour une particule](#génération-des-chemins-optimaux-pour-une-particule)
    - [Création d'un graph de réseau](#création-dun-graph-de-réseau)
    - [Modélisation des obstacles](#modélisation-des-obstacles)
- [Documentation](#documentation)
- [Sources et ressources utilisées](#sources-et-ressources-utilisées)
  - [Modules notables de l'installation de base](#modules-notables-de-linstallation-de-base)
  - [Modules supplémentaires utilisés](#modules-supplémentaires-utilisés)
  - [Services en ligne utilisés](#services-en-ligne-utilisés)
- [Licence](#licence)
- [Contact](#contact)

# A propos du projet

**But du projet** : réalisation d'une simulation 2D de comportements de foule, en vue top-down.
On souhaite simuler un comportement de type boidien qui est régie par ces trois caractéristiques :

1. l'alignement : les individus sont attirés vers un centre de gravité global calculé entre tous les individus.
2. la séparation : les individus ne peuvent pas se superposer (ie ils ne pauvent pas avoir de collisions), ils ont donc un comportement d'évitement.
3. la cohésion : les boids se rapprocheront les uns des autres.

Globalement, on peut représenter les boids comme des points, caractérisés par leur comportement lorsqu'ils rencontrent des congénères. On peut retrouver ici un schéma simplifié qui dicte les différents comportements :

<p align="center">
<img src="https://github.com/Polarolouis/BoidSimulation/raw/main/images/Boids.png" alt="schema boid" width="400"/>
</p>

On définira donc trois zones :

- une zone rosée, qui va représenter l'attraction : tout voisin qui entre dans cette zone se verra attiré vers le boid lui même.
- une zone rouge, qui va représenter l'orientation : un voisin qui entre dans cette zone "suivra" le boid.
- une zone rouge foncée, qui représente la zone de répulsion : le voisin s'éloignera du boid en rentrant dans cette zone.

# Fenêtre graphique en temps réel

Nous avons commencé par créer une fenêtre graphique nous permettant de changer les paramètres de la simulation de manière quasi-dynamique en utilisant pour 
l'affichage la bibliothèque graphique `tkinter`(https://github.com/Polarolouis/BoidSimulation/blob/main/Rapport.md#sources-et-ressources-utilisées).
<p align="center">
<img src ="https://github.com/Polarolouis/BoidSimulation/raw/main/images/280061579_550147653192539_8183857592037787828_n.png"
  alt="fenetre graphique" width=""/>
</p>

Sur le panneau de gauche, nous pouvons pouvons voir les paramètres actuels de la simulation en cours d'exécution.
C'est sur le panneau de droite que nous pourrons changer les paramètres en temps réel pour pouvoir observer de manière directe les comportements de notre simulation.

<p align="center">
<img src="https://github.com/Polarolouis/BoidSimulation/blob/main/images/example-full-usage.gif?raw=true"
  alt="Gif d'example d'une simulation temps réelle" width=""/>
</p>

*Note*: l'image ci-dessus est un GIF visible dans le rapport sur le [dépôt GitHub](https://github.com/Polarolouis/BoidSimulation/blob/main/Rapport.md)

Nous avons implémenté un comportement de rebond aux limites du système.
Nous avons aussi implémenté une indication visuelle de la "densité" des *boids* au sein d'une simulation. Le gradient de coloration s'affiche directement sur les boids, en suivant le comportement suivant : plus la densité est forte plus la coloration rouge sera intense.

Cette fenêtre a été développé de manière à pouvoir supporter différents modules de calculs tant que ceux-ci disposent de certaines *interfaces*, ainsi on peut imaginer coder
d'autres modules de calculs, par exemple comme écrit plus haut des modules sous le paradigme du calcul impératif. Le code de la fenêtre est dans le fichier `realtime_display.py`.

# Première implémentation : Modèle vectoriel

Une première réalisation dite vectorielle a été codée (voir fichier python `boid.py` et `display.py` qui permet un affichage graphique du comportement).

Les *boids* sont définis ainsi :

```python
class Boid:
    """Boid class"""

    id = 0
    radius = 5
    near_distance_alignment = 10*radius  # Distance to be considered near
    near_distance_cohesion = 0.5*near_distance_alignment
    near_distance_separation = 4*radius
    near_distance_collision = 2.5*radius
    chaotic_probability = 0.0
    bouncing = False

    goal_position = np.array([[0], [0]], dtype=np.float64)

    number_of_around_to_be_dense = 2

    alignment_force = 1
    cohesion_force = 1
    separation_force = 1
    goal_multiplicator_force = 1
    wind_speed = 0
    wind_direction = 0

    max_speed = 3
    max_alignment_force = 1
    max_cohesion_force = 1
    max_separation_force = 1
    max_goal_force = 1

    def __init__(self, x_pos, y_pos, x_vel, y_vel, the_chosen_one=False):
        """Initialize the boid
        Arguments:
            x_pos {float} -- x position of the boid
            y_pos {float} -- y position of the boid
            x_vel {float} -- x velocity of the boid
            y_vel {float} -- y velocity of the boid
            the_chosen_one {bool} -- True if the boid is the chosen one"""

        # Identification of the boid
        self.id = Boid.id
        Boid.id += 1

        # Initialise the boid position and velocity
        self.position = np.array([[x_pos], [y_pos]], dtype=np.float64)
        self.velocity = np.array([[x_vel], [y_vel]], dtype=np.float64)
        self.acceleration = np.array([[0], [0]], dtype=np.float64)
        self.new_acceleration = np.array([[0], [0]], dtype=np.float64)

        # Initialise the boid neighbours lists
        self.near_boids_alignment = []
        self.near_boids_cohesion = []
        self.near_boids_separation = []
        self.near_boids_collision = []

        # Initialise the boid color related variables
        self.the_chosen_one = the_chosen_one
        self.color = "green" if self.the_chosen_one else "white"
        self.boids_rate = 0
        self.density = len(self.near_boids_cohesion) / \
            self.number_of_around_to_be_dense
```

Pour chaque boid, nous calculons les *boids* les plus proches (calcul de distance vectoriel)

Notre approche se fait ici dans la logique de la Programmation Orientée Objet *(POO)*, nous avons trouvé ce paradigme de programmation très utiles
pour faire des collections de structures, variables et méthodes. Cette approche est plus "intuitive" (littéraire en quelque sorte puisque le code peut se lire facilement)
mais elle présente des défauts notamment au niveau des temps d'exécution et de l'optimisation. Nous n'avons pas fait de comparaison avec un code suivant le paradigme impératif mais la
comparaison pourrait être intéressante.

## Calcul des distances

Dans un premier temps, on retrouve de manière calculatoire les *boids* qui sont proches du boid concerné, pour chaque boid présent dans la simulation.
Réaliser un premier tri en fonction des coordonées permet de réduire la complexité de l'algorithme. La fonction concernée est indiquée juste ici :

```python
    def find_near_boids(self, boids):
        """Sets a list of boids that are within a certain distance
        Arguments:
            boids {list} -- list of boids"""

        self.near_boids_alignment = []
        self.near_boids_cohesion = []
        self.near_boids_separation = []
        self.near_boids_collision = []

        filtered_boids = (boid for boid in boids if (self.id != boid.id) and ((self.position[0][0] - self.near_distance_alignment < boid.position[0][0] and self.position[1][0] - self.near_distance_alignment < boid.position[1][0]) and (
            self.position[0][0] + self.near_distance_alignment > boid.position[0][0] and self.position[1][0] + self.near_distance_alignment > boid.position[1][0])))
        logging.debug('Filtered boids: %s', filtered_boids)

        for boid in filtered_boids:
            dist = np.linalg.norm(self.position - boid.position)
            if (boid not in self.near_boids_alignment) and dist < self.near_distance_alignment and dist > self.near_distance_cohesion:
                self.near_boids_alignment.append((boid, dist))
                boid.near_boids_alignment.append((self, dist))

            if (boid not in self.near_boids_cohesion) and dist < self.near_distance_cohesion and dist > self.near_distance_separation:
                self.near_boids_cohesion.append((boid, dist))
                boid.near_boids_cohesion.append((self, dist))

            if (boid not in self.near_boids_separation) and dist < self.near_distance_separation:
                self.near_boids_separation.append((boid, dist))
                boid.near_boids_separation.append((self, dist))

            if (boid not in self.near_boids_collision) and dist < self.near_distance_collision:
                self.near_boids_collision.append((boid, dist))
                boid.near_boids_collision.append((self, dist))
```

## Actions des forces : Principe fondamental de la dynamique

Nous introduirons les effets des différentes forces en utilisant la 2ème loi de Newton (autrement appelée Principe Fondamental de la Dynamique).

Ainsi la somme des forces donnera l'accélération du *boid*, sa masse étant considéré comme valant 1. Le code appliquant cela est le suivant :

```python
    def apply_rules(self):
        """Apply the rules of the flock to the boid
        By adding the forces of the different behaviours to the acceleration"""

        logging.debug('Applying rules to boid %s', self.id)
        logging.debug('----------------------------------')

        if self.goal_force > 0:
            goal = self.goal()
            self.acceleration += goal * (1/2 - self.density)

        if self.wind_speed > 0:
            wind = self.wind()
            self.acceleration += wind

        if self.alignment_force > 0:
            alignment = self.alignment()
            self.acceleration += alignment

        if self.cohesion_force > 0:
            cohesion = self.cohesion()
            self.acceleration += cohesion * (1/2 - self.density)

        if self.separation_force > 0:
            separation = self.separation()
            self.acceleration += separation * (1 + self.density)

# [...] Ellipse de parties non essentielle à la compréhension du fonctionnement du code

# Update the boid
    def update(self, obstacles_list):
        """Update the velocity and the position of the boid
        Arguments:
            obstacles_list {list} -- List of obstacles to check against"""

        logging.debug('Boid %s is updating', self.id)
        logging.debug('Boid %s position: %s', self.id, self.position)

        # Update the velocity
        logging.debug('Boid %s is updating the velocity from %s',
                      self.id, self.velocity)
        self.velocity += self.acceleration
        logging.debug('to %s', self.velocity)

        # Chaotic behaviour
        if self.chaotic_probability < random.random():
            logging.debug('Boid %s ', self.id)
            angle = random.uniform(0, 2 * math.pi)
            self.velocity[0] += math.cos(angle)
            self.velocity[1] += math.sin(angle)

        # Collision
        if self.near_boids_collision:
            self.collision()

        # Check if the boid is out of bounds and apply the correction
        if self.bouncing:
            # If we bounce the output is the velocity
            self.velocity = self.check_edges()
        else:
            # If we don't bounce the output is the position
            self.position = self.check_edges()

        # Check if the boid will collide with an obstacle
        self.get_the_obstacles_collisions(obstacles_list)

        # If velocity exceeds the max speed, set it to the max speed
        if np.linalg.norm(self.velocity) > self.max_speed:
            logging.debug(
                'Boid %s velocity exceeds the max speed, setting it to the max speed', self.id)
            self.velocity = self.velocity / \
                np.linalg.norm(self.velocity) * self.max_speed
            logging.debug('Boid %s velocity: %s', self.id, self.velocity)
        # Update the position
        self.position += self.velocity
        logging.debug('Boid %s new position: %s', self.id, self.position)

        # If the boid is out of space, bring it back to space
        self.bring_back_to_space()

        # Reset the acceleration
        self.acceleration = np.array([[0], [0]], dtype=np.float64)
```

## Comportement boidien

### Attraction

```python
    def cohesion(self):
        """Cohesion behaviour to steer towards the average position of the boids in the near_boids list
        Returns:
            np.array([float, float]) -- [x acceleration, y acceleration]"""

        # Calculate the average position of the boids
        correction_to_avg = np.array([[0], [0]], dtype=np.float64)
        if self.near_boids_cohesion:
            position_avg = np.array([[0], [0]], dtype=np.float64)
            for boid, _ in self.near_boids_cohesion:
                position_avg += boid.position
            position_avg /= len(self.near_boids_cohesion)
            correction_to_avg = position_avg - self.position
        if np.linalg.norm(correction_to_avg) > self.max_cohesion_force:
            correction_to_avg = correction_to_avg / \
                np.linalg.norm(correction_to_avg) * self.max_cohesion_force

        logging.debug('Cohesion correction to avg: %s', correction_to_avg)
        logging.debug('The cohesion force is: %s', Boid.cohesion_force)
        logging.debug('The correction for cohesion is: %s',
                      correction_to_avg * Boid.cohesion_force)

        return correction_to_avg * Boid.cohesion_force
```

### Orientation

```python
    def alignment(self):
        """Alignment behaviour to steer towards the average heading of the boids in the near_boids list
        Returns:
            np.array([float, float]) -- [x acceleration, y acceleration]"""

        # Calculate the average heading of the boids
        heading_correction = np.array([[0], [0]], dtype=np.float64)
        if self.near_boids_alignment:
            # Taking the the fastest boid as a leader
            heading_correction = max(self.near_boids_alignment, key=lambda boid_and_distance: np.linalg.norm(
                boid_and_distance[0].velocity))[0].velocity

        if np.linalg.norm(heading_correction) > self.max_alignment_force:
            heading_correction = heading_correction / \
                np.linalg.norm(heading_correction) * self.max_alignment_force

        logging.debug('Alignment heading correction: %s', heading_correction)
        logging.debug('The alignment force is: %s', Boid.alignment_force)
        logging.debug('The correction for alignment is: %s',
                      heading_correction * Boid.alignment_force)

        return heading_correction * Boid.alignment_force
```

### Répulsion

```python
    def separation(self):
        """Separation behaviour to avoid collisions with other boids
        Returns:
            np.array([float, float]) -- [x acceleration, y acceleration]"""

        separation_correction = np.array([[0], [0]], dtype=np.float64)
        for boid, distance in self.near_boids_separation:
            diff = self.position - boid.position
            diff /= distance
            separation_correction += diff
        if self.near_boids_separation:
            separation_correction /= len(self.near_boids_separation)
        if np.linalg.norm(separation_correction):
            separation_correction = (
                separation_correction / np.linalg.norm(separation_correction)) * self.max_separation_force

        logging.debug('Separation correction: %s', separation_correction)
        logging.debug('The separation force is: %s', Boid.separation_force)
        logging.debug('The correction for separation is: %s',
                      separation_correction * Boid.separation_force)

        return separation_correction * Boid.separation_force
```

## Ajouts par rapport au comportement boidien

Nous avons ajouté une gestion plus fine de la collision afin de réduire les chevauchements de *boids*.

### Collisions

> Ici l'explication du code par Gabin Derache

```python

    def collision(self):
        """collision behavior to prevent boids from going through each other
        Returns:
            np.array([float,float]) -- [x velocity, y velocity]"""
        if len(self.near_boids_collision) == 1:
            x_vel = self.velocity[0][0]
            y_vel = self.velocity[1][0]
            vel = np.array([x_vel, y_vel], dtype=np.float64)

            for boid, distance in self.near_boids_collision:
                diff = self.position - boid.position
                diff_norm = np.linalg.norm(diff)
                x_diff = diff[0][0]
                y_diff = diff[1][0]
                if distance <= 1.9*boid.radius:
                    self.velocity = np.array(
                        [[-x_diff/diff_norm], [-y_diff/diff_norm]], dtype=np.float64)
                else:
                    normal = np.array([[-y_diff, x_diff]], dtype=np.float64)
                    normal_norm = np.linalg.norm(normal)
                    new_vel = (np.dot(normal, vel)/(normal_norm**2))*normal if normal_norm != 0 else self.velocity
                    x_new_vel = new_vel[0][0]
                    y_new_vel = new_vel[0][1]
                    self.velocity = np.array(
                        [[x_new_vel], [y_new_vel]], dtype=np.float64)
        elif len(self.near_boids_collision) == 2:
            """We want the boid to go away from it's two neighbors"""
            boid1 = self.near_boids_collision[0][0]
            boid2 = self.near_boids_collision[1][0]
            diff = boid1.position-boid2.position
            x_diff = diff[0][0]
            y_diff = diff[1][0]
            normal = np.array([[-y_diff], [x_diff]], dtype=np.float64)
            normal_norm = np.linalg.norm(normal)
            # determining if using the normal vector as velocity reduces or augments the distance between boids
            new_pos = self.position+(normal/normal_norm) if normal_norm != 0 else self.position
            new_diff = new_pos-boid1.position
            new_dist = np.linalg.norm(new_diff)
            if new_dist <= self.near_distance_collision:
                new_vel = -2 * normal / normal_norm if normal_norm != 0 else self.velocity
            else:
                new_vel = 2 * normal / normal_norm if normal_norm != 0 else self.velocity
            self.velocity = new_vel
    # (np.dot(normal,self.velocity)/(normal_norm**2))*normal
```

### Force du vent

Nous avons ajouté la possibilité de mettre un vent qui est une force d'intensité constante soufflant dans une direction choisie par un angle.

**ICI UN EXEMPLE**

### Force `goal` ou objectif

Nous avons également ajouté une force d'objectif qui attire les *boids* vers elle et permet donc en modifiant sa position de les diriger sur le terrain de simulation.

**ICI UN EXEMPLE**

### Obstacles

Afin de pouvoir modéliser des mouvements de foules nous avons implémenté la possibilité de poser des obstacles, figuré sur l'affichage temps réel par des rectangles rouges.

Les boids rebondissent alors sur ces surfaces. Nous avons fait en sorte qu'une fois la simulation lancée, il soit possible de cliquer pour poser le **coin haut-gauche** puis recliquer pour poser le **coin bas-droit**.

Il est alors assez intéressant de regarder les *boids* rebondir sur les différentes surfaces et en utilisant la force `goal` on peut observer un comportement assimilable *sous certaines conditions* à un fluide dans un tuyau.

**ICI UN EXEMPLE**

De même on peut *sous certaines conditions* observer un comportement similaire à l'évacuation d'une foule par une porte.

**ICI UN EXEMPLE**

Nous invitons le lecteur à essayer les différentes possibilités offertes par cet outil.

### Impact de la distance sur les effets des forces

Le problème des chevauchements a été une des tâches qui nous a le plus occupé et déranger, afin de le réduire nous avons intégré une prise en compte de la distance et de la densité dans l'application des forces citées plus haut.
Le code est le suivant :

#### Densité : calcul

La "densité" est calculée grâce à un paramètre que nous avons défini arbitrairement selon ce qui nous semblait acceptable.
Ainsi en prenant en compte que le rayon de cohésion est relativement faible nous avons considéré qu'avoir 2 *boids* dans le champ de cohésion était déjà élevée. *La définition choisie n'est donc pas vraiment celle d'une densité en tant que telle*.

```python
        self.density = len(self.near_boids_cohesion) / \
            self.number_of_around_to_be_dense
```

Ce code donne des résultats que nous avons jugés acceptables mais il pourrait être un point d'amélioration.

#### Densité application

```python
        if self.goal_force > 0:
            goal = self.goal()
            self.acceleration += goal * (1/2 - self.density)

        if self.wind_speed > 0:
            wind = self.wind()
            self.acceleration += wind

        if self.alignment_force > 0:
            alignment = self.alignment()
            self.acceleration += alignment

        if self.cohesion_force > 0:
            cohesion = self.cohesion()
            self.acceleration += cohesion * (1/2 - self.density)

        if self.separation_force > 0:
            separation = self.separation()
            self.acceleration += separation * (1 + self.density)
```

A noter que malgré tout à la fin, nous avons réussi à diminuer mais pas à effacer tous les chevauchement des *boids*.

## Optimisations

Afin d'essayer d'optimiser nos différentes itérations nous avons utilisées plusieurs approches :

### Construction de listes des distances

#### Filtrage des *boids*

Avant de calculer les distances nous définissons un carré autour du *boid* qui sera parcouru pour détecter les autres *boids* et calculer la distance par rapport à eux.
**Cette étape d'optimisation nous a fait gagner un temps de calcul considérable, nous permettant de doubler le nombre de *boids* que l'affichage temps réel pouvait simuler.**

Plutôt que de recalculer les distances à la volée nous faisons entre chaque itération un calcul de toutes les distances entre les différents *boids*,
ces distances sont ensuite stockées dans des listes qui sont reparcourues quand nécessaire.

Enfin les distances étant symétriques entre deux *boids* nous stockons la distance dans le *boid* considéré par la boucle comme origine et dans l'*autre boid* ainsi nous divisons par deux le nombre de calculs de distances nécessaires.

Le code se déploie donc ainsi :

```python
    def find_near_boids(self, boids):
        """Sets a list of boids that are within a certain distance
        Arguments:
            boids {list} -- list of boids"""

        self.near_boids_alignment = []
        self.near_boids_cohesion = []
        self.near_boids_separation = []
        self.near_boids_collision = []

        filtered_boids = (boid for boid in boids if (self.id != boid.id) and ((self.position[0][0] - self.near_distance_alignment < boid.position[0][0] and self.position[1][0] - self.near_distance_alignment < boid.position[1][0]) and (
            self.position[0][0] + self.near_distance_alignment > boid.position[0][0] and self.position[1][0] + self.near_distance_alignment > boid.position[1][0])))
        logging.debug('Filtered boids: %s', filtered_boids)

        for boid in filtered_boids:
            dist = np.linalg.norm(self.position - boid.position)
            if (boid not in self.near_boids_alignment) and dist < self.near_distance_alignment and dist > self.near_distance_cohesion:
                self.near_boids_alignment.append((boid, dist))
                boid.near_boids_alignment.append((self, dist))

            if (boid not in self.near_boids_cohesion) and dist < self.near_distance_cohesion and dist > self.near_distance_separation:
                self.near_boids_cohesion.append((boid, dist))
                boid.near_boids_cohesion.append((self, dist))

            if (boid not in self.near_boids_separation) and dist < self.near_distance_separation:
                self.near_boids_separation.append((boid, dist))
                boid.near_boids_separation.append((self, dist))

            if (boid not in self.near_boids_collision) and dist < self.near_distance_collision:
                self.near_boids_collision.append((boid, dist))
                boid.near_boids_collision.append((self, dist))
```

## Complexité

Nous avons pu approcher la complexité par le programme `complexity.py`.
En terme de complexité algorithmique, on observe un comportement proche du N², qui s'explique par une double succession de boucle for.

Nous avons tracé ci-dessous le temps de simulation en fonction du nombre d'objets simulés.

<p align="center">
<img src="https://i.pinimg.com/originals/17/61/fc/1761fc369490f2ebb9a135dab987269a.jpg"
 alt="Complexité temporelle du projet" width=""/>
</p>

Malgré les optimisations que nous avons implémenté, l'ordre de grandeur reste en O(N²) mais nous estimons être proche de N²/2.

## La simulation précalculée pour pallier à la complexité

N'ayant pas de nécessité d'un calcul temps réel nous avons développé des modules de pré-calcul qui génèrent des fichiers contenant les trajectoires
des différents *boids* à tous les instants.

Les modules de pré-calcul se décompose en deux parties.

### Simulateur

[precomputing_simulator.py](https://github.com/Polarolouis/BoidSimulation/blob/9927037af0fde6ff9ab84311d5ce114de85f5d35/precomputing_simulator.py)

Le simulateur se compose d'un menu de sélection des différents paramètres de la simulation (nous perdons donc l'aspect dynamique de la simulation
temps réelle).

Le simulateur fait avancer la simulation en utilisant les mêmes *interfaces* que dans la simulation temps réelle mais en se débarrassant de l'affichage,
cela permet donc de réduire un petit peu le temps de calcul.

Il utilise ensuite les différents paramètres pour nommer le fichier et l'enregistrer sous le format `json` grâce au package python dédié.

Afin de donner plus d'informations durant le temps de calcul nous avons implémenté une méthode de calcul de l'ETA (Estimated Time of Arrival, ou temps estimée d'arrivée)
et un affichage dynamique d'une bar de progression.

*Note* : les couleurs dans le terminal sont obtenues grâce au package `colored`(https://github.com/Polarolouis/BoidSimulation/blob/main/Rapport.md#sources-et-ressources-utilisées).

### Affichage des simulations précalculées

[precomputing_display.py](https://github.com/Polarolouis/BoidSimulation/blob/9927037af0fde6ff9ab84311d5ce114de85f5d35/precomputing_display.py)

L'affichage du simulateur utilise le module `tkinter`(https://github.com/Polarolouis/BoidSimulation/blob/main/Rapport.md#sources-et-ressources-utilisées) afin de générer l'affichage.
Il se compose d'un menu par terminal pour la sélection des fichiers détectés dans le dossier `/json/` et après la sélection par l'utilisateur du fichier
il affiche alors la fenêtre graphique permettant de lancer, faire pause et moduler la vitesse de la simulation.

## Usage du programme

Afin d'utiliser le programme il faut cloner le dépôt GitHub (à l'aide du bouton Clone). 

Une fois les fichiers récupérés il faut :

1 - Installer les modules non inclus dans le package de base, cela se fait en se plaçant dans le répertoire de travail et en tapant dans un terminal (Bash, CMD, PowerShell ...) la commande suivante :
```bash
python -m pip install -r requirements.txt
```

2 - Choisir le module que l'on souhaite utiliser :

- `realtime_display.py` se lance à partir d'un terminal avec :
```bash
python realtime_display.py
```
- `precomputing_simulator.py` :
```bash
python precomputing_simulator.py
```
- `precomputing_display.py` : 
```bash
python precomputing_display.py
```
3 - Utiliser les interfaces qui s'ouvrent pour simuler les *boids*.

# Deuxième implémentation : Modèle particulaire

Comme deuxième approche, nous sommes partis du constat que les foules, lorqu'elles présentent une densité suffisante, peuvent être approchées par de la mécanique des fluides (cf. https://www.shf-lhb.org/articles/lhb/pdf/1963/08/lhb1963067.pdf).

Nous sommes repartis de ce constat pour réaliser une simulation de foule avec une approche similaire à celle de Navier-Stokes.

## Génération des chemins optimaux pour une particule

Vous pouvez trouver le code correspondant à cette partie sur ce lien suivant : [code du modèle particulaire]

### Création d'un graph de réseau

Un des prérequis de l'étude que nous avons dû implémenter est l'automatisation de la recherche et de la représentation des chemins optimaux.

Nous avons pour cela utilisé un graphe de réseau. La structure était la suivante : 
- un noeud représentant l'objectif du réseau (le noeud vers lequel tous les objets présents sur le graph veulent converger).
- un ou des obstacles (modélisés sur le graph comme quatres noeds reliés entre eux deux à deux pour former des rectangles).
- un noeud représentant l'endroit d'oû part la particule en elle même (sa position initiale).

Nous avons donc implémenté une classe Node à notre système, qui est définie ainsi :

```python
class Node () :
  all_nodes = [] #the list of nodes present in the system
  def __init__(self, id = str, x_pos = int, y_pos = int, neigh = str, node_type = str) : 
    """
    Node class initialisation
    Args:
        id (str): identification of the node
        x_pos (int): x_position
        y_pos (int): y_position
        neigh (str): the neighbour nodes
        node_type (str): the node type
    """
    self.id = id
    self.x_pos = float(x_pos)
    self.y_pos = float(y_pos)
    self.neigh = neigh
    self.node_type = node_type
    
    #add the created node to the list of existing nodes
    self.all_nodes.append(self)
```

### Modélisation des obstacles 

Dans une conformation avec un seul obstacle, nous obtenons donc dans un premier temps un graph de réseau similaire à celui-ci par exemple :

<p align="center">
  <img src= "https://github.com/Polarolouis/BoidSimulation/raw/main/images/2022-05-13 11_37_35-Create Graph online and find shortest path or use other algorithm — Mozilla Fire.png" alt="Graph" width=""/>
</p>

Où les nodes 1,2,3,4 sont les "angles" de l'obstacle, et les nodes 5 et 6 sont respectivement la position initiale et le goal du réseau.

Cependant, il est nécessaire de considérer que les mouvements de particules sont impossibles au sein même de l'obstacle. Il faut pour cela "mettre à jour" le graph de réseau, de manière à éliminer les arrêtes qui traversent l'obstacle.

Nous avons pour cela implémenté la méthode suivante utilisant le module `shapely` ([documentation de la bibliothèque shapely])  :

```python
def block_intersection (self, start_node, goal_node) :
  """
  Verify that a block is obstruing the path
    Args : 
        start_node (Node): the beginning path node
        goal_node (Node): the end path node
    Returns : 
        intersections (list): the list containing all the [x,y] values of the intersection(s) with the block
  """
  intersections = []
  block_nodes = self.get_all_block () #returns all the nodes which are "block" type
  
  A = (start_node.x_pos, start_node.y_pos)
  B = (goal_node.x_pos, goal_node.y_pos)
  line1 = LineString([A, B]) #create the first line
  
  for i in range (len (block_nodes)-1) :
    C = (block_nodes[i].x_pos, block_nodes[i].y_pos)
    D = (block_nodes[i+1].x_pos, block_nodes[i+1].y_pos)
    line2 = LineString([C, D]) #create the second line

    try :
      intersec_pt = line1.intersection(line2) #if there is an intersection add it to intersections
      intersec_pt_pos = [intersec_pt.x, intersec_pt.y]
      intersections.append (intersec_pt_pos) 
                            
    except AttributeError : #else  try next line
      pass
  return(intersections)
```

Cette boucle permet de faire la liste de toutes les intersections entre une ligne donnée et les arrêtes de l'obstacle.
En couplant cette méthode avec la méthode `notation_intersections` (qui donne une note à un point d'intersection en fonction du type de l'intersection : si c'est une réelle intersection ou une intersection entre deux arrêtes de l'obstacle) et la méthode  `knock_out_path` (qui permet de mettre à jour les voisins de chaque node pour que l'obstacle soit pris en compte).

On obtient alors un graphe similaire à celui ci :
<p align="center">
  <img src= "https://github.com/Polarolouis/BoidSimulation/raw/main/images/2022-05-13 11_29_43-Create Graph online and find shortest path or use other algorithm — Mozilla Fire.png" alt="Graph intersections" width=""/>
</p>

# Documentation 

Nous avons généré de manière automatique une documentation, celle-ci est basée sur les docstrings et autres commentaires dans le code du projet.
De par l'aspect automatique cette documentation peut-être considérée comme incomplète mais sa lecture pourra permettre une compréhension globale du projet,
complété par ce rapport et l'utilisation des différent fichiers.
- [boid.py](https://htmlpreview.github.io/?https://github.com/Polarolouis/BoidSimulation/blob/9927037af0fde6ff9ab84311d5ce114de85f5d35/html/boid.html)
- [precomputing_simulator.py](https://htmlpreview.github.io/?https://github.com/Polarolouis/BoidSimulation/blob/9927037af0fde6ff9ab84311d5ce114de85f5d35/html/precomputing_simulator.html)
- [precomputing_display.py](https://htmlpreview.github.io/?https://github.com/Polarolouis/BoidSimulation/blob/9927037af0fde6ff9ab84311d5ce114de85f5d35/html/precomputing_display.html)

# Sources et ressources utilisées

- <https://betterprogramming.pub/boids-simulating-birds-flock-behavior-in-python-9fff99375118>
- <https://www.codespeedy.com/how-to-implement-dijkstras-shortest-path-algorithm-in-python/>
- ESAIM: PROCEEDINGS, July 2007, Vol.18, 143-152
Jean-Frédéric Gerbeau & Stéphane Labbé, Editors

## Modules notables de l'installation de base
- *tkinter* : [page de documentation](https://docs.python.org/fr/3/library/tk.html)

## Modules supplémentaires utilisés
- `numpy` : [site](https://numpy.org/)
- `colored` : [page sur le site PyPI](https://pypi.org/project/colored/)
- `pathlib` : [page sur le site PyPI](https://pypi.org/project/pathlib/)
- `shapely` : [page sur le site PyPI](https://pypi.org/project/Shapely/)

## Services en ligne utilisés
- [HTML Preview](https://htmlpreview.github.io/) pour l'affichage des documents HTML de la documentation auto-générée

<!-- LINKS IN THE MD -->
[documentation de la bibliothèque shapely]: https://shapely.readthedocs.io/en/stable/manual.html
[code du modèle particulaire]: https://github.com/Polarolouis/BoidSimulation/blob/boid_flow/dijkstra.py

# Licence

Ce projet est fourni sous la license du MIT, pour plus d'informations voir [`LICENSE.txt`](https://github.com/Polarolouis/BoidSimulation/raw/main/LICENSE.txt).

# Contact

Joseph Allyndrée - joseph.allyndree@agroparistech.fr

Louis Lacoste - louis.lacoste@agroparistech.fr

Gabin Derache - gabin.derache@agroparistech.fr

Project Link : <https://github.com/Polarolouis/BoidSimulation>
  