redFlag = []

class RaiseRedFlagModel(object):
    def __init__(self):
        self.db = redFlag
    def save(self, id, createdOn, createdBy, ci_type, location, status, photo, video, comments):
        
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

    def updateRecord(self, comment, index):
        data = comment

        for comment in self.db:
            self.db[index]['comment'] = data

    def find(self, id):
        for record in self.db:
            if record['id'] == id:
                return record
            None