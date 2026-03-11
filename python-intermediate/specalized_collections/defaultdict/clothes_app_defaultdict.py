"""
TLDR:
Uses a defaultdict to ensure every product in `updated_products`
has a category in `site_locations`.

How it works:
1. `validated_locations` starts with all known product → category mappings.
2. If a product is missing, the defaultdict returns:
   "TODO: Add to website".
3. The loop checks every product in `updated_products` and adds it
   to `site_locations`.
4. Known items keep their original category; new items get the
   default placeholder category.

Result:
`site_locations` becomes a complete mapping of every product in
`updated_products`, with unknown products marked for review.
"""

from collections import defaultdict

site_locations = {
  't-shirt': 'Shirts',
  'dress shirt': 'Shirts',
  'flannel shirt': 'Shirts',
  'sweatshirt': 'Shirts',
  'jeans': 'Pants',
  'dress pants': 'Pants',
  'cropped pants': 'Pants',
  'leggings': 'Pants'
}

updated_products = ['draped blouse', 'leggings', 'undershirt', 'dress shirt', 'jeans', 'sun dress', 'flannel shirt', 'cropped pants', 'dress pants', 't-shirt', 'camisole top', 'sweatshirt']

validated_locations = defaultdict(lambda: 'TODO: Add to website')

validated_locations.update(site_locations)
for item in updated_products:
  site_locations[item] = validated_locations[item]
print(site_locations)