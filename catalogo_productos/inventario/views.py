from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria
from .forms import ProductoForm
from django.db.models import Sum, F, DecimalField
from decimal import Decimal



def lista_productos(request):
    busqueda = request.GET.get('buscar', '')
    orden = request.GET.get('orden', 'nombre')

    productos = Producto.objects.filter(
        nombre__icontains=busqueda
    )

    opciones_orden = {
        'nombre': 'nombre',
        'precio': 'precio',
        'existencias': 'existencias',
    }

    if orden in opciones_orden:
        productos = productos.order_by(opciones_orden[orden])

    total_productos = Producto.objects.count()
    total_existencias = Producto.objects.aggregate(
        total=Sum('existencias')
    )['total'] or 0

    valor_inventario = Producto.objects.aggregate(
        total=Sum(
            F('precio') * F('existencias'),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        )
    )['total'] or Decimal('0.00')
    total_categorias = Categoria.objects.count()

    return render(
        request,
        'inventario/lista_productos.html',
        {
            'productos': productos,
            'busqueda': busqueda,
            'orden': orden,
            'total_productos': total_productos,
            'total_existencias': total_existencias,
            'valor_inventario': valor_inventario,
            'total_categorias': total_categorias,
        }
    )


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()

    return render(request, 'inventario/formulario_producto.html',
                  {'form': form})



def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'inventario/formulario_producto.html',
                  {'form': form})



def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')

    return render(request, 'inventario/confirmar_eliminacion.html',
                  {'producto': producto})
