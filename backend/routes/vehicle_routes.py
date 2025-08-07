from flask_restx import Namespace, Resource
from flask_restx.reqparse import RequestParser
from extensions import db
from models import Vehicle
from datetime import datetime, timezone

# Create a namespace for fleet endpoints
fleets_ns = Namespace('fleets', description='Fleet (Vehicle) Operations')

# Parser for full create/replace operations (POST & PUT)
fleet_parser = RequestParser()
fleet_parser.add_argument('plate',           type=str,   required=True,  help='Number plate',    location='json')
fleet_parser.add_argument('make',            type=str,   required=True,  help='Make',            location='json')
fleet_parser.add_argument('color',           type=str,   required=True,  help='Color',           location='json')
fleet_parser.add_argument('classification',  type=str,   required=True,  help='Classification',  location='json')
fleet_parser.add_argument('purchase_price',  type=float, required=False, help='Purchase price',   location='json')
fleet_parser.add_argument('expected_resale', type=float, required=False, help='Expected resale',  location='json')

# Parser for partial updates (PATCH) — all fields optional
fleet_patch = RequestParser()
for arg in ['plate','make','color','classification','purchase_price','expected_resale']:
    fleet_patch.add_argument(arg, location='json')


@fleets_ns.route('/v1/fleets')
class FleetList(Resource):
    def get(self):
        """
        GET /v1/fleets
        Return a list of all vehicles in the fleet.
        """
        all_f = Vehicle.query.all()
        return {'fleets': [f.serialize() for f in all_f]}, 200

    @fleets_ns.expect(fleet_parser, validate=True)
    def post(self):
        """
        POST /v1/fleets
        Create a new vehicle record using all required fields.
        """
        args = fleet_parser.parse_args()
        v = Vehicle(**args, created_at=datetime.now(timezone.utc))
        db.session.add(v)
        db.session.commit()
        return {'message': 'Added', 'fleet': v.serialize()}, 201


@fleets_ns.route('/v1/fleets/<int:id>')
@fleets_ns.param('id', 'Fleet vehicle identifier')
class FleetDetail(Resource):
    def get(self, id):
        """
        GET /v1/fleets/<id>
        Return the details of a single vehicle.
        """
        v = Vehicle.query.get_or_404(id)
        return v.serialize(), 200

    @fleets_ns.expect(fleet_parser, validate=True)
    def put(self, id):
        """
        PUT /v1/fleets/<id>
        Replace all fields of an existing vehicle.
        """
        args = fleet_parser.parse_args()
        v = Vehicle.query.get_or_404(id)
        for k, val in args.items():
            setattr(v, k, val)
        db.session.commit()
        return {'message': 'Replaced', 'fleet': v.serialize()}, 200

    @fleets_ns.expect(fleet_patch)
    def patch(self, id):
        """
        PATCH /v1/fleets/<id>
        Update only the provided fields of an existing vehicle.
        """
        args = fleet_patch.parse_args()
        v = Vehicle.query.get_or_404(id)
        for k, val in args.items():
            if val is not None:
                setattr(v, k, val)
        db.session.commit()
        return {'message': 'Updated', 'fleet': v.serialize()}, 200

    def delete(self, id):
        """
        DELETE /v1/fleets/<id>
        Remove a vehicle record entirely.
        """
        v = Vehicle.query.get_or_404(id)
        db.session.delete(v)
        db.session.commit()
        return {'message': 'Deleted'}, 204
