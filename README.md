Pearson OpenClass Python API
===

Author
---
* Sam Purtill [https://github.com/sampurtill]

Purpose
----
* Makes working with the OpenClass API dreamy
* Creates and maintains a connection with the OpenClass API
* Supports GET, POST, PUT, and DELETE requests (aka any request you would ever make to the OpenClass API)
* Allows for subclassing, i.e. if one wanted to cache the authentication tokens in memory 

Installation
---

For now, installation is manual:

> git clone git://github.com/sampurtill/openclass-python.git

Basic Example
---

```
>>> from pearson.openclass import OpenClass
>>> oc = OpenClass('sam@classowl.com', 'password', 'oc_api_key')
>>> course = oc.get_course('oc_course_key')
>>> course['name']
u'Math 51'
```

In-Depth Tutorial
---

Here we will show you how to _create, read, update, and delete_ an OpenClass course using the OpenClass Python library.

### Required Variables for Tutorial

You'll need these variables (though not necessarily the institution ID) in any calls you make to the OpenClass API

```
OPENCLASS_ADMIN_EMAIL:    email of OpenClass admin
OPENCLASS_ADMIN_PASSWORD: password of OpenClass admin
OPENCLASS_API_KEY:        API key provisioned by OpenClass for your app
OPENCLASS_INSTITUTION_ID: string of the OpenClass school you're creating a course on
```

### Onto the Code

```
# Import the OpenClass library

from pearson.openclass import OpenClass

# ========================================================
# Create a connection with OpenClass (valid throughout)
# ========================================================

oc = OpenClass(OPENCLASS_ADMIN_EMAIL, OPENCLASS_ADMIN_PASSWORD, OPENCLASS_API_KEY)

# ========================================================
# Create a course
# ========================================================

math41_data = {
	'institutionId': OPENCLASS_INSTITUTION_ID,
	'courseTitle':   'Math 41: Linear Algebra',
	'courseCode':    'MATH41',
	'description':   'Difficult equations, naturally',
	'credits':       4
}

math41_creation = oc.create_course(OPENCLASS_INSTITUTION_ID, math41_data)

# Get the ID of the course that was just created
math41_id = math41_creation['data']['id']

# ========================================================
# Read a course
# ========================================================

math41 = oc.get_course(math41_id)

# ========================================================
# Update a course
# ========================================================

math41_update = {
	'id': math41_id,
	'institutionId': OPENCLASS_INSTITUTION_ID,
	'courseTitle':   'Math 41: Calculus',
	'courseCode':    'MATH41',
	'description':   'Here we go again!',
	'credits':       5
}

oc.update_course(math41_id, updated_math41)

# Re-read the course, ensuring it was updated
math41 = oc.get_course(math41_id)

# ========================================================
# Delete a course
# ========================================================

oc.delete_course(math41_id)

# And you're done!
```
