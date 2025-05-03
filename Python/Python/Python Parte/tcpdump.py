import socket
import time

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception as e:
        print(f"Error: {e}")
        local_ip = None
    finally:
        s.close()
    
    return local_ip

def redirect():
    local_ip = get_local_ip()
    if not local_ip:
        print("Failed to retrieve local IP. Exiting.")
        return

    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        conn.bind((local_ip, 0))  

        conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        with open("logs.txt", "w") as log_file:
            try:
                print("Capturing packets...")
                while True:
                    raw_data, addr = conn.recvfrom(65536)  
                    packet_info = raw_data.hex()  
                    log_file.write(packet_info + "\n")
                    log_file.flush()
                    print(packet_info)
                    time.sleep(0.1)  
            except KeyboardInterrupt:
                print("Interrumpido por el usuario.")
            finally:
               
                conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
                conn.close()
                print("Socket closed, packet capturing terminated.")
    except Exception as e:
        print(f"Error during socket operation: {e}")

if __name__ == "__main__":
    redirect()