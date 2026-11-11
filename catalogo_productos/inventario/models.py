from django.db import models
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    existencias = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    imagen_url = models.URLField(blank=True)

    def __str__(self):
        return self.nombre
