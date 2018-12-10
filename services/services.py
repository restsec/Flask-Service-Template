# -*- coding: utf-8 -*-
import requests
import json
import logging
from time import sleep

http_gateway = "http://localhost"

#
def request_and_retry(request, args, retry=3):
    """
    write_message function will post a message to a queue using the AMQP 0-9-1 protocol.

    This function helps ensure all messages are posted correclty. They are posted with delivery_mode = 2, this means they are made persistent, and if the queue fails, the messages will be kept in disk storage.

    Parameters
    ----------
    request : function
        Message to be posted as body in the message queue. It should be encoded in the desired scheme (JSON, MessagePack)
    args : list
        List of args to  be parsed into the request.
    retry : int
        Numer of retry attempts to be performed if the operation fails.
        

    Returns
    -------
    bool
        True : Operation Successfull
        False: Operation Failed. In this case, logging.error and logging.critical messages will be produced, after n logging.info messages, n being the ammount of attempts.

    """
    res, err = request(args)
    if err != None:
        if retry <= 0:
            logging.error('Failed http request after all attempts.' )
            logging.critical(err)
            return res, err
        logging.error('Failed http request. Remaining attempts : %d' %retry)
        logging.error(err)

        sleep(1)
        return request_and_retry(request, args, retry - 1)
    return res, err


# Eaxample get function
def __get_code(args):
    url = http_gateway + f"/status/{args[0]}"

    try:
        r = requests.get(url,timeout=3)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logging.error(f"Http Error:{err}")
        return None,err
    except requests.exceptions.ConnectionError as err:
        logging.error(f"Error Connecting: {err}")
        return None,err
    except requests.exceptions.Timeout as err:
        logging.error(f"Timeout Error: {err}")
        return None, err
    except requests.exceptions.RequestException as err:
        logging.error(f"Some Else {err}")
        return None,err
    return r.json(), None