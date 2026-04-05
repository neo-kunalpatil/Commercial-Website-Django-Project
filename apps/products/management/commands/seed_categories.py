from django.core.management.base import BaseCommand
from apps.products.models import Category


CATEGORIES = [
    "Electronics",
    "Mobile Phones & Accessories",
    "Computers & Laptops",
    "Cameras & Photography",
    "Home & Kitchen",
    "Furniture",
    "Appliances",
    "Clothing & Fashion",
    "Men's Clothing",
    "Women's Clothing",
    "Kids' Fashion",
    "Shoes & Footwear",
    "Books",
    "Sports & Fitness",
    "Toys & Games",
    "Beauty & Personal Care",
    "Health & Wellness",
    "Grocery & Gourmet Foods",
    "Automotive",
    "Tools & Hardware",
    "Garden & Outdoors",
    "Pet Supplies",
    "Office Supplies",
    "Musical Instruments",
    "Watches & Jewellery",
    "Bags & Luggage",
    "Art & Craft Supplies",
    "Baby Products",
    "Industrial & Scientific",
]


class Command(BaseCommand):
    help = 'Seed the database with default product categories'

    def handle(self, *args, **options):
        created_count = 0
        for name in CATEGORIES:
            obj, created = Category.objects.get_or_create(name=name)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  Created: {name}'))
            else:
                self.stdout.write(f'  Already exists: {name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! {created_count} new categories added, {len(CATEGORIES) - created_count} already existed.'
        ))
