from modelcontext import Table, Column, Integer, String, ModelContext

class Users(Table):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

class Orders(Table):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    amount = Column(Integer)

model = ModelContext(tables=[Users, Orders])