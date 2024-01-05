import ast
import configparser
import pathlib

from pyspark.sql import SparkSession


def grant_permissions() -> None:
    """Grants a set of permissions on an object to a principal(user, group, or service principal)
    """
    # Read "grant_permissions_config.ini" & parse configs
    grant_permissions_config_path = (
        pathlib.Path(__file__).parent / "grant_permissions_config.ini"
    )
    grant_permissions_config = configparser.ConfigParser()
    grant_permissions_config.read(grant_permissions_config_path)
    permissions = ast.literal_eval(grant_permissions_config["options"]["permissions"])

    # Get or Create SparkSession
    spark = SparkSession.builder.getOrCreate()

    # Grant a set of permissions to a UC object for one or more principals(user, group, or service principal)
    for permission in permissions:
        object_name = permission["object_name"]
        object_type = permission["object_type"]
        grants = ", ".join(str(grant) for grant in permission["grants"])
        principals = permission["principals"]
        for principal in principals:
            spark.sql(
                f"GRANT {grants} ON {object_type} `{object_name}` TO `{principal}`"
            )


if __name__ == "__main__":
    grant_permissions()
