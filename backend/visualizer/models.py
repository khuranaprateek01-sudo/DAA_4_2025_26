from django.db import models


class RunHistory(models.Model):
	category = models.CharField(max_length=32)
	algorithm = models.CharField(max_length=64)
	input_payload = models.JSONField(default=dict)
	output_payload = models.JSONField(default=dict)
	duration_ms = models.FloatField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"{self.category}:{self.algorithm} ({self.duration_ms:.2f} ms)"

