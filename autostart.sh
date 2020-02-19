sleep 5 && chromium-browser --kiosk --disable-session-crashed-bubble http://localhost:5000  && unclutter -idle 0.1 -root &
sudo python3 server.py

