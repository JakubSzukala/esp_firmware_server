from django.db import models

class EspDevice(models.Model):
    chip_id = models.IntegerField("unique chip id")

    def __str__(self):
        return str(self.chip_id)


class HeartbeatSignal(models.Model):
    esp_device = models.ForeignKey(EspDevice, on_delete=models.CASCADE)
    heartbeat_date = models.DateTimeField("date of heartbeat signal arrival", )

    def __str__(self):
        return "ID: " + str(self.esp_device) + ", T:" + str(self.heartbeat_date)

