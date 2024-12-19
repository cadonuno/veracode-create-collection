import argparse
import sys
from veracode_api_py.collections import Collections
from veracode_api_py.applications import Applications
from veracode_api_py.identity import BusinessUnits


def get_application_ids(applications):
    application_ids = []
    for application in applications:
        matches = Applications().get_by_name(application)
        if not matches or len(matches) == 0:
            print(f"Application named '{application}' not found")
            sys.exit(-1)
        for match in matches:
            if match["profile"]["name"] == application.strip():
                application_ids.append(match["guid"])
                break
            print(f"Application named '{application}' not found")
            sys.exit(-1)
    return application_ids

def get_business_unit_id(business_unit):
    matches = BusinessUnits().get_all()
    if not matches or len(matches) == 0:
        print(f"Business Unit named '{business_unit}' not found")
        sys.exit(-1)
    for match in matches:
        if match["bu_name"] == business_unit.strip():
            return match["bu_id"]
    print(f"Business Unit named '{business_unit}' not found")
    sys.exit(-1)

def parse_custom_field(custom_field):
    split_field = custom_field.split(":")
    if not split_field or len(split_field) != 2:
        print(f"Invalid custom field definition: {custom_field}")
    return {
        "name": split_field[0],
        "value": split_field[1]
    }

def main():
    parser = argparse.ArgumentParser(
        description="This script allows for the creation of Custom User Roles in Veracode."
    )
    parser.add_argument(
        "-n",
        "--name",
        help="Name of the collection to create.",
        required=True
    )
    parser.add_argument(
        "-d",
        "--description",
        help="Description of the collection.",
        required=False
    )
    parser.add_argument(
        "-b",
        "--business_unit",
        help="Name of the Business unit to assign to the collection.",
        required=False
    )
    parser.add_argument(
        "-a",
        "--application",
        help="Applications to add, requires 1 or more.",
        action="append",
        required=True
    )
    parser.add_argument(
        "-c",
        "--custom_field",
        help="(Optional) Colon(:)-separated key-value pairs for the custom fields to set, takes 0 or more. I.e.: A Field:Some Value",
        action="append",
        required=True
    )
    parser.add_argument(
        "-k",
        "--keep",
        help="If a collection with this name already exists, will add the applications to it (Defaults to false) - if this is not set, the step will fail instead.",
        required=False, 
        action=argparse.BooleanOptionalAction
    )

    args = parser.parse_args()
    collection_id = Collections().get_by_name(args.name)

    if collection_id and not args.keep:
        print("A collection with this name already exists")
        print("To reuse this collection, adding the applications to it, you can use the --keep flag")
        sys.exit(-1)

    application_list = get_application_ids(args.application)
    business_unit_id = get_business_unit_id(args.business_unit)
    custom_fields = None if not args.custom_field else list(map(parse_custom_field, args.custom_field))

    if not collection_id:
        Collections().create(
            name=args.name,
            description=args.description,
            business_unit_guid=business_unit_id,
            custom_fields=custom_fields,
            assets=application_list
        )
        print(f"Collection {args.name} CREATED successfully")
    else:
        Collections().update(
            guid=collection_id,
            name=args.name,
            description=args.description,
            business_unit_guid=business_unit_id,
            custom_fields=custom_fields,
            assets=application_list
        )
        print(f"Collection {args.name} UPDATED successfully")
    



if __name__ == '__main__':
    main()
    