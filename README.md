# Confession Manager Website

# Installation

## Django + Python requirements installation
### Quick installation

```bash
# Install Python (Ubuntu)
sudo apt-get install python

# Install Python dependency
sudo pip install -r requirements.txt

# Initialize database
# First of all, we have to install mysql
sudo apt-get update
sudo apt-get install mysql-server
# (in this step, we have to choose the password for root)
sudo apt-get install python-mysqldb
#Then go to Confession/settings_local.py, edit 'DATABASE_PASSWORD' in DATABASES to password of root
./init_database.sh
```
