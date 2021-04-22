import socketio

# serve static files
static_files = {
    '': './public',
}

# create a Socket.IO server
sio = socketio.Server(async_mode='eventlet')
# wrap with a WSGI application
app = socketio.WSGIApp(sio, static_files=static_files)

if __name__ == '__main__':
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)