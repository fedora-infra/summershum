import socket
hostname = socket.gethostname()

config = {
    # This is just a key to tell the fedmsg-hub to initialize us.
    'summershum.enabled': True,

    # Here is where we will publish our status
    'endpoints': {
        'summershum.%s' % hostname: [
            "tcp://127.0.0.1:99887",
        ],
    },
}
