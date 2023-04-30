CREATE TABLE recipes (
    id UUID NOT NULL,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(500) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    CONSTRAINT pkey_recipes PRIMARY KEY(id)
);

CREATE TABLE ingredients (
    id UUID NOT NULL,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(500) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    CONSTRAINT pkey_ingredients PRIMARY KEY(id)
);

CREATE TABLE ingredients_recipes (
    recipe_id UUID NOT NULL,
    ingredient_id UUID NOT NULL,
    CONSTRAINT pkey_dataset_sections PRIMARY KEY(recipe_id, ingredient_id),
    CONSTRAINT fkey_recipes FOREIGN KEY (recipe_id) REFERENCES recipes(id),
    CONSTRAINT fkey_ingredients FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
);
