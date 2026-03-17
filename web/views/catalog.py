from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import ProductType, Product, ProductVariant
from web.forms import ProductVariantForm


@login_required
def product_type_list_view(request, bus_id):
    """This func shows the list your schemes when you create a new ptoduct"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    product_types = business.product_types.all()
    return render(request, 'web/workspace/catalog/type_list.html',{
        'business': business,
        'types': product_types, 
        'enabled_modules': business.enabled_modules.values_list('slug', flat=True)

    })

@login_required
def product_type_index_list(request, bus_id):
    """This func shows the list your title schemes when you view your catalog"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    product_types = business.product_types.all()
    return render(request, 'web/workspace/catalog/catalog_index.html',{
        'business': business,
        'types': product_types, 
        'enabled_modules': business.enabled_modules.values_list('slug', flat=True)

    })

@login_required
def product_type_add_view(request, bus_id):
    """This func creates a new scheme and saves it"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    if request.method == 'POST':
        name = request.POST.get('type_name')
        label_list = request.POST.getlist('attribute_labels')
        type_list = request.POST.getlist('attribute_types')
        unit_list = request.POST.getlist('attribute_units')
        is_service_flag = request.POST.get('is_service') == 'on'

        fields_data = []
        for i in range(len(label_list)):
            label = label_list[i]
            if label.strip():
                field_type = type_list[i] if i < len(type_list) else 'text'
                unit = unit_list[i] if i < len(unit_list) else ''
                
                tech_name = label.lower().replace(" ", "_")
                dict_item = {
                    'name': tech_name,
                    'label': label,
                    'type': field_type,
                    'unit': unit.strip() if field_type == 'number' else '', 
                    
                }
                fields_data.append(dict_item)
            
        ProductType.objects.create(business=business, name=name, fields=fields_data, is_service=is_service_flag)
        messages.success(request, f"Шаблон под названием {name} успешно создан")
        return redirect('web:product_type_list', bus_id=business.id)
    
    return render(request, 'web/workspace/catalog/type_form.html', {
        'business': business,
        'enabled_modules': business.enabled_modules.values_list('slug', flat=True)
    })

@login_required
def delete_product_type(request, bus_id, scheme_id):
    """This func deletes  your scheme"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    scheme = get_object_or_404(ProductType, business=business, id=scheme_id)
    if scheme.products.exists():
        messages.error(request, "Нельзя удалить шаблон! К нему уже привязаны товары.")
        return redirect('web:product_type_list', bus_id=business.id)
    scheme.delete()
    messages.success(request, "Шаблон успешно удален!")
    return redirect('web:product_type_list', bus_id=business.id)

@login_required
def product_add_view(request, bus_id, scheme_id):
    """This func creates a new product using scheme"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    scheme = get_object_or_404(ProductType, business=business, id=scheme_id)
    if request.method == "POST":
        is_service_flag = request.POST.get('is_service') == 'on'

        product = Product.objects.create(
            business=business,
            product_type=scheme,
            name=request.POST.get('name'),
            description=request.POST.get('description', ''),
            is_service=scheme.is_service
            )
        messages.success(request, f"Товар «{product.name}» добавлен в каталог!")
        return redirect('web:product_list_by_type', bus_id=business.id, type_id=scheme.id)
    
    return render(request, 'web/workspace/catalog/add_product.html', {
        'business': business,
        'scheme': scheme,
        'enabled_modules': business.enabled_modules.values_list('slug', flat=True)
    })

@login_required
def product_list_by_type_view(request, bus_id, type_id):
    """This func shows the list your product from the catalog"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    p_type = get_object_or_404(ProductType, business=business, id=type_id)
    products = Product.objects.filter(business=business, product_type=p_type)
    
    return render(request, 'web/workspace/catalog/product_grid.html', {
        'business': business,
        'p_type': p_type,
        'products': products,
        'enabled_modules': business.enabled_modules.values_list('slug', flat=True)
    })

@login_required
def delete_product(request, bus_id, prod_id):
    """This func deletes your choosed product"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    product = get_object_or_404(Product, business=business, id = prod_id)
    type_id = product.product_type.id
    product.delete()
    messages.success(request, "Шаблон успешно удален!")
    return redirect('web:product_list_by_type', bus_id=business.id, type_id=type_id)

@login_required
def product_detail_view(request, bus_id, prod_id):
    """This func shows the list your products variants"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    product = get_object_or_404(
        Product.objects.prefetch_related('variants__stock_items'), 
        business=business, 
        id=prod_id
    )

    return render(request, 'web/workspace/catalog/product_detail.html', {
        'business': business,
        'product': product,
        'enabled_modules': business.enabled_modules.values_list('slug', flat=True)
    })

@login_required
def variant_add_view(request, bus_id, prod_id):
    """This func adds new product varint your catalog"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    product = get_object_or_404(Product, business=business, id=prod_id)
    fields_schema = product.product_type.fields

    if request.method == "POST":
        form = ProductVariantForm(request.POST, product_type_fields=fields_schema)
        
        if form.is_valid():
            attr_dict = {}
            for item in fields_schema:
                key = item['name']
                attr_dict[key] = form.cleaned_data[f'field_{key}']

            variant = ProductVariant.objects.create(
                product=product,
                price=form.cleaned_data['price'],
                attributes=attr_dict
            )

            messages.success(request, f"Экземпляр добавлен в каталог!")
            return redirect('web:product_detail', bus_id=business.id, prod_id=product.id)
        else:
            messages.error(request, "Ошибка валидации. Проверьте правильность заполнения полей.")
    else:
        
        form = ProductVariantForm(product_type_fields=fields_schema)
    
    return render(request, 'web/workspace/catalog/add_variant.html', {
        'business': business,
        'product': product,
        'form': form,
        'enabled_modules': business.enabled_modules.values_list('slug', flat=True)
    })

@login_required
def variant_delete(request, bus_id, prod_id, variant_id):
    """This func deletes the variant product"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    product = get_object_or_404(Product, business=business, id=prod_id)
    variant = get_object_or_404(ProductVariant, product=product, id=variant_id)
    variant.delete()
    messages.success(request, f"Вариант успешно удален!")
    return redirect('web:product_detail', bus_id=business.id, prod_id=product.id)

@login_required
def variant_edit_view(request, bus_id, prod_id, variant_id):
    """This func changes the variant product"""
    business = get_object_or_404(request.user.owned_businesses, id=bus_id)
    product = get_object_or_404(Product, business=business, id=prod_id)
    variant = get_object_or_404(ProductVariant, product=product, id=variant_id)
    if request.method == 'POST':
        fields = product.product_type.fields
        attr_dict = {}

        for item in fields:
            key = item['name']
            value = request.POST.get(f'field_{key}')
            attr_dict[key] = value

        price = request.POST.get('price')

        variant.price = price  
        variant.attributes = attr_dict
        variant.save()          
        messages.success(request, f"Вариант успешно изменен!")
        return redirect('web:product_detail', bus_id=business.id, prod_id=product.id)
    return render(request, 'web/workspace/catalog/update_variant.html', {
        'business': business,
        'product': product,
        'variant': variant,
        'enabled_modules': business.enabled_modules.values_list('slug', flat=True)
    })
    
    