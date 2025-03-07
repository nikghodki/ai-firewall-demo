# Firewall Management Assistant

## Overview

The Firewall Management Assistant is a tool designed to help manage firewall rules for pfSense firewalls. It provides functionalities to add, delete, and edit firewall rules through a conversational interface.

## Features

- **Add Firewall Rule**: Create new firewall rules based on user input.
- **Edit Firewall Rule**: Modify existing firewall rules.
- **Delete Firewall Rule**: Remove firewall rules based on user input.
- **Get Firewall Rules**: Retrieve and display current firewall rules.

## Prerequisites

- Python
- pip
- RabbitMQ
- OpenAI API Key

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-folder>
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up RabbitMQ:
    - Ensure RabbitMQ is installed and running on your machine.
    - Create a queue named `firewall_rules`.

4. Set the OpenAI API Key:
    ```sh
    export OPENAI_API_KEY=<your-openai-api-key>
    ```

## Running the Application

1. Start the RabbitMQ consumer:
    ```sh
    python rabbitmq/receivemq.py
    ```

2. Run the main application:
    ```sh
    python botservice/main.py
    ```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key.

## Configuration

- **config_file_path**: Path to the JSON configuration file for creating firewall rules.
- **rules_file_path**: Path to the JSON file containing the current firewall rules.
- **new_rule_config_file**: Path to the JSON file for new firewall rule configuration.

## Usage

1. Open the Gradio interface.
2. Interact with the assistant by typing commands such as:
    - "Get Firewall Rules."
    - "Show Firewall Rules."
    - "Create a firewall rule to allow access to IP 192.168.1.10 from 10.64.10.1 with source port as 8081 and destination port as 8081, on WAN interface, protocol TCP, Description: Allow access to Arjun for pfSense."
    - "Delete rule with description test."

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License.
