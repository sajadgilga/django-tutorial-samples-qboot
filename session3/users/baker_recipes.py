from model_bakery import seq
from model_bakery.recipe import Recipe

user_recipe = Recipe('auth.User', username=seq('test_user'), first_name='ali')
