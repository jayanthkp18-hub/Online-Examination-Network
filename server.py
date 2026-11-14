
import json
import socket
import threading
import time

HOST = "0.0.0.0"
PORT = 5000
EXAM_DURATION = 120

QUESTIONS = [
    {
        "question": "Which layer of the OSI model handles routing?",
        "options": ["A. Physical", "B. Network", "C. Transport", "D. Session"],
        "answer": "B"
    },
    {
        "question": "Which protocol provides reliable data delivery?",
        "options": ["A. UDP", "B. IP", "C. TCP", "D. ARP"],
        "answer": "C"
    },
    {
        "question": "What does DNS stand for?",
        "options": [
            "A. Domain Name System",
            "B. Data Network Service",
            "C. Digital Naming System",
            "D. Domain Network Security"
        ],
        "answer": "A"
    }
]


def send_message(conn, data):
    message = json.dumps(data) + "\n"
    conn.sendall(message.encode())


def receive_message(conn):
    buffer = bytearray()

    while True:
        char = conn.recv(1)

        if not char:
            return None

        if char == b"\n":
            return json.loads(buffer.decode())

        buffer.extend(char)


def handle_client(conn, address):
    print(f"[CONNECTED] {address}")

    try:
        start_time = time.monotonic()
        score = 0
        

        send_message(conn, {
            "type": "welcome",
            "message": "Welcome to the Online Examination Network",
            "duration": EXAM_DURATION
        })

        for index, question in enumerate(QUESTIONS):

            remaining = EXAM_DURATION - (time.monotonic() - start_time)

            if remaining <= 0:
                send_message(conn, {"type": "timeout"})
                break

            send_message(conn, {
                "type": "question",
                "number": index + 1,
                "total": len(QUESTIONS),
                "question": question["question"],
                "options": question["options"],
                "remaining": int(remaining)
            })

            conn.settimeout(remaining)

            try:
                response = receive_message(conn)
            except TimeoutError:
                send_message(conn, {"type": "timeout"})
                break

            if response is None:
                break
            if (response.get("type") == "answer" and response.get("answer", "").upper() == question["answer"]):
                score += 1

        send_message(conn, {
            "type": "result",
            "score": score,
            "total": len(QUESTIONS)
        })

        print(f"[RESULT] {address} | Score: {score}/{len(QUESTIONS)}")

    except (ConnectionError, OSError, json.JSONDecodeError) as error:
        print(f"[ERROR] {address}: {error}")

    finally:
        conn.close()
        print(f"[DISCONNECTED] {address}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER] Listening on {HOST}:{PORT}")

    while True:
        conn, address = server.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(conn, address),
            daemon=True
        )
        thread.start()


if __name__ == "__main__":
    start_server()
