# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import loader, RequestContext, Context
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from apps.utils.context_processors import custom_proc
from django.conf import settings

def index(request):

    sale_products = Product.items.exclude(old_price__isnull=True)
    sale_products_count = sale_products.count()

    sections_id = sale_products.values_list('subcategory__category__section', flat=True)

    sale_sections = Section.items.filter(id__in=sections_id)

    sale_products = sale_products.order_by('?')[:12]

    return render_to_response(
        'index.html',
        {
            'sale_products':sale_products,
            'sale_products_count':sale_products_count,
            'sale_sections':sale_sections
        },
        context_instance=RequestContext(request, processors=[custom_proc])
    )


from xml.etree import ElementTree as ET
from apps.products.models import Property, Product, Section, Category, SubCategory, Param,Storage
from decimal import Decimal, InvalidOperation

def import_xml(request):
    try:
        #doc = ET.parse(u'%s/catalog.xml'%settings.ROOT_PATH)
        doc = ET.parse(u'/home/antonio/!!!PyCharm2!!!/klev/catalog.xml')
    except IOError:
        return HttpResponse(u'nofile')

    root = doc.getroot()
    calalog = root.find(u'Каталог')
    if len(calalog):
        properties = calalog.findall(u'Свойство')

        for pr in properties:
            try:
                prop_ID = unicode(pr.attrib[u'Идентификатор']).strip()
            except KeyError:
                #prop_ID = False
                continue

            prop_name = unicode(pr.attrib[u'Наименование']).strip()

            if prop_ID:
                try:
                    prop = Property.objects.get(xml_id=prop_ID)
                except Property.DoesNotExist:
                    Property.objects.create(
                        xml_id=prop_ID,
                        name=prop_name
                    )

        products = calalog.findall(u'Товар')

        for prod in products:
            try:
                prod_ID = unicode(prod.attrib[u'Идентификатор']).strip()
            except KeyError:
                #prop_ID = False
                continue
            values_prop = prod.findall(u'ЗначениеСвойства')

            section_value = False
            category_value = False
            subcategory_value = False
            product_name = False

            prop_list = []
            for value_prop in values_prop:
                prop_ID = unicode(value_prop.attrib[u'ИдентификаторСвойства']).strip()
                value = unicode(value_prop.attrib[u'Значение']).strip()
                if prop_ID == u'00003': #Вид товара (Категория)
                    category_value = value
                elif prop_ID == u'Ц0070': #Класс товара (Раздел)
                    section_value = value
                elif prop_ID == u'Ц0077': #Подвид товара (Подкатегория)
                    subcategory_value = value
                elif prop_ID == u'ПолноеНаименование': #Подвид товара (Подкатегория)
                    product_name = value
                else:
                    prop_list.append([prop_ID, value])

            if not section_value or not category_value or not subcategory_value or not product_name:
                continue

            try:
                product = Product.objects.get(xml_id=prod_ID)
            except Product.DoesNotExist:
                try:
                    section = Section.objects.select_related().get(xml_name=section_value)
                except Section.DoesNotExist:
                    section = Section.objects.select_related().create(
                        name=section_value,
                        alias=section_value.replace(u' ', '_'),
                        xml_name=section_value
                    )
                try:
                    category = Category.objects.select_related().get(xml_name=category_value)
                except Category.DoesNotExist:
                    category = Category.objects.select_related().create(
                        section=section,
                        name=category_value,
                        alias=category_value.replace(u' ', '_'),
                        xml_name=category_value
                    )

                try:
                    subcategory = SubCategory.objects.select_related().get(xml_name=subcategory_value)
                except SubCategory.DoesNotExist:
                    subcategory = SubCategory.objects.select_related().create(
                        category=category,
                        name=subcategory_value,
                        alias=subcategory_value.replace(u' ', '_'),
                        xml_name=subcategory_value
                    )
                keywords = u'%s %s' % (product_name, subcategory.name)
                product = Product.objects.create(
                    subcategory=subcategory,
                    name=product_name,
                    xml_id=prod_ID,
                    keywords=keywords
                )

                if prop_list:
                    for p in prop_list:
                        try:
                            property = Property.objects.get(xml_id=p[0])
                        except Property.DoesNotExist:
                            continue

                        Param.objects.create(
                            product=product,
                            property=property,
                            value=p[1]
                        )

    package = root.find(u'ПакетПредложений')
    if package:
        proposals = package.findall(u'Предложение')

        for proposal in proposals:
            try:
                product_xml_id = unicode(proposal.attrib[u'ИдентификаторТовара']).strip()
                product_count = unicode(proposal.attrib[u'Количество']).strip()
                product_price = unicode(proposal.attrib[u'Цена']).strip()
            except KeyError:
                continue

            try:
                product_old_price = unicode(proposal.attrib[u'СтараяЦена']).strip()
            except KeyError:
                product_old_price = None

            try:
                product = Product.objects.get(xml_id=product_xml_id)
            except Product.DoesNotExist:
                continue


            presence = proposal.find(u'Наличие')

            storage_xml = unicode(presence.attrib[u'Склад']).strip()

            try:
                storage = Storage.objects.get(name=storage_xml)
            except Storage.DoesNotExist:
                storage = Storage.objects.create(name=storage_xml)


            product_price = Decimal(product_price).quantize(Decimal(10) ** -2)
            product.price = product_price
            if product_old_price:
                product_old_price = Decimal(product_old_price).quantize(Decimal(10) ** -2)
                product.old_price = product_old_price
            else:
                product.old_price = product_old_price

            product.storage = storage
            product.count = product_count
            product.save()


        return HttpResponse('good')
    else:
        return HttpResponse('bad')