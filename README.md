## Atlys Scraper

Atlys Scraper is a web scraping tool designed to gather information from the website efficiently. This project leverages Docker for easy deployment and management.

## Features

\- Efficiently scrapes data from Custom URL

\- Configurable settings for different scraping needs

\- Docker support for easy setup and deployment

## Requirements

\- Docker

\- Docker Compose

## Installation

1\. Clone the repository:

```bash

git clone https://github.com/samariaVipin98/atlys-scraper.git

cd atlys-scraper
```

2\. Build and run the application using Docker Compose:

```bash
docker-compose up --build
```
    

## Usage

Once the application is running, it will start scraping data according to the configuration specified in the code. You can customize the scraping parameters in the /scrape api payload (like pages count and proxy).

## Docker Compose

The docker-compose.yml file is included in the repository to facilitate easy deployment. Here’s a brief overview of the docker-compose.yml configuration:

```bash
version: '3.8'

services:
  scraper:
    build: .
    volumes:
      - .:/app
    environment:
      - WEBSITE_ENDPOINT=www.abc.com # Website endpoint for which scraping is to be done

```

### Configuration Options

*   **WEBSITE_ENDPOINT**: Adjust this environment variable to set the website endpoint.
    

## Contributing
------------

Contributions are welcome! Please fork the repository and submit a pull request.

## License
-------

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
-------

For any questions or suggestions, please open an issue in the repository.

```bash

Feel free to copy this directly into your `README.md` file! Let me know if you need any other changes.
```
