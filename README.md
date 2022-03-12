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

### Connection

Start by creating an instance of Metabase with your credentials.
```python
from metabase import Metabase

metabase = Metabase(
    host="<host>",
    user="<username/email>",
    password="<password>",
)
```

### Interacting with Endpoints
You can then interact with any of the supported endpoints through the classes included in this package. Methods that
instantiate an object from the Metabase API require the `using` parameter which expects an instance of `Metabase` such
as the one we just instantiated above. All changes are reflected in Metabase instantly.

```python
from metabase import User

# get all objects
users = User.list(using=metabase)

# get an object by ID
user = User.get(1, using=metabase)

# attributes are automatically loaded and available in the instance
if user.is_active:
    print("User is active!")

# update any available attribute
user.update(is_superuser=True)

# delete an object
user.delete()

# create an object
new_user = User.create(
    using=metabase,
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

user = User.get(1, using=metabase)

user.reactivate()   # Reactivate user
user.send_invite()  # Resend the user invite email for a given user.
```

Here's a slightly more advanced example:
```python
from metabase import User, PermissionGroup, PermissionMembership

# create a new PermissionGroup
my_group = PermissionGroup.create(name="My Group", using=metabase)

for user in User.list():
    # add all users to my_group
    PermissionMembership.create(
        group_id=my_group.id,
        user_id=user.id,
        using=metabase,
    )
```

### Querying & MBQL

You can also execute queries and get results back as a Pandas DataFrame. You can provide the exact MBQL, or use
the `Query` object to compile MBQL (i.e. Metabase Query Language) from Python classes included in this package.

```python
from metabase import Dataset, Query, Count, GroupBy, TemporalOption

dataset = Dataset.create(
    database=1,
    type="query",
    query={
        "source-table": 1,
        "aggregation": [["count"]],
        "breakout": ["field", 7, {"temporal-unit": "year"},],
    },
    using=metabase,
)

# compile the MBQL above using the Query object
dataset = Dataset.create(
    database=1,
    type="query",
    query=Query(
        table_id=2,
        aggregations=[Count()],
        group_by=[GroupBy(id=7, option=TemporalOption.YEAR)]
    ).compile(),
    using=metabase
)

df = dataset.to_pandas()
```

As shown above, the `Query` object allows you to easily compile MBQL from Python objects. Here is a
more complete example:
```python
from metabase import Query, Sum, Average, Metric, Greater, GroupBy, BinOption, TemporalOption

query = Query(
    table_id=5,
    aggregations=[
        Sum(id=5),                                  # Provide the ID for the Metabase field
        Average(id=5, name="Average of Price"),     # Optionally, you can provide a name
        Metric.get(5)                               # You can also provide your Metabase Metrics
    ],
    filters=[
        Greater(id=1, value=5.5)                    # Filter for values of FieldID 1 greater than 5.5
    ],
    group_by=[
        GroupBy(id=4),                              # Group by FieldID 4
        GroupBy(id=5, option=BinOption.AUTO),       # You can use Metabase's binning feature for numeric fields
        GroupBy(id=5, option=TemporalOption.YEAR)   # Or it's temporal option for date fields
    ]
)

print(query.compile())
{
    'source-table': 5,
    'aggregation': [
        ['sum', ['field', 5, None]],
        ['aggregation-options', ['avg', ['field', 5, None]], {'name': 'Average of Price', 'display-name': 'Average of Price'}],
        ["metric", 5]
    ],
    'breakout': [
        ['field', 4, None],
        ['field', 5, {'binning': {'strategy': 'default'}}],
        ['field', 5, {'temporal-unit': 'year'}]
    ],
    'filter': ['>', ['field', 1, None], 5.5]
}
```

This can also be used to more easily create `Metric` objects.

```python
from metabase import Metric, Query, Count, EndsWith, CaseOption


metric = Metric.create(
    name="Gmail Users",
    description="Number of users with a @gmail.com email address.",
    table_id=2,
    definition=Query(
        table_id=1,
        aggregations=[Count()],
        filters=[EndsWith(id=4, value="@gmail.com", option=CaseOption.CASE_INSENSITIVE)]
    ).compile(),
    using=metabase
)
```



## Endpoints

For a full list of endpoints and methods, see [Metabase API](https://www.metabase.com/docs/latest/api-documentation.html).

| Endpoints             | Support    | Notes |
|-----------------------|:----------:|-------|
| Activity              |  ❌        |       |
| Alert                 |  ❌        |       |
| Automagic dashboards  |  ❌        |       |
| Card                  |  ✅        |       |
| Collection            |  ❌        |       |
| Dashboard             |  ❌        |       |
| Database              |  ✅        |       |
| Dataset               |  ✅        |       |
| Email                 |  ❌        |       |
| Embed                 |  ❌        |       |
| Field                 |  ✅        |       |
| Geojson               |  ❌        |       |
| Ldap                  |  ❌        |       |
| Login history         |  ❌        |       |
| Metric                |  ✅        |       |
| Native query snippet  |  ❌        |       |
| Notify                |  ❌        |       |
| Permissions           |  ✅        |       |
| Premium features      |  ❌        |       |
| Preview embed         |  ❌        |       |
| Public                |  ❌        |       |
| Pulse                 |  ❌        |       |
| Revision              |  ❌        |       |
| Search                |  ❌        |       |
| Segment               |  ✅        |       |
| Session               |  ❌        |       |
| Setting               |  ❌        |       |
| Setup                 |  ❌        |       |
| Slack                 |  ❌        |       |
| Table                 |  ✅        |       |
| Task                  |  ❌        |       |
| Tiles                 |  ❌        |       |
| Transform             |  ❌        |       |
| User                  |  ✅        |       |
| Util                  |  ❌        |       |

## Contributing
Contributions are welcome!

## License
This library is distributed under the MIT license.
