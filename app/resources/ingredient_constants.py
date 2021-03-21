# Error messages Ingredients
INGREDIENT_DOES_NOT_EXIST = "Ingredient does not exist"

# Tags Ingredients
TAG_INGREDIENTS = "ingredients"

# Aliases Ingredients
ALIAS_INGREDIENT = "ingredient"


# Query Ingredients regexes
QUERY_INGREDIENT_SORT_REGEX = "(name|created_at|updated_at):(asc|desc)"
QUERY_INGREDIENT_FILTER_REGEX = (
    r"((name)\sLIKE\s'%.*%')|((created_at|updated_at)\s[><=][=]?\s'.*')"
)

# Model length constants Ingredients
INGREDIENT_NAME_MAX = 50
INGREDIENT_DESCRIPTION_MAX = 500
