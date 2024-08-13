"""
run this python method or use postman to just send:
POST on localhost:8080/engine-rest/message
with this body

{
    "messageName": "CANCEL_MESSAGE",
    "business_key": "111",
    "process_variables":{"msg": "CANCEL message received"}
}
"""


from camunda.client.engine_client import EngineClient


def message_correlation():
    client = EngineClient()
    resp_json = client.correlate_message(
        message_name="CANCEL_MESSAGE",
        business_key="111",
        # business_key="b4a6f392-12ab-11eb-80ef-acde48001122",
        process_variables={"msg": "CANCEL message received"}
    )
    print(resp_json)


if __name__ == "__main__":
    message_correlation()

