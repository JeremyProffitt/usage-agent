from modelcontext import Table, Column, Integer, String, ModelContext

class prc(Table):
    id = Column(Integer, primary_key=True)
    projectid = Column(Integer)
    record = Column(String)

class van(Table):
    id = Column(Integer, primary_key=True)
    name = Column(String)

class user(Table):
    id = Column(Integer, primary_key=True)
    name = Column(String)

class projects(Table):
    id = Column(Integer, primary_key=True)
    Customer = Column(String)

class prc_event(Table):
    id = Column(Integer, primary_key=True)
    projectid = Column(Integer)
    userid = Column(Integer)
    vanid = Column(Integer)
    etype = Column(String)
    currentstate = Column(Integer)
    timestamp = Column(String)

model = ModelContext(tables=[prc, van, user, projects, prc_event])