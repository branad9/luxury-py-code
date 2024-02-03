from django.utils.text import slugify
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .filters import ProductFilter
from .serializers import *
from .forms import *
from PIL import Image
from io import BytesIO
from django.core.files import File
import json
import uuid
import os
from django.utils import timezone
from datetime import timedelta
import csv
from django.template.loader import render_to_string
from django.conf import settings
from io import StringIO
from home.models import Settings

from home.tasks import email_notification


def reduce_image_size(image):
    img = Image.open(image)
    thumb_io = BytesIO()
    img.save(thumb_io, "jpeg", quality=30, optimize=True)
    new_image = File(thumb_io, name=image.name)
    return new_image


def get_product_slug(instance):
    slug = slugify(instance.name)
    qs = Product.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        slug = f"{slug}-{uuid.uuid4()}"
    return slug


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def attributes(request):
    all_attributes = Attribute.objects.all()
    paginator = Paginator(all_attributes, 30)
    page = request.GET.get("page")
    paged_attributes = paginator.get_page(page)
    return render(
        request, "cms/attributes/index.html", {"attributes": paged_attributes}
    )


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def add_attribute(request):
    return render(request, "cms/attributes/add.html")


@api_view(["POST"])
@login_required
@user_passes_test(lambda user: user.is_superadmin)
def save_attribute(request):
    name = request.POST.get("name")
    active = request.POST.get("active")
    json_values = request.POST.get("values")
    values = json.loads(json_values)
    data = {"name": name, "active": active, "values": values}
    serializer = AddAttributeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": True})
    else:
        return Response({"status": False, "errors": serializer.errors})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_attribute(request, id):
    attr = get_object_or_404(Attribute, id=id)
    serializer = ReadAttributeSerializer(attr)
    if serializer:
        attributes = json.dumps(serializer.data)
    else:
        attributes = []
    return render(
        request, "cms/attributes/edit.html", {"id": id, "attributes": attributes}
    )


