import json
from apimedic.database_builder import DatabaseBuilder


def main():
    builder = DatabaseBuilder()
    builder.set_start_disease(80)   # Set Cold as Starting disease

    builder.build_disease_list()
    with open("../database/diseases_100_db.json", "w") as outfile:
        json.dump(builder.diseases, outfile)

    # builder.get_issue_descriptions()


if __name__ == "__main__":
    main()
