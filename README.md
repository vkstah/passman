# Vault

Vault is a lightweight and ultra-simple password manager built with Python for my personal use.

## Features

Vault allows you to create a centralized and locally hosted vault for all your passwords that can be accessed using a master password. In addition to the master password, a secret key (sometimes called device secret) is also required, to add an additional layer of security.

- Add, edit or remove credentials (username, password)
- Copy credentials to clipboard without ever displaying them on the terminal
- Automatic script timeout after X amount of seconds for additional security
- Stores AES encrypted credentials into a [PostgreSQL](https://www.postgresql.org/) database

## Requirements

- Python >= 3.11.4

## Installation

Begin by cloning or downloading this repository to your device.

```bash
git clone git@github.com:vkstah/vault.git
```

Install all of the required dependencies using `pip`.

```bash
pip install -r requirements.txt
```

Finally, define the required environment variables.

```bash
DB_HOST="host"
DB_NAME="name"
DB_USER="user"
DB_PASSWORD="password"
DB_PORT="5432"
SECRET_KEY="vr+6,+~aIGc/X9-SIJayGbP+;F+m?E7FMhSW%Tx}C3{Lq:!V4}?-%mA-WBooT(0/"
```

## Usage

Under construction. 🔧

## Furthermore

This password manager is based on Computerphile's detailed explanation of Password Managers in their video [How Password Managers Work](https://www.youtube.com/watch?v=w68BBPDAWr8).

## Troubleshooting

Make sure you have installed a version of Python that is compatible with this project as specified in [Requirements](#requirements). Additionally, make sure you have the latest version of this project, and that you have installed the required dependencies as specified in [Installation](#installation).
