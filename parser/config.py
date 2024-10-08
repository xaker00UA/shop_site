import os

# TYPE = sys.argv[1].upper() if len(sys.argv) > 1 else "DEFAULT"

# if TYPE == "DEFAULT":
#     with open("settings.yaml", "r") as file:
#         data = yaml.safe_load(file)
# elif TYPE == "TEST":
#     with open("test_settings.yaml", "r") as file:
#         data = yaml.safe_load(file)
# else:
#     raise ValueError("Неправильные аргументы")

DB_CONNECTION = {
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
    "dbname": os.getenv("NAME"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
}
