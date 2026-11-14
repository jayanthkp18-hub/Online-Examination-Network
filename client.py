
import json
import socket

SERVER_HOST = "10.0.0.1"
SERVER_PORT = 5000


def send_message(sock, data):
    message = json.dumps(data) + "\n"
    sock.sendall(message.encode())


def receive_message(sock):
    buffer = bytearray()

    while True:
        char = sock.recv(1)

        if not char:
            return None

        if char == b"\n":
            return json.loads(buffer.decode())

        buffer.extend(char)


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((SERVER_HOST, SERVER_PORT))

        print("Connected to Examination Server!\n")

        while True:
            message = receive_message(client)

            if message is None:
                print("Server disconnected.")
                break

            message_type = message.get("type")

            if message_type == "welcome":
                print(message["message"])
                print("Exam duration:", message["duration"], "seconds\n")

            elif message_type == "question":
                print(f"\nQuestion {message['number']}/{message['total']}")
                print(message["question"])

                for option in message["options"]:
                    print(option)

                print("Remaining time:", message["remaining"], "seconds")

                answer = input("Enter your answer (A/B/C/D): ").strip().upper()

                if answer not in ["A", "B", "C", "D"]:
                    answer = "INVALID"

                send_message(client, {
                    "type": "answer",
                    "answer": answer
                })

            elif message_type == "timeout":
                print("\nTime is up!")

            elif message_type == "result":
                print("\n========== EXAM RESULT ==========")
                print("Your Score:", message["score"])
                print("Total Marks:", message["total"])
                print("================================")
                break

    except ConnectionRefusedError:
        print("Cannot connect to examination server.")

    except (ConnectionError, OSError, json.JSONDecodeError) as error:
        print("Communication error:", error)

    finally:
        client.close()


if __name__ == "__main__":
    start_client()
