from . import views, cms
from django.urls import path
from django.views.generic import RedirectView

cms_patterns = [
    path("cms/attributes", cms.attributes, name="cms_attributes"),
    path("cms/attribute/add", cms.add_attribute, name="cms_add_attribute"),
    path("cms/attribute/save", cms.save_attribute, name="cms_save_attribute"),
    path("cms/attribute/<int:id>/edit", cms.edit_attribute, name="cms_edit_attribute"),
    path(
        "cms/attribute/<int:id>/update",
        cms.update_attribute,
        name="cms_update_attribute",
    ),
    path(
        "cms/attribute/<int:id>/delete",
        cms.delete_attribute,
        name="cms_delete_attribute",
    ),
    path("cms/products/", cms.products, name="cms_products"),
    path("cms/product/add", cms.add_product, name="cms_add_product"),
    path("cms/product/save", cms.save_product, name="cms_save_product"),
    path("cms/product/<int:id>/edit", cms.edit_product, name="cms_edit_product"),
    path("cms/product/<int:id>/update", cms.update_product, name="cms_update_product"),
    path("cms/product/<int:id>/delete", cms.delete_product, name="cms_delete_product"),
    path(
        "cms/products/email/enquiry-report",
        cms.email_product_enquiry_report,
        name="cms_products_email_enquiry_report",
    ),
    path("cms/product_images/<int:pid>", cms.product_images, name="cms_product_images"),
    path(
        "cms/product_image/<int:pid>/add",
        cms.add_product_image,
        name="cms_add_product_image",
    ),
    path(
        "cms/product_image/<int:pid>/<int:id>/edit",
        cms.edit_product_image,
        name="cms_edit_product_image",
    ),
    path(
        "cms/product_image/<int:pid>/<int:id>/delete",
        cms.delete_product_image,
        name="cms_delete_product_image",
    ),
    path(
        "cms/product_image/<int:pid>/<int:id>/activate",
        cms.product_image_default,
        name="cms_product_image_default",
    ),
]


api_patterns = [
    path("api/attributes", views.get_attributes, name="api_attributes"),
    path("api/products", views.get_products, name="api_products"),
    path(
        "api/category_products/<int:cid>",
        views.get_category_products,
        name="api_category_products",
    ),
    path(
        "api/subcategory_products/<int:scid>",
        views.get_subcategory_products,
        name="api_subcategory_products",
    ),
    path(
        "api/brand_products/<int:bid>",
        views.get_brand_products,
        name="api_brand_products",
    ),
    path("api/products/search", views.api_search_products, name="api_search_products"),
    path("api/products/enquiry", views.api_product_enquiry, name="api_product_enquiry"),
]


redirect_urlpatterns = [
    path("shop", RedirectView.as_view(pattern_name="products", permanent=True)),

    path("brands/first-copy/<str:bslug>", RedirectView.as_view(pattern_name="main_brand_products", permanent=True)),
    path("brands/first-copy/<str:bslug>/page/<int:page>", RedirectView.as_view(pattern_name="paged_main_brand_products", permanent=True)),
    path("brands/first-copy/<str:bslug>/sort", RedirectView.as_view(pattern_name="sort_main_brand_products", permanent=True)),   
    path("brands/first-copy/<str:bslug>/sort/page/<int:page>", RedirectView.as_view(pattern_name="paged_sort_main_brand_products", permanent=True)),

    path("shop/<str:mcslug>", RedirectView.as_view(pattern_name="maincategory_products", permanent=True)),
    path("shop/<str:mcslug>/page/<int:page>", RedirectView.as_view(pattern_name="paged_maincategory_products", permanent=True)),
    path("shop/<str:mcslug>/sort", RedirectView.as_view(pattern_name="sort_maincategory_products", permanent=True)),
    path("shop/<str:mcslug>/sort/page/<int:page>", RedirectView.as_view(pattern_name="paged_sort_maincategory_products", permanent=True)),
]

web_patterns = [
        path("store", views.products, name="products"),
        path("store/page/<int:page>", views.paged_products, name="paged_products"),
        path("products/sort", views.sort_products, name="sort_products"),
        path(
            "products/sort/page/<int:page>",
            views.paged_sort_products,
            name="paged_sort_products",
        ),
        path("products/search", views.search_products, name="search_products"),
        path(
            "products/search/page/<int:page>",
            views.paged_search_products,
            name="paged_search_products",
        ),
        path("product/<str:slug>", views.product_details, name="product_details"),

        # Brands
        path(
            "brands/<str:bslug>",
            views.main_brand_products,
            name="main_brand_products",
        ),
        path(
            "brands/<str:bslug>/page/<int:page>",
            views.paged_main_brand_products,
            name="paged_main_brand_products",
        ),
        path(
            "brands/<str:bslug>/sort",
            views.sort_main_brand_products,
            name="sort_main_brand_products",
        ),
        path(
            "brands/<str:bslug>/sort/page/<int:page>",
            views.paged_sort_main_brand_products,
            name="paged_sort_main_brand_products",
        ),

        # Main Categories
        path(
            "<str:mcslug>",
            views.maincategory_products,
            name="maincategory_products",
        ),
        path(
            "<str:mcslug>/page/<int:page>",
            views.paged_maincategory_products,
            name="paged_maincategory_products",
        ),
        path(
            "<str:mcslug>/sort",
            views.sort_maincategory_products,
            name="sort_maincategory_products",
        ),
        path(
            "<str:mcslug>/sort/page/<int:page>",
            views.paged_sort_maincategory_products,
            name="paged_sort_maincategory_products",
        ),
       
        # Category
        path("<str:mcslug>/<str:cslug>", views.category_products, name="category_products"),
        path(
            "<str:mcslug>/<str:cslug>/page/<int:page>",
            views.paged_category_products,
            name="paged_category_products",
        ),
        path(
            "<str:mcslug>/<str:cslug>/sort",
            views.sort_category_products,
            name="sort_category_products",
        ),
        path(
            "<str:mcslug>/<str:cslug>/sort/page/<int:page>",
            views.paged_sort_category_products,
            name="paged_sort_category_products",
        ),

        # Category brands
        # path(
        #     "<str:cslug>/first-copy/<str:bslug>",
        #     views.brand_products,
        #     name="brand_products",
        # ),
        # path(
        #     "<str:cslug>/first-copy/<str:bslug>/page/<int:page>",
        #     views.paged_brand_products,
        #     name="paged_brand_products",
        # ),
        # path(
        #     "<str:cslug>/first-copy/<str:bslug>/sort",
        #     views.sort_brand_products,
        #     name="sort_brand_products",
        # ),
        # path(
        #     "<str:cslug>/first-copy/<str:bslug>/sort/page/<int:page>",
        #     views.paged_sort_brand_products,
        #     name="paged_sort_brand_products",
        # ),

        # Sub categories
        path(
            "<str:mcslug>/<str:cslug>/<str:scslug>",
            views.subcategory_products,
            name="subcategory_products",
        ),
        path(
            "<str:mcslug>/<str:cslug>/<str:scslug>/page/<int:page>",
            views.paged_subcategory_products,
            name="paged_subcategory_products",
        ),
        path(
            "<str:mcslug>/<str:cslug>/<str:scslug>/sort",
            views.sort_subcategory_products,
            name="sort_subcategory_products",
        ),
        path(
            "<str:mcslug>/<str:cslug>/<str:scslug>/sort/page/<int:page>",
            views.paged_sort_subcategory_products,
            name="paged_sort_subcategory_products",
        ),
    ]


urlpatterns = cms_patterns + api_patterns + redirect_urlpatterns + web_patterns