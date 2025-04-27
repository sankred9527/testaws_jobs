from dynamorm import DynaModel
from marshmallow import fields
from django.conf import settings
    


class Jobs(DynaModel):
	class Table:
		# resource_kwargs = {
		# 	'endpoint_url': settings.DB_ENDPOINT
		# }
		name = settings.DB_TABLE
		hash_key = 'uuid'
		read = 25
		write = 5

	class Schema:
		job_name = fields.String()
		content = fields.String()
		uuid = fields.String()
		status = fields.Int()
		create_at = fields.DateTime()
		start_time = fields.DateTime()
		end_time = fields.DateTime()
    


