def get_all_tasks(loop):
    tasks = asyncio.all_tasks(loop=loop)

    # Print information about each task
    for task in tasks:
        print("Task:", task)
        print("Task ID:", id(task))
        print("Task Name:", task.get_name())
        print("Task State:", task.get_stack())


def print_client_details(websocket):
    client_address = websocket.scope["client"]
    client_ip = client_address[0]  # Get the client's IP address
    client_port = client_address[1]  # Get the client's port
    print("Client IP Address:", client_ip)
    print("Client Port:", client_port)

