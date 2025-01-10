# Veracode Custom Roles

Allows for the creation of a collection in Veracode from the command-line

## Setup

Clone this repository:

    git clone https://github.com/cadonuno/veracode-create-collection

Install dependencies:

    cd veracode-create-collection
    pip install -r requirements.txt

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## Run

If you have saved credentials as above you can run:

    python create-collection.py (arguments)

Otherwise you will need to set environment variables:

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
    python create-collection.py (arguments)
    

* `--name`, `-n`  Name of the collection to create
* `--application`, `-a` Applications to add, requires 1 or more.
* `--description`, `-d` (optional): Description of the collection.
* `--business_unit`, `-b` (optional): Name of the Business unit to assign to the collection.
* `--custom_field`, `-c`(optional): Colon(:)-separated key-value pairs for the custom fields to set, takes 0 or more. I.e.: A Field:Some Value".
* `--keep`, `-l` (optional flag): if a collection with this name already exists, will add the applications to it (Defaults to false) - if this is not set, the step will fail instead.
