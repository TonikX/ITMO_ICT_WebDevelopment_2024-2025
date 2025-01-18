# Animals API Endpoints

## List Animals

`GET /system/animals/`
Returns a list of all animals.

### Permissions

Authenticated Users: Can view the list of animals.
Admin Users: Can view the list of animals.

## Retrieve Animal

`GET /system/animals/{id}/`
Retrieves a specific animal by ID.

### Permissions

Authenticated Users: Can view the animal details.
Admin Users: Can view the animal details.

## Animals In Lease

`GET /system/animals/animals_in_lease/`
Returns a list of animals that are currently in lease.

### Permissions

Authenticated Users: Can view the list of animals in lease.
Admin Users: Can view the list of animals in lease.

## Animals In Communal Cages

`GET /system/animals/animals_in_communas/`
Returns a list of animals that are in communal cages.

### Permissions

Authenticated Users: Can view the list of animals in communal cages.
Admin Users: Can view the list of animals in communal cages.

## Animals Leaving Together

`GET /system/animals/{id}/leaving_together/`
Returns a list of animals leaving together in the same area as the animal with the specified ID.

### Permissions

Authenticated Users: Can view the list of animals leaving together.
Admin Users: Can view the list of animals leaving together.

## Retrieve Area

`GET /system/locations/{id}/`
Retrieves a specific area by ID.

### Permissions

Authenticated Users: Can view the area details.
Admin Users: Can view the area details.

...

# Cage API Endpoints

## List Cages

`GET /system/locations/cage/`
Returns a list of all cages.

### Permissions

Authenticated Users: Can view the list of cages.
Admin Users: Can view the list of cages.

## Retrieve Cage

`GET /system/locations/cage/{id}/`
Retrieves a specific cage by ID.

### Permissions

Authenticated Users: Can view the cage details.
Admin Users: Can view the cage details.

...

# Diet API Endpoints

## List Diets

`GET /system/food/diets/`
Returns a list of all diets.

### Permissions

Authenticated Users: Can view the list of diets.
Admin Users: Can view the list of diets.

## Retrieve Diet

`GET /system/food/diets/{id}/`
Retrieves a specific diet by ID.

### Permissions

Authenticated Users: Can view the diet details.
Admin Users: Can view the diet details.

...

# Habitat API Endpoints

## List Habitats

`GET /system/habitats/`
Returns a list of all habitats.

### Permissions

Authenticated Users: Can view the list of habitats.
Admin Users: Can view the list of habitats.

## Retrieve Habitat

`GET /system/habitats/{id}/`
Retrieves a specific habitat by ID.

### Permissions

Authenticated Users: Can view the habitat details.
Admin Users: Can view the habitat details.

...

# Winter Place API Endpoints

## List Winter Places

`GET /system/animals/winterp-laces/`
Returns a list of all winter places.

### Permissions

Authenticated Users: Can view the list of winter places.
Admin Users: Can view the list of winter places.

## Retrieve Winter Place

`GET /system/animals/winterp-laces/{id}/`
Retrieves a specific winter place by ID.

### Permissions

Authenticated Users: Can view the winter place details.
Admin Users: Can view the winter place details.

...

# Animal In Cage API Endpoints

## List Animals in Cages

`GET /system/locations/locations/`
Returns a list of all animal-cage relations.

### Permissions

Authenticated Users: Can view the list of animal-cage relations.
Admin Users: Can view the list of animal-cage relations.

## Retrieve Animal In Cage

`GET /system/locations/locations/{id}/`
Retrieves a specific animal-cage relation by ID.

### Permissions

Authenticated Users: Can view the animal-cage relation details.
Admin Users: Can view the animal-cage relation details.

...

# Additional Custom Actions

## Show Empty Cages

`GET /system/locations/cage/show_empty/`
Returns a list of cages that are currently empty.

### Permissions

Authenticated Users: Can view the list of empty cages.
Admin Users: Can view the list of empty cages.

## Animals In a Specific Area

`GET /system/animals/animals_in/`
Returns a count of animals in each area.

### Permissions

Authenticated Users: Can view the count of animals in areas.
Admin Users: Can view the count of animals in areas.
