---
title: NLMaps Annotation Guidelines
geometry:
- a4paper
- top=30mm
- left=35mm
- right=35mm
- bottom=30mm
mainfont: TeX Gyre Adventor
monofont: TeX Gyre Cursor
monofontoptions:
- Color=028900
urlcolor: blue
---
\pagenumbering{gobble}
# Principles

In essence, we need a dataset that fulfills three criteria:

1. The natural language (NL) queries should be linguistically diverse, i.e. a
   mix of short search-engine-style queries and full questions like you would
   ask another person.

2. The queries should cover a large part of the commonly used OpenStreetmap
   (OSM) tags that are relevant for our system.

3. The queries should cover the most useful OSM tags in particular depth. E.g.,
   asking for restaurants and shops is arguably one of the most useful areas.

# Linguistic Diversity

When entering queries, please diversify your language use. Valid variations of
the same question include:

* _closest swimming pool near Eiffel Tower in Paris_
* _In Paris, give me the swimming pool that is closest to the Eiffel Tower!_
* _Closest place where I can take a swim near Eiffel Tower in Paris_

However, keep it natural and don’t make your queries artificially complex. If a
particular query style comes more natural to you, it’s alright to use it more
often. Just make sure that not all of you queries look alike.

Similarly, avoid using the same place name more than a couple of times. Also use
place names in other languages than German and English, e.g. _České Budějovice_
or _València_.

It’s **very important** that you don’t only base your wording on the name of the
OSM tags. E.g., for `highway=speed_camera` you can ask for a _speed camera_, but
you can also ask for a _speed trap_ or a _radar trap_.

# Tag Diversity and Depth

Take a _quick_ look at the [most important OSM
features](https://wiki.openstreetmap.org/wiki/Map_features) to get a feel for
what things you can ask for in OSM. You can use this as an inspiration if you
run out of ideas about what to ask. Choose tags that you find relevant.

**Beware of the `building=*` tag!** It is used to tag what the building was
built as, not to tag its current use. E.g., a place tagged `building=church` may
not be a church anymore; churches are tagged as
`amenity=place_of_worship + religion=christian`. If in doubt, don’t use the
`building=*` tag, at all.

In general, enter more than one query for a chosen tag or tag combination,
especially if the system fails answering the query correctly.

## Most relevant keys

Please enter at least the given amount of queries for each of the following. The
linked wiki pages give you a feel for what the most common tags in each category
are.

* [shop=*](https://wiki.openstreetmap.org/wiki/Key:shop): 30
* [leisure=*](https://wiki.openstreetmap.org/wiki/Key:leisure): 30
* [sport=*](https://wiki.openstreetmap.org/wiki/Key:sport): 20
* [craft=*](https://wiki.openstreetmap.org/wiki/Key:craft): 20
* [man_made=*](https://wiki.openstreetmap.org/wiki/Key:man_made): 20
* [amenity=restaurant](https://wiki.openstreetmap.org/wiki/Tag:amenity=restaurant), [amenity=fast_food](https://wiki.openstreetmap.org/wiki/Tag:amenity=fast_food): 30
* [cuisine=*](https://wiki.openstreetmap.org/wiki/Key:cuisine): 30.
* [diet:\*=\*](https://wiki.openstreetmap.org/wiki/Key:diet): 20.
* [wheelchair=yes](https://wiki.openstreetmap.org/wiki/Key:wheelchair): 50.
  Just sprinkle phrases like _wheelchair-accessible [place]_ or _[places] that
  are wheelchair-accessible_ into your queries now and then.
