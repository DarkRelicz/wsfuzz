import websocket

def InteractWithWsSite(url, message):
    websocket.setdefaulttimeout(10)
    ws = websocket.create_connection(url)
    

    # Send the message to the WebSocket server
    ws.send(message)
    # print(f"Sent: {message}")

    # Receive and process the response from the WebSocket server in chunks
    response = ''
    while True:
        try:
            chunk = ws.recv()
            response += chunk
            if len(chunk) < 4096:  # Adjust the chunk size as needed
                break
        except websocket.WebSocketTimeoutException:
            response = "Connection Timed Out"
            break
    
    #print(f"Recieved: {response}")
    ws.close()
    return response


#main function
def main():
    # Example usage
    websocket_url = 'ws://dvws.local:8080/authenticate-user'  # Replace with the actual WebSocket URL
    message_to_send = '{"auth_user":"Jw==","auth_pass":"Jw=="}'  # Replace with the message you want to send
    InteractWithWsSite(websocket_url, message_to_send)

#__main__ functiuon
if __name__ == "__main__":
    main()