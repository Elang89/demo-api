# Error messages recipes
RECIPE_DOES_NOT_EXIST = "Recipe does not exist"

# Tags Recipes
TAG_RECIPES = "recipes"

# Aliases Recipes
ALIAS_RECIPE = "recipe"

# Query Recipes regexes
QUERY_RECIPE_SORT_REGEX = "(name|created_at|updated_at):(asc|desc)"
QUERY_RECIPE_FILTER_REGEX = (
    r"((name)\sLIKE\s'%.*%')|((created_at|updated_at)\s[><=][=]?\s'.*')"
)

# Model length constatns Recipes
RECIPE_NAME_MAX = 50
RECIPE_DESCRIPTION_MAX = 500
