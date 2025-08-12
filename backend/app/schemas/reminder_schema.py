from ..extensions import ma
from ..models.reminder import Reminder

class ReminderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reminder
        load_instance = True

reminder_schema = ReminderSchema()
reminders_schema = ReminderSchema(many=True)
