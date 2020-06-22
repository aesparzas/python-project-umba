# Umba Backend Homework Assignment

## Getting started
To install and run the project you need to create and activate a virtual enviroment after cloning the project.
To do that, assuming you are on the project root folder, you have to type (linux example)

```
mkdir tmp
python -m venv tmp/venv
. tmp/venv/bin/activate
```

Then you need to install all the required packages. To do that

```
pip install -r requirements.txt
```

The project has already a Makefile that allows you to run it just typing
```
make server
```

Also you can run the unittests by typing
```
make test
```

## Introduction
Imagine a system where hundreds of thousands of hardware devices are concurrently uploading temperature and humidity sensor data.

The API to facilitate this system accepts creation of sensor records, in addition to retrieval.

These `GET` and `POST` requests can be made at `/devices/<uuid>/readings/`.

Retrieval of sensor data should return a list of sensor values such as:

```
    [{
        'date_created': <int>,
        'device_uuid': <uuid>,
        'type': <string>,
        'value': <int>
    }]
```

The API supports optionally querying by sensor type, in addition to a date range.

A client can also access metrics such as the max, median and mean over a time range.

These metric requests can be made by a `GET` request to `/devices/<uuid>/readings/<metric>/`

When requesting max or median, a single sensor reading dictionary should be returned as seen above.

When requesting the mean, the response should be:

```
    {
        'value': <mean>
    }
```

The API also supports the retrieval of the 1st and 3rd quartile over a specific date range.

This request can be made via a `GET` to `/devices/<uuid>/readings/quartiles/` and should return

```
    {
        'quartile_1': <int>,
        'quartile_3': <int>
    }
```

Finally, the API supports a summary endpoint for all devices and readings. When making a `GET` request to this endpoint, we should receive a list of summaries as defined below, where each summary is sorted in descending order by number of readings per device.
The url to access this endpoint is `/devices/<uuid>/summary`

```
    [
        {
            'device_uuid':<uuid>,
            'number_of_readings': <int>,
            'max_reading_value': <int>,
            'median_reading_value': <int>,
            'mean_reading_value': <int>,
            'quartile_1_value': <int>,
            'quartile_3_value': <int>
        },

        ... additional device summaries
    ]
```

NOTE: all of this endpoints accept filtering by `type`, `date_from` and `date_to`

The API is backed by a SQLite database.

## Design Desitions

Since the querying is supported by all `GET` views, metrics and no metrics ones, all the querying was grouped in a father class, an the rest of the endpoints just extend that one.

For data serialization and validation was used marshmallow since it handles very well validation and parsing of inputs

## Future work recommendations

Getting rid of SQLite. Though it has DATE field type, on the inside they are treated as strings and the validation is very poor. That goes to data inconsistency.
I recommend using postgres and SQLAlchemy as an ORM.

## Tasks
Your task is to fork this repo and complete the following:

- [x] Add field validation. Only *temperature* and *humidity* sensors are allowed with values between *0* and *100*.
- [x] Add logic for query parameters for *type* and *start/end* dates.
- [x] Implementation
  - [x] The max, median and mean endpoints.
  - [x] The quartiles endpoint with start/end parameters
  - [x] Add the path for the summary endpoint
  - [x] Complete the logic for the summary endpoint
- [x] Tests
  - [x] Wrap up the stubbed out unit tests with your changes
  - [x] Add tests for the new summary endpoint
  - [x] Add unit tests for any missing error cases
- [x] README
  - [x] Explain any design decisions you made and why.
  - [x] Imagine you're building the roadmap for this project over the next quarter. What features or updates would you suggest that we prioritize?

When you're finished, send your git repo link to engineering@umba.com. If you have any questions, please do not hesitate to reach out!
