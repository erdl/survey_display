# Survey Display [![Stories in Ready](https://badge.waffle.io/erdl/survey_display.png?label=ready&title=Ready)](http://waffle.io/erdl/survey_display)

Survey Display is a minimal flask and elm application hooked to a Postgres database to conduct surveys. Contrary to most survey apps, it can store responses in memory locally in the browser as responses are submitted, until the connection is recovered and all responses are submitted together to the remote server.

## Installation

Clone the Github repository and follow the instructions on the [wiki](https://github.com/erdl/survey_display/wiki/Running-in-Localhost).

```
git clone https://github.com/erdl/survey_display.git
```

## Usage

Create questions and responses on the database, and survey_display will serve them as different URLs. For a GUI interface to adding questions, and surveys, see [survey_admin](https://github.com/erdl/survey_admin) project.

## Documentation

Please see the [wiki](https://github.com/erdl/survey_display/wiki) for the project documentation.

## Known Issues

Please see [Issues](https://github.com/erdl/survey_display) for known bugs and new feature requests.

## Contributing

A CONTRIBUTING.md will be updated soon. Currently, the project is maintained by ERDL. Feel free to open an issue if you are interested in contributing.

## License

Please feel free to use this project code. Code dependencies are still being assessed to decide on a license.
