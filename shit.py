from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel , QLineEdit, QPushButton
import sys
import requests as req
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from os import path
    
    
class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PlayerUserInfoLookup")
        self.setGeometry(400,400,400,600)
        self.setFixedSize(400,600)

        
        self.label = QLabel("Roblox info checker", self)
        self.entry = QLineEdit(self)
        self.btn = QPushButton("Get info", self)
        self.label1 = QLabel("", self)
        self.label2 = QLabel(self)
        
        self.label.setStyleSheet("font-size: 30px;"
                            "font-family: Inter;"
                            "text-decoration:" "underline;"
                            "font-weight:" "bold;")
        self.btn.setStyleSheet("""
    QPushButton {
        background-color: #E52521; color: white; font-size: 20px; font-family: Inter; border-radius: 10px;
    }
    QPushButton:hover {
        background-color: #FF3333;
    }
""")
        self.entry.setStyleSheet("font-size: 20px;"
                            "font-family: Inter;"
                            "border-radius:" "10px;")
        self.label.setGeometry(0,0,400,400)
        self.label.setAlignment(Qt.AlignHCenter)
        self.entry.setGeometry(90,100,200,40)
        self.btn.setGeometry(90,140,200,40)
        self.btn.clicked.connect(self.get_info)
        self.label1.setGeometry(90,180,400,150)
        
    def get_info(self):
        inp = self.entry.text().strip()
        if len(inp) < 20:
            if len(inp) >= 3:
                url = f"https://users.roblox.com/v1/usernames/users"
                data = {"usernames": [inp], "excludeBannedUsers": False}
                r = req.post(url=url,json=data)

                
                if r.status_code == 200:
                    r = r.json()
                    if r['data']:
                        user_info = r['data'][0]
                        url1 = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_info['id']}&size=150x150&format=Png"
                        r1 = req.get(url1)
                        if r1.status_code == 200:
                            r1 = r1.json()
                            data = r1['data'][0]['imageUrl']
                            r2 = req.get(data).content
                            if not path.exists(f"player{user_info['id']}.png"):
                                with open(f"player{user_info['id']}.png", "wb") as f:
                                    f.write(r2)
                            pixmap = QPixmap(f"player{user_info['id']}.png")
                            self.label2.setPixmap(pixmap)
                            self.label2.setScaledContents(True)
                            self.label2.setGeometry(90,400,200,200)
                            self.label1.setText(f"username: {user_info['name']}\n"
                                                f"Verified: {user_info['hasVerifiedBadge']}\n"
                                                f"id: {user_info['id']}\n"
                                                f"DisplayName: {user_info['displayName']}\n\n"
                                                f"Avatar image:")
                            self.label1.setStyleSheet("font-size:" "20px;"
                                                    "font-weight:" "bold;"
                                                    "font-family:" "Inter;")
                        
                        else:
                            self.label1.setText(f"error: {r1.status_code}")
                    
                    else:
                        self.label1.setText(f"error")
                else:
                    self.label1.setText(f"error: {r.status_code}")
            else:
                self.label1.setText("Username must be more than 3 characters")
        else:
            self.label1.setText("Username must only have upto 20 Characters")
    

                        
def main():
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    sys.exit(app.exec_())
    

main()

