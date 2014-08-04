

class Group(ndb.Model):
	#Group datastore
    group_title = ndb.StringProperty()
    group_description = ndb.TextProperty()

class Chores(ndb.model):
	#Chores datastore
	chore_title = ndb.StringProperty()
	chore_score = ndb.StringProperty()
	chore_assign = ndb.StringProperty()
	chore_status = ndb.StringProperty(required=False, choices=set(["Active", "Archived"]))
	chore_create_date = ndb.DateTimeProperty(auto_now_add=True)
	
		