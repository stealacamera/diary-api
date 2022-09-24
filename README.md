# Diary API
> REST API to store and keep track of diary/journal entries, folders, tags, and posting streaks.


## API endpoints
<sub>*Uses JWT authentication.  
Methods in italic are accessible without authentication.  
Methods in bold are only accessible by admins.  
All other methods are only accessible by logged in users.*</sub>

### User endpoints 
`http://localhost:5000/account/`
| Endpoint  | HTTP methods | Description |
| --- | --- | --- |
| `register/` | *`POST`* |
| `change-password/` | `POST` | Updates password & blacklists current refresh token |
| `token-refresh/` | `POST` |
| `login/` | *`POST`* | Enter username & password to log in |
| `logout/` | `POST` | Blacklists current refresh token |
| `profile/` | `GET` | Get logged-in user's profile |
| `profiles/` | **`GET`** | Get all registered profiles |
| `profiles/<int:pk>/` | **`GET`** |

### Quotes endpoints
`http://localhost:5000/`
| Endpoint  | HTTP methods | Description |
| --- | --- | --- |
| ` ` | `GET` `POST` | Get list of diary entries |
| `<pk>/` | `GET` `PUT` `PATCH` `DELETE` |
| `pinned/` | `GET` | Get list of pinned entries (`pinned` attribute is write only) |
| `pinned/<int:pk>/` | `GET` `PUT` `PATCH` `DELETE` |
| `trash/` | `GET` | Get list of trashed entries (`deleted` attribute is write only) (entries older than 30 days are deleted) |
| `trash/<int:pk>/` | `GET` `PUT` `PATCH` `DELETE` |
| `folders/` | `GET` `POST`| Get list of folders (folder names are unique per user) |
| `folders/<int:pk>/` | `GET` `PUT` `PATCH` `DELETE` |
| `tags/` | `GET` `POST` | Get list of tags (tag names are unique per user) |
| `tags/<int:pk>/` | `GET` `PUT` `PATCH` `DELETE` |

## Usage
- **Register**
![Postman register user](usage_photos/postman_register.png)

- **Get profile**
![Postman GET profile](usage_photos/postman_profile.png)

- **Change password**
![Postman change password](usage_photos/postman_change_password.png)

- **Get all registered user profiles**
![Postman GET user profiles](usage_photos/postman_all_profiles.png)

- **Get all entries**
![Postman GET entries](usage_photos/postman_entries.png)

- **Create entry**
![Postman POST entry](usage_photos/postman_create_entry.png)

- **Get all folders**
![Postman GET folders](usage_photos/postman_folders.png)

- **Get all tags**
![Postman GET tags](usage_photos/postman_tags.png)


## Installation
1. **Clone the repo**
```
git clone https://github.com/stealacamera/diary-api.git
```
2. **Create and activate a virtual environment**
```
virtualenv <venv name>
<venv name>\Scripts\activate
```
3. **Install the dependencies**
```
pip install -r requirements.txt
```
4. **Run migrations and server**
```
python manage.py migrate
python manage.py runserver
```
