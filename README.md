# Vault

Vault is a lightweight and ultra-simple password manager built with Python for my personal use.

## Features

Vault allows you to create a centralized and locally hosted vault for all your passwords that can be accessed using a master password. In addition to the master password, a secret key (sometimes called device secret) is also required in order to add an additional layer of security to the mix.

- Add, edit or remove credentials (username, password)
- Copy credentials to clipboard without ever displaying them on the terminal
- Automatic script timeout after 90 seconds for additional security. The timeout can be modified as specified in [Arguments](#arguments)
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

Finally, define the required environment variables. For `SECRET_KEY`, use a 30 character long sequence of random characters (uppercase, lowercase and numbers). You can use [RANDOM.org](https://www.random.org/strings/?num=5&len=30&digits=on&upperalpha=on&loweralpha=on&unique=on&format=html&rnd=new) to generate such a sequence.

```bash
DB_HOST="host"
DB_NAME="name"
DB_USER="user"
DB_PASSWORD="password"
DB_PORT="5432"
SECRET_KEY="hUmbfgDF6WLD3OVLfcNv2bTLVYQIaq" # You can remove this after you've set your master password.
```

## Usage

Under construction. 🔧

## Arguments

### Timeout

You can use the `--timeout` flag to specify the amount of idle seconds you want the program to timeout in.

```bash
python main.py --timeout 30
```

## Furthermore

This password manager is based on Computerphile's detailed explanation of Password Managers in their video [How Password Managers Work](https://www.youtube.com/watch?v=w68BBPDAWr8).

## Troubleshooting

Make sure you have installed a version of Python that is compatible with this project as specified in [Requirements](#requirements). Additionally, make sure you have the latest version of this project, and that you have installed the required dependencies as specified in [Installation](#installation).
