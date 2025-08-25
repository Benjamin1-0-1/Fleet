from ..extensions import ma
from ..models.rental import Rental

class RentalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rental
        load_instance = True

rental_schema = RentalSchema()
rentals_schema = RentalSchema(many=True)
