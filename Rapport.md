<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="flo cimage">
    <img src=https://images.unsplash.com/photo-1516434233442-0c69c369b66d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80
  alt="Logo" width="734" height="489">
  </a>

  <h3 style="color:white;font-size:40px;">Crowd Simulation Project</h3>

</div>

<!-- TABLE OF CONTENTS -->

<summary>Sommaire</summary>
<ol>
  <li><a href="">A propos du projet</a> </li>
  <li><a href="">Fenêtre graphique</a></li>
  <li><a href="">Première implémentation : Modèle vectoriel</a></li>
  <ul>
    <li><a href="">Calcul des distances</a></li>
    <li><a href="">Comportement boidien</a></li>
    <ol>
      <li><a href="">Attaction</a></li>
      <li><a href="">Orientation</a></li>
      <li><a href="">Repulsion</a></li>
    <ol>
  </ul>
  <li><a href="">Sources et ressources</a></li>
  <li><a href="">Contact</a></li>
</ol>

# A propos du projet

**But du projet** : réalisation d'une simulation 2D de comportements de foule, en vue top-down.
On souhaite simuler un comportement de type boidien qui est régie par ces trois caractéristiques :

1. l'alignement : les individus sont attirés vers un centre de gravité global calculé entre tous les individus.
2. la séparation : les individus ne peuvent pas se superposer (ie ils ne pauvent pas avoir de collisions), ils ont donc un comportement d'évitement.
3. la cohésion : les boids se rapprocheront les uns des autres.

Globalement, on peut représenter les boids comme des points, caractérisés par leur comportement lorsqu'ils rencontrent des congénères. On peut retrouver ici un schéma simplifié qui dicte les différents comportements :

<p align="center">
  <img src= images/boids.png alt="schema boid" width="400"/>
</p>

On définira donc trois zones :

- une zone rosée, qui va représenter l'attraction : tout voisin qui entre dans cette zone se verra attiré vers le boid lui même.
- une zone rouge, qui va représenter l'orientation : un voisin qui entre dans cette zone "suivra" le boid.
- une zone rouge foncée, qui représente la zone de répulsion : le voisin s'éloignera du boid en rentrant dans cette zone.

# Fenêtre graphique en temps réel

Nous avons commencé par créer une fenêtre graphique nous permettant de changer les paramètres de la simulation de manière quasi-dynamique.
<p align="center">
  <img src = images/280061579_550147653192539_8183857592037787828_n.png
  alt="fenetre graphique" width=""/>
</p>

Sur le panneau de gauche, nous pouvons pouvons voir les paramètres actuels de la simulation en cours d'éxecution.
C'est sur le panneau de droite que nous pourrons changer les paramètres en temps réel pour pouvoir observer de manière direct les comportements de notre simulation.

<p align="center">
  <img src=images/example_real_time_simulation.gif 
  alt="fenetre graphique" width=""/>
</p>

Nous avons implémenté un comportement de rebond aux limites du système.
Nous avons aussi implémenté une indication visuelle de la densité des boids au sein d'une simulation. Le gradient de coloration s'affiche directement sur les boids, en suivant le comportement suivant : plus la densité est forte plus la coloration rouge sera intense.

# Première implémentation : Modèle vectoriel

Une première réalisation dite vectorielle a été codée (voir fichier python `boid.py` et `display.py` qui permet un affichage graphique du comportement).

Les boids sont définis ainsi :

```python
def __init__(self, x_pos, y_pos, x_vel, y_vel, the_chosen_one = False):
        """Initialize the boid
        Arguments:
            x_pos {float} -- x position of the boid
            y_pos {float} -- y position of the boid
            x_vel {float} -- x velocity of the boid
            y_vel {float} -- y velocity of the boid
            the_chosen_one {bool} -- True if the boid is the chosen one"""
```

Pour chaque boid, nous calculons les boids les plus proches (calcul de distance vectoriel)

## Calcul des distances

Dans un premier temps, on retrouve de manière calculatoire les boids qui sont proches du boid concerné, pour chaque boid présent dans la simulation.
Réaliser un premier tri en fonction des coordonées permet de réduire la complexité de l'algorithme. La fonction concernée est indiquée juste ici :

```python
# Flock calculation
def find_near_boids(self, boids):
    """Sets a list of boids that are within a certain distance"""
    self.near_boids = []
    #filtrage préalable avec les coordonées des autres boids (sur x et sur y)
    filtered_boids = (boid for boid in boids if (not np.array_equal(self.position, boid.position)) 
    and ((self.position[0] - self.near_distance < boid.position[0] 
    and self.position[1] - self.near_distance < boid.position[1]) 
    and (self.position[0] + self.near_distance > boid.position[0] 
    and self.position[1] + self.near_distance > boid.position[1])))
    for boid in filtered_boids:
        #tri final avec la near.distance 
        if (boid not in self.near_boids) and self.distance(boid) < self.near_distance:
            self.near_boids.append(boid)
            boid.near_boids.append(self)

def distance(self, other_boid):
  """Return the distance between two boids"""
  return np.linalg.norm(self.position - other_boid.position)
```

## Comportement boidien

### Attraction

