@api_view(['POST'])
def shop_update_product(request, id, product_id):
    print(request.data)
    shop_products = dict(request.POST)
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_products/{id}/primary_image/" + primary_image,
                                     request.FILES['primary_image'])
        primary_image_paths = all_image_url + fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['primary_image'] = primary_image_paths
    except:
        pass

    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_products/{id}/other_images/" + sav.name, sav)
            other_image.append(str(ot).replace(" ", "_"))

            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url + fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist

    except:
        pass

    try:
        shop_product_instance = models.shop_productsmodel.objects.get(shop_id=id, product_id=product_id)
        existing_product_data = shop_product_instance.product

        # Updating product field with new data
        new_product_data = dict(request.POST)
        shop_products = dict(request.POST)
        cleaned_data_dict = {key: value[0] if isinstance(value, list) and len(value) == 1 else value for key, value in
                             shop_products.items()}

        existing_product_data.update(cleaned_data_dict)

        # Saving changes to the SQLite table
        with transaction.atomic():
            
            # Updating only the product field
            shop_product_instance.product = existing_product_data
            shop_product_instance.save()

        return Response(id, status=status.HTTP_200_OK)
    except models.shop_productsmodel.DoesNotExist:
        return Response({"error": "Shop product not found"}, status=status.HTTP_404_NOT_FOUND)



