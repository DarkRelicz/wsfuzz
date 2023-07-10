import websocket

# open WebSocket connection
def initWsConn(url):
    ws = websocket.create_connection(url,timeout=3)
    return ws

# send requests to target WebSocket server
def InteractWithWsSite(ws, message):
    
    try: 
        # Send the message to the WebSocket server
        
        ws.send(message)

        # Receive and process the response from the WebSocket server in chunks
        response = ''
        while True:
            chunk = ws.recv()
            response += chunk
            if len(chunk) < 4096:  # Adjust the chunk size as needed
                break
    # reopens the websocket connection and move on the the next payload
    except websocket.WebSocketTimeoutException:
        response = "Connection Timed Out"
    return response


#main function
def main():
    # Example usage
    websocket_url = 'ws://dvws.local:8080/authenticate-user'  # Replace with the actual WebSocket URL
    message_to_send = '{"auth_user":"Jw==","auth_pass":"Jw=="}'  # Replace with the message you want to send
    InteractWithWsSite(initWsConn(websocket_url), message_to_send)

#__main__ functiuon
if __name__ == "__main__":
    main()