import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session  # соединение с базой данных
import sqlalchemy.ext.declarative as dec  # помогает объявить бд

SqlAlchemyBase = dec.declarative_base()  # сюда будем наследовать модели

__factory = None  # для получения сессий подключения к нашей базе данных


def global_init(db_file):  # проверяет что мы первый раз подключились к бд.
    # если нет, то завершаем работу
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    # создаем строку подключения conn_str , которую передаем Sqlalchemy для того, чтобы она выбрала правильный движок работы с
    # базой данных (переменная engine).
    # В нашем случае это будет движок для работы с SQLite базами данных.
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:  # для получения сессии подключения к нашей базе данных
    global __factory
    return __factory()