@api_view(["POST"])
@login_required
@user_passes_test(lambda user: user.is_superadmin)
def update_attribute(request, id):
    name = request.POST.get("name")
    active = request.POST.get("active")
    json_values = request.POST.get("values")
    values = json.loads(json_values)
    try:
        attr = Attribute.objects.get(id=id)
    except Attribute.DoesNotExist:
        return Response(
            {"status": False, "errors": {"Error": ["Attribute not found."]}}
        )
    values_data = []
    for i in values:
        if "id" in i.keys():
            values_data.append({"attribute": attr.id, "id": i["id"], "name": i["name"]})
        else:
            values_data.append({"name": i["name"]})
    data = {"name": name, "active": active, "values": values_data}
    serializer = UpdateAttributeSerializer(attr, partial=True, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": True})
    else:
        return Response({"status": False, "errors": serializer.errors})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_attribute(request, id):
    Attribute.objects.filter(id=id).delete()
    return redirect("cms_attributes")


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def products(request):
    sort = request.GET.get("sort") or "-created"
    all_products = Product.objects.order_by(sort)
    filters = ProductFilter(request.GET, queryset=all_products)
    filtered_products = filters.qs
    paginator = Paginator(filtered_products, 30)
    page = request.GET.get("page")
    paged_products = paginator.get_page(page)
    return render(
        request,
        "cms/products/index.html",
        {"products": paged_products, "filters": filters},
    )


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def add_product(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    tags = Tag.objects.all()
    attrs = Attribute.objects.all()
    serializer = ReadAttributeSerializer(attrs, many=True)
    if serializer:
        attributes = json.dumps(serializer.data)
    else:
        attributes = []
    context = {
        "categories": categories,
        "brands": brands,
        "tags": tags,
        "attributes": attributes,
    }
    return render(request, "cms/products/add.html", context)


@api_view(["POST"])
@login_required
@user_passes_test(lambda user: user.is_superadmin)
def save_product(request):
    json_product = request.POST.get("product")
    product = json.loads(json_product)
    image_files = request.FILES.getlist("images")
    json_images_meta = request.POST.getlist("imagesMeta")

    images = []
    for i, image in enumerate(image_files):
        image_meta = json.loads(json_images_meta[i])

        for img in images:
            if img['name'] == image_meta["name"]:
                errors = {'images': {i: {'name': ['Image name must be unique.']}}}
                return Response({"status": False, "errors": errors})

        images.append(
            {
                "image": image,
                "name": image_meta["name"],
                "alt": image_meta["alt"],
                "default": i == 0,
            }
        )

    if product["type"] == "Simple":
        data = {
            "name": product["name"],
            "code": str(uuid.uuid4()),
            "main_category": product["main_category"],
            "category": product["category"],
            "subcategory": product["subcategory"],
            "brand": product["brand"],
            "type": product["type"],
            "price": product["price"],
            "sale_price": product["sale_price"],
            "desc": product["desc"],
            "reference": product["reference"],
            "opening_qty": product["qty"],
            "in_stock": product["in_stock"],
            "images": images,
            "pre_order": product["pre_order"],
            "pre_order_date": product["pre_order_date"],
            "pre_order_msg": product["pre_order_msg"],
            "length": product["length"],
            "width": product["width"],
            "height": product["height"],
            "specs": product["specs"],
            "active": product["active"],
            "meta_title": product["meta_title"],
            "meta_description": product["meta_description"],
            "schema": product["schema"],
            "robots": product["robots"],
            "keywords": product["keywords"],
        }
        serializer = AddSimpleProductSerializer(data=data)
    else:
        json_variations = request.POST.get("variations")
        variations = json.loads(json_variations)
        data = {
            "name": product["name"],
            "code": str(uuid.uuid4()),
            "main_category": product["main_category"],
            "category": product["category"],
            "subcategory": product["subcategory"],
            "brand": product["brand"],
            "type": product["type"],
            "desc": product["desc"],
            "reference": product["reference"],
            "in_stock": product["in_stock"],
            "images": images,
            "length": product["length"],
            "width": product["width"],
            "height": product["height"],
            "pre_order": product["pre_order"],
            "pre_order_date": product["pre_order_date"],
            "pre_order_msg": product["pre_order_msg"],
            "specs": product["specs"],
            "active": product["active"],
            "variations": variations,
            "meta_title": product["meta_title"],
            "meta_description": product["meta_description"],
            "schema": product["schema"],
            "robots": product["robots"],
            "keywords": product["keywords"],
        }

        serializer = AddVariableProductSerializer(data=data)
    if serializer.is_valid():
        obj = serializer.save()
        obj.slug = get_product_slug(obj)
        obj.save()
        return Response({"status": True})
    else:
        return Response({"status": False, "errors": serializer.errors})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if product.type == "Simple":
        serializer = ReadSimpleProductSerializer(product)
    else:
        serializer = ReadVariableProductSerializer(product)
    if serializer:
        product = json.dumps(serializer.data)
    else:
        product = None
    categories = Category.objects.all()
    brands = Brand.objects.all()
    tags = Tag.objects.all()
    attributes = Attribute.objects.order_by("created")
    serializer = ReadAttributeSerializer(attributes, many=True)
    if serializer:
        attributes = json.dumps(serializer.data)
    else:
        attributes = []
    context = {
        "categories": categories,
        "brands": brands,
        "tags": tags,
        "attributes": attributes,
        "product": product,
        "id": id,
    }
    return render(request, "cms/products/edit.html", context)


@api_view(["POST"])
@login_required
@user_passes_test(lambda user: user.is_superadmin)
def update_product(request, id):
    try:
        prod = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({"status": False, "errors": {"Error": ["Product not found."]}})
    json_product = request.POST.get("product")
    product = json.loads(json_product)

    image_files = request.FILES.getlist("images")
    json_images_meta = request.POST.getlist("imagesMeta")
    json_images_to_delete = request.POST.get("imagesToDelete")

    # Update product images
    images_to_delete = json.loads(json_images_to_delete)
    ProductImage.objects.filter(pk__in=images_to_delete).delete()

    image_errors = {}
    for i, json_image_meta in enumerate(json_images_meta):
        image_meta = json.loads(json_image_meta)
        img = {
            "id": image_meta["id"],
            "name": image_meta["name"],
            "alt": image_meta["alt"],
            "product": prod.pk,
        }

        for file in image_files:
            if f"pid-{img['id']}" in file.name or f"index-{i}" in file.name:
                img["image"] = file

        if img.get("id"):
            obj = ProductImage.objects.get(pk=img["id"])
            serializer = ProductImageSerializer(instance=obj, data=img, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                image_errors[i] = serializer.errors

        else:
            serializer = ProductImageSerializer(data=img)
            if serializer.is_valid():
                serializer.save()
            else:
                image_errors[i] = serializer.errors
            
    if len(image_errors) > 0:
        return Response({"status": False, "errors": {'images': image_errors}})

    if prod.type == "Simple":
        data = {
            "name": product["name"],
            "main_category": product["main_category"],
            "category": product["category"],
            "subcategory": product["subcategory"],
            "brand": product["brand"],
            "type": product["type"],
            "price": product["price"],
            "sale_price": product["sale_price"],
            "desc": product["desc"],
            "reference": product["reference"],
            "tag": product["tag"],
            "opening_qty": product["qty"],
            "in_stock": product["in_stock"],
            "pre_order": product["pre_order"],
            "pre_order_date": product["pre_order_date"] or None,
            "pre_order_msg": product["pre_order_msg"],
            "length": product["length"],
            "width": product["width"],
            "height": product["height"],
            "specs": product["specs"],
            "active": product["active"],
            "meta_title": product["meta_title"],
            "meta_description": product["meta_description"],
            "schema": product["schema"],
            "robots": product["robots"],
            "keywords": product["keywords"],
        }
        serializer = UpdateSimpleProductSerializer(prod, partial=True, data=data)
    else:
        json_variations = request.POST.get("variations")
        variations = json.loads(json_variations)
        variations_data = []
        # print(f'product are {product}')
        # print(f'variations are {variations}')
        for i in variations:
            if "id" in i.keys():
                variations_data.append(
                    {
                        "product": prod.id,
                        "id": i["id"],
                        "price": i["price"],
                        "sale_price": i["sale_price"],
                        "opening_qty": i["opening_qty"],
                        "in_stock": i["in_stock"],
                        "values": i["values"],
                    }
                )
            else:
                variations_data.append(
                    {
                        "price": i["price"],
                        "sale_price": i["sale_price"],
                        "opening_qty": i["opening_qty"],
                        "in_stock": i["in_stock"],
                        "values": i["values"],
                    }
                )

        data = {
            "name": product["name"],
            "main_category": product["main_category"],
            "category": product["category"],
            "subcategory": product["subcategory"],
            "brand": product["brand"],
            "type": product["type"],
            "desc": product["desc"],
            "reference": product["reference"],
            "tag": product["tag"],
            "in_stock": product["in_stock"],
            "length": product["length"],
            "width": product["width"],
            "height": product["height"],
            "pre_order": product["pre_order"],
            "pre_order_date": product["pre_order_date"] or None,
            "pre_order_msg": product["pre_order_msg"],
            "active": product["active"],
            "specs": product["specs"],
            "variations": variations_data,
            "meta_title": product["meta_title"],
            "meta_description": product["meta_description"],
            "schema": product["schema"],
            "robots": product["robots"],
            "keywords": product["keywords"],
        }

        serializer = UpdateVariableProductSerializer(prod, partial=True, data=data)
    if serializer.is_valid():
        obj = serializer.save()
        obj.slug = get_product_slug(obj)
        obj.save()
        return Response({"status": True})
    else:
        return Response({"status": False, "errors": serializer.errors})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_product(request, id):
    Product.objects.filter(id=id).delete()
    return redirect("cms_products")


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def product_images(request, pid):
    product = get_object_or_404(Product, id=pid)
    images = ProductImage.objects.filter(product=product)
    paginator = Paginator(images, 30)
    page = request.GET.get("page")
    paged_images = paginator.get_page(page)
    return render(
        request,
        "cms/product_images/index.html",
        {"images": paged_images, "product": product, "pid": pid},
    )


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def add_product_image(request, pid):
    product = get_object_or_404(Product, id=pid)
    if request.method == "POST":
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            f = form.save(commit=False)
            f.product = product
            f.cmp_image = reduce_image_size(image)
            f.save()
            return redirect("cms_product_images", pid)
        else:
            messages.error(request, form.errors)
            return render(
                request, "cms/product_images/add.html", {"form": form, "pid": pid}
            )
    else:
        form = ProductImageForm(None)
        return render(
            request, "cms/product_images/add.html", {"form": form, "pid": pid}
        )


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_product_image(request, pid, id):
    product = get_object_or_404(Product, id=pid)
    try:
        item = ProductImage.objects.get(id=id)
    except ProductImage.DoesNotExist:
        return redirect("cms_product_images", pid)
    if request.method == "POST":
        form = ProductImageForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            image = form.cleaned_data["image"]
            f = form.save(commit=False)
            f.product = product
            if f.cmp_image is not None:
                if len(f.cmp_image) > 0:
                    os.remove(f.cmp_image.path)
            f.cmp_image = reduce_image_size(image)
            f.save()
            return redirect("cms_product_images", pid)
        else:
            messages.error(request, form.errors)
            return render(
                request, "cms/product_images/edit.html", {"form": form, "pid": pid}
            )
    else:
        form = ProductImageForm(instance=item)
        return render(
            request, "cms/product_images/edit.html", {"form": form, "pid": pid}
        )


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_product_image(request, pid, id):
    ProductImage.objects.filter(id=id).delete()
    return redirect("cms_product_images", pid)


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def product_image_default(request, pid, id):
    ProductImage.objects.filter(product_id=pid).update(default=False)
    try:
        pi = ProductImage.objects.get(id=id)
        pi.default = True
        pi.save()
        return JsonResponse({"status": True})
    except ProductImage.DoesNotExist:
        pass
    return JsonResponse({"status": True})


def email_product_enquiry_report(request):
    yesterday = timezone.now() - timedelta(days=1)
    enquiries = ProductEnquiry.objects.filter(created__date=yesterday)
    setting = Settings.objects.first()

    file = StringIO()
    writer = csv.writer(file)
    writer.writerow(["Product", "Phone No."])
    for enquiry in enquiries.values_list("product__name", "phone"):
        writer.writerow(enquiry)

    try:
        filename = f"Product Enquiries - {yesterday.date()}.csv"
        email = setting.email
        mail_subject = f"Product Enquiries - {yesterday.date()}"
        message = render_to_string(
            "emails/product_enquiry_report.html", context={"date": yesterday.date()}
        )
        attachment = {
            "filename": filename,
            "content": file.getvalue(),
            "mimetype": "text/csv",
        }
        email_notification(mail_subject, message, [email], [attachment])
    except:
        return JsonResponse({"error": "Oops! Something went wrong"}, status=500)

    return JsonResponse({"message": "Enquiry report sent successfully!"})
