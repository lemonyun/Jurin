from jurinserver.models import title, rank
from jurinserver import db
import sqlalchemy
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine('sqlite:///D:\\Jurin\\Server\\jurinserver.db')
Session = sessionmaker(bind=engine)

q = title(title="qrr")
session = Session()
session.add(q)
session.commit()