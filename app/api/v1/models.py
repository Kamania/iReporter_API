users = []
redFlag = []


class UserModel:
    """Saves the user"""
    def __init__(self):
        self.db = users

    def save(self, id, firstname, lastname, othernames, email, phoneNumber,
             username, registeredOn, isAdmin, password, password_confirmation):
        payload = {
            'id': len(users)+1,
            'firstname': firstname,
            'lastname': lastname,
            'othernames': othernames,
            'email': email,
            'phoneNumber': phoneNumber,
            'username': username,
            'registeredOn': registeredOn,
            'isAdmin': isAdmin,
            'password': password,
            'password_confirmation': password_confirmation
        }

        self.db.append(payload)
        return self.db

    def get_user_data(self):
        return self.db


class RaiseRedFlagModel(object):
    def __init__(self):
        self.db = redFlag

    def save(self, id, createdOn, createdBy, ci_type, location, status, photo,
             video, comments):
        data = {
            "id": len(redFlag)+1,
            "createdOn": createdOn,
            "createdBy": createdBy,
            "type": ci_type,
            "location": location,
            "status": status,
            "photo": photo,
            "video": video,
            "comments": comments
        }

        self.db.append(data)

        return self.db

    def get_redFlag(self):
        """Returns all the records in the list redFlag"""
        return self.db

    def find(self, id):
        for record in self.db:
            if str(record['id']) == str(id):
                return record
            None
