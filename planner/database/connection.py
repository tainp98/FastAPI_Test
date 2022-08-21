from sqlmodel import SQLModel, Session, create_engine

# from models.events import Event

database_file = "planner.db"
database_connection_string = f"sqlite:///{database_file}"

connect_args = {"check_same_thread": False}
engine = create_engine('mysql+pymysql://root:admin@172.17.0.2:3306/event', echo=True)
print(engine)
def conn():
    SQLModel.metadata.create_all(engine, )


def get_session():
    with Session(engine) as session:
        yield session