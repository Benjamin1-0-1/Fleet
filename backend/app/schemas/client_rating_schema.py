from ..extensions import ma
from ..models.client_rating import ClientRating


class ClientRatingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClientRating
        load_instance = True


client_rating_schema  = ClientRatingSchema()
client_ratings_schema = ClientRatingSchema(many=True)
