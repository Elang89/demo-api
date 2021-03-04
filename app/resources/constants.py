# Error messages recipes
RECIPE_DOES_NOT_EXIST = "Recipe does not exist"

# Tags
TAG_RECIPES = "recipes"
TAG_INGREDIENTS = "ingredients"

# Aliases
ALIAS_RECIPE = "recipe"
ALIAS_INGREDIENT = "ingredient"

# Query constants
QUERY_DEFAULT_LIMIT = 50
QUERY_MAX_LIMIT = 200
QUERY_DEFAULT_OFFSET = 0

# Query recipe regexes
QUERY_RECIPE_SORT_REGEX = "(name|created_at|updated_at):(asc|desc)"
QUERY_RECIPE_FILTER_REGEX = (
    "((name)\\sLIKE\\s'.*')|((created_at|updated_at)\\s[><=][=]?\\s'.*')"
)

# Status codes
STATUS_CREATED_201 = 201
STATUS_NOT_FOUND_404 = 404
