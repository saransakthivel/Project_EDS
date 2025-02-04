import logging

# logging.basicConfig(
#     filename="service_debug.log",
#     level=logging.DEBUG,
#     format="%(asctime)s [%(levelname)s] %(message)s"
# )

# logging.debug("Debug log")
# logging.info("Info log")
# logging.error("Error log")


# import os
# try:
#     with open("C:\\xml_to Sql_store\\service_debug.log", "a") as f:
#         f.write("Log file test entry.\n")
# except Exception as e:
#     print(f"Error: {e}")

logging.basicConfig(
    filename="C:\\Users\\admin\\OneDrive - E 4 Energy Solutions\\Saturn Pyro Files\\Documents\\Project EDS\\xml_to Sql_store\\logs\\service_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
    force=True
)
logging.debug("Debug log")
logging.info("Info log")
logging.error("Error log")

