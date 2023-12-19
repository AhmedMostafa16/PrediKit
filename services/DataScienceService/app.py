from io import StringIO
import logging
import traceback
from typing import Dict

import executor
from flask import (
    Flask,
    jsonify,
    request,
)
import msgpack
import pandas

app = Flask(__name__)


@app.route("/")
def hello_world():  # put application's code here
    return "Hello World!"


@app.route("/get_all_columns", methods=["POST"])  # type: ignore
def get_all_columns():
    try:
        # Get MessagePack-encoded data from the request
        data = request.get_data()
        logging.debug("Got data")

        # Decode MessagePack data
        decoded_data: str = msgpack.unpackb(data, raw=False)
        logging.debug("Decoded data")

        df = (
            pandas.read_json(
                orient="records", path_or_buf=StringIO(decoded_data)
            )
            if decoded_data
            else pandas.DataFrame()
        )

        # Process the data (you can modify this part based on your requirements)
        result = list(df.columns)

        print("result: ", result)
        # Encode the result in MessagePack format
        encoded_result = msgpack.packb(result)
        print("encoded_result: ", encoded_result)

        return encoded_result, 200, {"Content-Type": "application/msgpack"}

    except Exception as e:
        # Handle exceptions appropriately
        error_message = {"error": str(e)}
        encoded_error = jsonify(error_message)

        traceback.print_exc()


@app.route("/execute_node", methods=["POST"])  # type: ignore
def execute_node():
    try:
        # Get MessagePack-encoded data from the request
        data = request.get_data()
        logging.debug("Got data")

        # Decode MessagePack data
        decoded_data: Dict = msgpack.unpackb(data, raw=False)
        logging.debug("Decoded data")

        props = decoded_data["Data"]
        df = (
            pandas.read_json(
                orient="records",
                path_or_buf=StringIO(decoded_data["DataFrame"]),
            )
            if decoded_data["DataFrame"]
            else pandas.DataFrame()
        )

        # Process the data (you can modify this part based on your requirements)
        result = executor.execute_node(
            props=props, df=df, node_type=decoded_data["Type"]
        )
        result = result.to_json(orient="records") if result is not None else ""
        # Encode the result in MessagePack format
        encoded_result = msgpack.packb(result)

        return encoded_result, 200, {"Content-Type": "application/msgpack"}

    except Exception as e:
        # Handle exceptions appropriately
        error_message = {"error": str(e)}
        encoded_error = jsonify(error_message)

        traceback.print_exc()  # Print the stack trace

        print("error: ", error_message)
        return encoded_error, 500, {"Content-Type": "application/msgpack"}


if __name__ == "__main__":
    app.run(debug=True, port=5501)
