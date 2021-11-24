# metabase-python
[![main](https://github.com/chasleslr/metabase-python/actions/workflows/main.yml/badge.svg)](https://github.com/chasleslr/metabase-python/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/chasleslr/metabase-python/branch/main/graph/badge.svg?token=15G7HOQ1CM)](https://codecov.io/gh/chasleslr/metabase-python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An unofficial Python library for the [Metabase API](https://www.metabase.com/learn/administration/metabase-api).


## Installation

```
pip install metabase-python
```

## Usage
This API is still experimental and may change significantly between minor versions.


Start by creating an instance of Metabase with your credentials. This connection will automatically be used by any
object that interacts with the Metabase API.
```python
from metabase import Metabase

metabase = Metabase(
    host="<host>",
    user="<username/email>",
    password="<password>",
)
```

You can then interact with any of the supported endpoints through the classes included in this package. All changes
are reflected in Metabase instantly.

```python
from metabase import User

# get all objects
users = User.list()

# get an object by ID
user = User.get(1)

# attributes are automatically loaded and available in the instance
if user.is_active:
    print("User is active!")

# update any available attribute
user.update(is_superuser=True)

# delete an object
user.delete()

# create an object
new_user = User.create(
    first_name="<first_name>",
    last_name="<last_name>",
    email="<email>",
    password="<password>"
)
```

The methods `.list()`, `.get()`, `.create()`, `.update()`, `.delete()` are available on all
endpoints that support them in Metabase API.

Some endpoints also support additional methods:

```python
from metabase import User

user = User.get(1)

user.reactivate()   # Reactivate user
user.send_invite()  # Resend the user invite email for a given user.
```

Here's a slightly more advanced example:
```python
from metabase import User, PermissionGroup, PermissionMembership

# create a new PermissionGroup
my_group = PermissionGroup.create(name="My Group")

for user in User.list():
    # add all users to my_group
    PermissionMembership.create(
        group_id=my_group.id,
        user_id=user.id
    )
```

You can also execute queries and get results back as a Pandas DataFrame. Currently, you need to provide
the exact MBQL (i.e. Metabase Query Language) as the `query` argument.
```python
from metabase import Dataset

dataset = Dataset.create(
    database=1,
    type="query",
    query={
        "source-table": 1,
        "aggregation": [["count"]],
        "breakout": ["field", 7, {"temporal-unit": "year"},],
    },
)

df = dataset.to_pandas()
```


## Endpoints

For a full list of endpoints and methods, see [Metabase API](https://www.metabase.com/docs/latest/api-documentation.html).

| Endpoints             | Support    |
|-----------------------|:----------:|
| Activity              |  ❌        |
| Alert                 |  ❌        |
| Automagic dashboards  |  ❌        |
| Card                  |  ❌        |
| Collection            |  ❌        |
| Card                  |  ❌        |
| Dashboard             |  ❌        |
| Database              |  ❌        |
| Dataset               |  ✅        |
| Email                 |  ❌        |
| Embed                 |  ❌        |
| Field                 |  ✅        |
| Geojson               |  ❌        |
| Ldap                  |  ❌        |
| Login history         |  ❌        |
| Metric                |  ✅        |
| Native query snippet  |  ❌        |
| Notify                |  ❌        |
| Permissions           |  ❌        |
| Premium features      |  ❌        |
| Preview embed         |  ❌        |
| Public                |  ❌        |
| Pulse                 |  ❌        |
| Revision              |  ❌        |
| Search                |  ❌        |
| Segment               |  ✅        |
| Session               |  ❌        |
| Setting               |  ❌        |
| Setup                 |  ❌        |
| Slack                 |  ❌        |
| Table                 |  ✅        |
| Task                  |  ❌        |
| Tiles                 |  ❌        |
| Transform             |  ❌        |
| User                  |  ✅        |
| Util                  |  ❌        |

## Contributing
Contributions are welcome!

## License
This library is distributed under the MIT license.
