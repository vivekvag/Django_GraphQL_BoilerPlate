import graphene
import graphql_jwt
from graphql_jwt.decorators import login_required, user_passes_test, superuser_required
from graphene_django import DjangoObjectType
from my_app.models import Restaurant

class RestaurantType(DjangoObjectType):
  class Meta:
      model = Restaurant
      fields = ("id", "name", "address")

class Query(graphene.ObjectType):
  """
  Queries for the Restaurant model
  """
  restaurants = graphene.List(RestaurantType)
  read_restaurants = graphene.Field(RestaurantType, id=graphene.Int())

  @login_required
  def resolve_restaurants(self, info, **kwargs):
    return Restaurant.objects.all()
  
  @login_required
  def resolve_read_restaurants(root, info, id):
    # get data where id in the database = id queried from the frontend
    return Restaurant.objects.get(id=id)

# Create Class code
class CreateRestaurant(graphene.Mutation):
  class Arguments:
    name = graphene.String()
    address = graphene.String()

  ok = graphene.Boolean() 
  restaurant = graphene.Field(RestaurantType)

  # @classmethod
  # @user_passes_test(lambda user: user.email.contains("@coditas"))
  @superuser_required
  def mutate(self, info, name, address):
    restaurant = Restaurant(name=name, address=address)
    restaurant.save()
    return CreateRestaurant(ok=True, restaurant=restaurant)

# Delete Class code
class DeleteRestaurant(graphene.Mutation):
  class Arguments:
    id = graphene.Int()

  ok = graphene.Boolean()

  @superuser_required
  def mutate(self, info, id):
    restaurant = Restaurant.objects.get(id=id)
    restaurant.delete()
    return DeleteRestaurant(ok=True)

# Update Class code
class UpdateRestaurant(graphene.Mutation):
  class Arguments:
    id = graphene.Int()
    name = graphene.String()
    address = graphene.String()

  ok = graphene.Boolean()
  restaurant = graphene.Field(RestaurantType)

  @superuser_required
  def mutate(self, info, id, name, address):
    restaurant = Restaurant.objects.get(id=id)
    restaurant.name = name
    restaurant.address = address
    restaurant.save()
    return UpdateRestaurant(ok=True, restaurant=restaurant)

class Mutation(graphene.ObjectType):
  token_auth = graphql_jwt.ObtainJSONWebToken.Field()
  verify_token = graphql_jwt.Verify.Field()
  refresh_token = graphql_jwt.Refresh.Field()

  create_restaurant = CreateRestaurant.Field()
  delete_restaurant = DeleteRestaurant.Field()  
  update_restaurant = UpdateRestaurant.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
