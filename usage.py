import wsHandler as w

# Example usage
websocket_url = 'ws://dvws.local:8080/authenticate-user'  # Replace with the actual WebSocket URL
message_to_send = '{"auth_user":"Jw==","auth_pass":"Jw=="}'  # Replace with the message you want to send
response = w.InteractWithWsSite(websocket_url, message_to_send)
print(response)
