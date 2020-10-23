# intelbras-bee

intelbras-bee is a Python project for obtaining and updating ipv4 settings on Intelbras Access Points using [Intelbras Zeus API](https://izeus.docs.apiary.io/)

## Requirements

The requirements for running this library are available at requirements.txt file:

certifi==2020.6.20
chardet==3.0.4
idna==2.10
requests==2.24.0
urllib3==1.25.11

## Usage

```python
import intelbras-bee

intelbras-bee.auth('username', 'password') # returns auth Token
intelbras-bee.update_ipv4(ipv4_settings) # returns True if succeeded
intelbras-bee.get_ipv4() # returns ipv4_settings
intelbras-bee.apply_changes # returns True if successfully applied changes
intelbras-bee.has_changes() # returns boolean indicating if there are saved changes that were not applied

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
GNU General Public License