```python
def cohesion(self):
  """Cohesion behaviour to steer towards the average position of the boids in the near_boids list
  Returns : the correction to add to the velocity""" 
  # Calculate the average position of the boids
  correction_to_avg = np.array([[0], [0]], dtype=np.float64)
  if self.near_boids:
      position_avg = np.array([[0], [0]], dtype=np.float64)
      for boid in self.near_boids:
          position_avg += boid.position
      position_avg /= len(self.near_boids)
      correction_to_avg = position_avg - self.position
      if np.linalg.norm(correction_to_avg):
          correction_to_avg = correction_to_avg / np.linalg.norm(correction_to_avg) * self.max_speed
  if np.linalg.norm(correction_to_avg) > self.max_cohesion_force:
      correction_to_avg = correction_to_avg / np.linalg.norm(correction_to_avg) * self.max_cohesion_force
  return correction_to_avg
```

### Orientation

```python
# Flock behaviour
def alignment(self):
  """Alignment behaviour to steer towards the average heading of the boids in the near_boids list
  Returns : the correction to add to the velocity""" 
  # Calculate the average heading of the boids
  heading_correction = np.array([[0], [0]], dtype=np.float64)
  if self.near_boids:            
      # Taking the the fastest boid as a leader
      heading_correction = max(self.near_boids, key=lambda boid: np.linalg.norm(boid.velocity)).velocity

  if np.linalg.norm(heading_correction):
      heading_correction = heading_correction / np.linalg.norm(heading_correction) * self.max_speed
  
  if np.linalg.norm(heading_correction) > self.max_alignment_force:
      heading_correction = heading_correction / np.linalg.norm(heading_correction) * self.max_alignment_force
  return heading_correction
```

### Répulsion

```python
def separation(self):
  """Separation behaviour to avoid collisions with other boids
  Returns : the correction to add to the velocity"""
  separation_correction = np.array([[0], [0]], dtype=np.float64)
  for boid in self.near_boids:
      distance_to_boid = self.distance(boid)
      diff = self.position - boid.position
      diff /= distance_to_boid
      separation_correction += diff
  if self.near_boids:
      separation_correction /= len(self.near_boids)
  if np.linalg.norm(separation_correction) > 0:
      separation_correction = separation_correction / np.linalg.norm(separation_correction) * self.max_speed
  if np.linalg.norm(separation_correction):
      separation_correction = (separation_correction / np.linalg.norm(separation_correction)) * self.max_separation_force
  
  return separation_correction
```

## Ajout par rapport au comportement boidien
Nous avons ajouté une gestion plus fine de la collision afin de réduire les chevauchements de *boids*.
### Collisions
```python
def collision(self):
    """collision behavior to prevent boids from going through each other
    Returns:
        np.array([float,float]) -- [x velocity, y velocity]"""
    x_vel = self.velocity[0][0]
    y_vel = self.velocity[1][0]
    vel = np.array([x_vel,y_vel], dtype=np.float64)
    for boid, _ in self.near_boids_collision:
        diff = self.position - boid.position
        x_diff = diff[0][0]
        y_diff = diff[1][0]
        normal = np.array([[-y_diff,x_diff]], dtype=np.float64)
        normal_norm = np.linalg.norm(normal)
        new_vel = (np.dot(normal,vel)/(normal_norm**2))*normal
        x_new_vel = new_vel[0][0]
        y_new_vel = new_vel[0][1]
        self.velocity = np.array([[x_new_vel],[y_new_vel]], dtype=np.float)
```

## Complexité

Nous avons pu approcher la complexité par le programme `complexity.py`.
En terme de complexité algorithmique, on observe un comportement proche du N², qui s'explique par une double succession de boucle for.

On a tracé ci-dessous le temps de simulation en fonction du nombre d'objets simulés.

<p align="center">
  <img src= https://i.pinimg.com/originals/17/61/fc/1761fc369490f2ebb9a135dab987269a.jpg
 alt="fenetre graphique" width=""/>
</p>

# Deuxième implémentation : Modèle particulaire

Comme deuxième approche, nous sommes partis du constat que les foules, lorqu'elles présentent une densité suffisante, peuvent être approchées par de la mécanique des fluides (cf. https://www.shf-lhb.org/articles/lhb/pdf/1963/08/lhb1963067.pdf).

Nous sommes repartis de ce constat pour réaliser une simulation de foule avec une approche similaire à celle de Navier-Stokes.

## Génération des chemins optimaux pour une particule

Un des prérequis de l'étude que nous avons 
# Sources et ressources utilisées

- <https://betterprogramming.pub/boids-simulating-birds-flock-behavior-in-python-9fff99375118>
- <https://www.codespeedy.com/how-to-implement-dijkstras-shortest-path-algorithm-in-python/>
- ESAIM: PROCEEDINGS, July 2007, Vol.18, 143-152
Jean-Frédéric Gerbeau & Stéphane Labbé, Editors

# Contact

Joseph Allyndrée - joseph.allyndree@agroparistech.fr

Louis Lacoste - louis.lacoste@agroparistech.fr

Gabin Derache - gabin.derache@agroparistech.fr

Project Link : <https://github.com/Polarolouis/BoidSimulation>