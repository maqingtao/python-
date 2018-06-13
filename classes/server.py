from classes.user import User
from errno import ECONNABORTED, EBADF
from search.getChatName import getChatName
import classes.server_client_base as scb
import threading
import socket


class Server(scb.ServerClientBase):
    MAX_U_NAME_LEN = 16
    MIN_U_NAME_LEN = 4

    def __init__(self, port,username):
        super().__init__()
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username=username
        ip = socket.gethostbyname(socket.gethostname())
        while True:
            try:
                self._s.bind((ip, port))
                break
            except:
                port += 1

        self._users = {}
        self._host_user = User(self._s, ip, port,self.username)
        self._system_user = User(self._s, ip, port,"系统提示")
        self._lock = threading.Lock()
        th = threading.Thread(target=self.new_conn_handler)
        th.start()

    @property
    def host_ip(self):
        return self._host_user.ip

    @property
    def host_port(self):
        return self._host_user.port


    def new_conn_handler(self):
        while True:
            try:
                self._s.listen(5)
                sock, addr = self._s.accept() 
                #根据自身的ip来确定昵称
                chatName = getChatName().getName(addr[0])
                user = User(sock,chatName, addr[1])
                msg = chatName+"连接成功"
                with self._lock:
                    self._users[sock] = user
                    self.send_msg_as_sys_to_all(msg)
                
                th = threading.Thread(target=self.recv_handler, kwargs={'sock': sock})
                th.start()
            except Exception as e:
                if e.errno == ECONNABORTED or e.errno == EBADF:
                    # User closed the program
                    break
                
                self.send_msg_as_sys_to_user(repr(e), self._host_user)

    # This function is the function that gets called when GUI presses send btn
    def send_msg(self, msg):
        if not msg:
            return
        
        msg_type = self.determine_msg_type(msg)
        
        with self._lock:
            if msg_type == 2:
                self.change_user_name(self._host_user, msg[4:])
            else:
                self.send_msg_as_user_to_all(msg, self._host_user)

    def send_msg_as_sys_to_user(self, msg, to_user):
        if not msg:
            return

        msg = self.prepend_msg_header(msg, self._system_user)
        msg += '.'

        if to_user is self._host_user:
            self.show_msg(msg)
        else:
            self.send_msg_to_user(msg, to_user)

    # Pre: call with lock
    def send_msg_as_sys_to_all(self, msg):
        if not msg:
            return

        msg = self.prepend_msg_header(msg, self._system_user)
        msg += '.'
        
        self.send_msg_to_all(msg)

    def send_msg_as_user_to_user(self, msg, as_user, to_user):
        if not msg:
            return

        msg = self.prepend_msg_header(msg, as_user)
        self.send_msg_to_user(msg, to_user)
    
    # Pre: call with lock
    def send_msg_as_user_to_all(self, msg, as_user):
        if not msg:
            return

        msg = self.prepend_msg_header(msg, as_user)
        self.send_msg_to_all(msg)

    def prepend_msg_header(self, msg, as_user):
        return as_user.name + ': ' + msg

    # Pre: Call with lock for thread safety
    def send_msg_to_all(self, msg):
        for user in self._users.values():
            try:
                self.send_msg_to_user(msg, user)
            except Exception as e:
                self.send_msg_as_sys_to_user(repr(e), self._host_user)

        # To ensure what I see is what they see
        self._msg_queue.put(msg)

    def send_msg_to_user(self, msg, to_user):
        to_user.sock.sendall(msg.encode())

    def recv_handler(self, sock):
        while True:
            try:
                msg = sock.recv(1024)
                msg = msg.decode()
                msg_type = self.determine_msg_type(msg)

                with self._lock:
                    user = self._users[sock]
                    if msg_type == 1:
                        self.handle_disconnected(user)
                        break
                    elif msg_type == 2:
                        self.change_user_name(user, msg[4:])
                    else:
                        self.send_msg_as_user_to_all(msg, user)
            except Exception as e:
                if e.errno == EBADF:    
                    # User closed the program
                    break
                self.send_msg_as_sys_to_user(repr(e), self._host_user)

    def determine_msg_type(self, msg):
        if not msg:
            return 1

        if len(msg) >= 5 and msg[:4] == "/nc ":
            return 2

        return 3

    # Pre: call with lock for thread safety
    def handle_disconnected(self, user):
        msg = user.name + " is disconnected" 
        self.send_msg_as_sys_to_all(msg)
        user.sock.close()
        del self._users[user.sock]

    def show_msg(self, msg):
        self._msg_queue.put(msg)
    
    def destroy(self):
        with self._lock:
            for sock in self._users.keys():
                sock.close()
            self._s.close()

